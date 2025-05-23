#!/usr/bin/env python3

# Copyright 2020 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
"""A script to generate build.gradle from template and run fetch_all.py

More specifically, to generate build.gradle:
  - It downloads the BUILD_INFO file for the latest androidx snapshot from
    https://androidx.dev/snapshots/builds
  - It replaces {{androidx_repository_url}} with the URL for the latest snapshot
  - For each dependency, it looks up the version in the BUILD_INFO file and
    substitutes the version into {{androidx_dependency_version}}.
"""

import argparse
import contextlib
import json
import logging
import os
import pathlib
import re
import shutil
import stat
import sys
import subprocess
import tempfile
import urllib
from urllib import request

_ANDROIDX_PATH = os.path.normpath(os.path.join(__file__, '..'))
_CIPD_PATH = os.path.join(_ANDROIDX_PATH, 'cipd')
_SRC_PATH = os.path.normpath(os.path.join(_ANDROIDX_PATH, '..', '..'))

sys.path.insert(1, os.path.join(_SRC_PATH, 'third_party', 'depot_tools'))
import gclient_eval

_FETCH_ALL_PATH = os.path.normpath(
    os.path.join(_ANDROIDX_PATH, '..', 'android_deps', 'fetch_all.py'))

# URL to BUILD_INFO in latest androidx snapshot.
_ANDROIDX_LATEST_SNAPSHOT_BUILD_INFO_URL = 'https://androidx.dev/snapshots/latest/artifacts/BUILD_INFO'
# URL to BUILD_INFO in a specific androidx snapshot.
_ANDROIDX_VERSIONED_BUILD_INFO_URL = 'https://androidx.dev/snapshots/builds/{{version}}/artifacts/BUILD_INFO'

# Path to package listed in //DEPS
_DEPS_PACKAGE = 'src/third_party/androidx/cipd'
# CIPD package name
_CIPD_PACKAGE = 'chromium/third_party/androidx'

# Snapshot repository URL with {{version}} placeholder.
_SNAPSHOT_REPOSITORY_URL = 'https://androidx.dev/snapshots/builds/{{version}}/artifacts/repository'

# When androidx roller is breaking, and a fix is not immenent, use this to pin a
# broken library to an old known-working version.
# * The first element of each tuple is the path to the artifact of the latest
#   version of the library. It could change if the version is rev'ed in a new
#   snapshot.
# * The second element is a URL to replace the file with. Find the URL for older
#   versions of libraries by looking in the BUILD_INFO for the older version
#   (e.g.: https://androidx.dev/snapshots/builds/8545498/artifacts/BUILD_INFO)
_OVERRIDES = [
    # Example:
    #('androidx_core_core/core-1.9.0-SNAPSHOT.aar',
    # 'https://androidx.dev/snapshots/builds/8545498/artifacts/repository/'
    # 'androidx/core/core/1.8.0-SNAPSHOT/core-1.8.0-20220505.122105-1.aar'),
]


def _build_snapshot_repository_url(version):
    return _SNAPSHOT_REPOSITORY_URL.replace('{{version}}', version)


def _parse_dir_list(dir_list):
    """Computes 'library_group:library_name'->library_version mapping.

    Args:
      dir_list: List of androidx library directories.
    """
    dependency_version_map = dict()
    for dir_entry in dir_list:
        stripped_dir = dir_entry.strip()
        if not stripped_dir.startswith('repository/androidx/'):
            continue
        dir_components = stripped_dir.split('/')
        # Expected format:
        # "repository/androidx/library_group/library_name/library_version/pom_or_jar"
        if len(dir_components) < 6:
            continue
        dependency_package = 'androidx.' + '.'.join(dir_components[2:-3])
        dependency_module = '{}:{}'.format(dependency_package,
                                           dir_components[-3])
        if dependency_module not in dependency_version_map:
            dependency_version_map[dependency_module] = dir_components[-2]
    return dependency_version_map


@contextlib.contextmanager
def _build_dir():
    dirname = tempfile.mkdtemp()
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)


def _get_latest_androidx_version():
    androidx_build_info_response = request.urlopen(
        _ANDROIDX_LATEST_SNAPSHOT_BUILD_INFO_URL)
    # Get the versioned url from the redirect destination.
    androidx_build_info_url = androidx_build_info_response.url
    androidx_build_info_response.close()
    logging.info('URL for the latest build info: %s', androidx_build_info_url)
    # Strip '/repository' from pattern.
    resolved_snapshot_repository_url_pattern = (
        _build_snapshot_repository_url('([0-9]*)').rsplit('/', 1)[0])
    version = re.match(resolved_snapshot_repository_url_pattern,
                       androidx_build_info_url).group(1)
    return version


def _query_cipd_tags(version):
    cipd_output = subprocess.check_output(
        ['cipd', 'describe', _CIPD_PACKAGE, '-version', version],
        encoding='utf-8')
    # Output looks like:
    # Package:       chromium/third_party/androidx
    # Instance ID:   gUjEawxv5mQO8yfbuC8W-rx4V3zYE-4LTWggXpZHI4sC
    # Registered by: user:chromium-cipd-builder@chops-service-accounts.iam.gserviceaccount.com
    # Registered at: 2025-01-06 17:54:48.034135 +0000 UTC
    # Refs:
    #   latest
    # Tags:
    #   details0:version-cr-012873390
    #   version:cr-012873390
    lines = cipd_output.split('\n')
    tags = {}
    parsing_tags = False
    for line in lines:
        if not line.strip():
            continue
        if line.startswith('Tags:'):
            parsing_tags = True
            continue
        if parsing_tags:
            tag, value = line.strip().split(':', 1)
            tags[tag] = value
    return tags


def _get_current_cipd_instance():
    with open(os.path.join(_SRC_PATH, 'DEPS'), 'rt') as f:
        gclient_dict = gclient_eval.Exec(f.read())
        return gclient_eval.GetCIPD(gclient_dict, _DEPS_PACKAGE, _CIPD_PACKAGE)


def _get_current_androidx_version():
    cipd_instance = _get_current_cipd_instance()
    cipd_tags = _query_cipd_tags(cipd_instance)
    version_string = cipd_tags['version']
    version = version_string[len('cr-0'):]
    return version


def _download_and_parse_build_info(version):
    """Downloads and parses BUILD_INFO file."""
    with _build_dir() as build_dir:
        androidx_build_info_url = _ANDROIDX_VERSIONED_BUILD_INFO_URL.replace(
            '{{version}}', version)
        androidx_build_info_response = request.urlopen(androidx_build_info_url)

        androidx_build_info_path = os.path.join(build_dir, 'BUILD_INFO')
        build_info_contents = androidx_build_info_response.read().decode(
            'utf-8')
        with open(androidx_build_info_path, 'w') as f:
            f.write(build_info_contents)

        build_info_dict = json.loads(build_info_contents)
        dir_list = build_info_dict['target']['dir_list']

        return dir_list


def _create_local_dir_list(repo_path):
    repo_path = repo_path.rstrip('/')
    prefix_len = len(repo_path) + 1
    ret = []
    for dirpath, _, filenames in os.walk(repo_path):
        for name in filenames:
            ret.append(os.path.join('repository', dirpath[prefix_len:], name))
    return ret


def _process_build_gradle(template_path, output_path, dependency_version_map,
                          androidx_repository_url):
    """Generates build.gradle from template.

    Args:
      template_path: Path to build.gradle.template.
      output_path: Path to build.gradle.
      dependency_version_map: An "dependency_group:dependency_name"->dependency_version mapping.
      androidx_repository_url: URL of the maven repository.
    """
    version_re = re.compile(r'\s*\w+ompile\s+[\'"]([^:]+:[^:]+):(.+?)[\'"]')
    template_text = pathlib.Path(template_path).read_text()
    deps_with_custom_versions = set()
    sb = []
    for line in template_text.splitlines(keepends=True):
        line = line.replace('{{androidx_repository_url}}',
                            androidx_repository_url)
        if m := version_re.search(line):
            name, version = m.groups()
            if version == '{{androidx_dependency_version}}':
                new_version = dependency_version_map.get(name)
                if new_version is None:
                    raise Exception(f'Version for {name} not found.')
                line = line.replace(version, new_version)
            else:
                deps_with_custom_versions.add(name)
        elif line.strip() == '{{version_overrides}}':
            sb.append('versionOverrideMap = [:]\n')
            for name, version in sorted(dependency_version_map.items()):
                if name not in deps_with_custom_versions:
                    sb.append(f"versionOverrideMap['{name}'] = '{version}'\n")
            deps_with_custom_versions = None
            continue

        sb.append(line)

    # build.gradle is not deleted after script has finished running. The file is in
    # .gitignore and thus will be excluded from uploaded CLs.
    pathlib.Path(output_path).write_text(''.join(sb))


def _write_cipd_yaml(libs_dir, version, cipd_yaml_path, experimental=False):
    """Writes cipd.yaml file at the passed-in path."""

    lib_dirs = os.listdir(libs_dir)
    if not lib_dirs:
        raise Exception('No generated libraries in {}'.format(libs_dir))

    data_files = [
        'BUILD.gn', 'VERSION.txt', 'additional_readme_paths.json',
        'build.gradle'
    ]
    for lib_dir in lib_dirs:
        abs_lib_dir = os.path.join(libs_dir, lib_dir)
        androidx_rel_lib_dir = os.path.relpath(abs_lib_dir, _CIPD_PATH)
        if not os.path.isdir(abs_lib_dir):
            continue
        lib_files = os.listdir(abs_lib_dir)
        if not 'cipd.yaml' in lib_files:
            continue

        for lib_file in lib_files:
            if lib_file == 'cipd.yaml' or lib_file == 'OWNERS':
                continue
            data_files.append(os.path.join(androidx_rel_lib_dir, lib_file))

    if experimental:
        package = 'experimental/google.com/' + os.getlogin() + '/androidx'
    else:
        package = 'chromium/third_party/androidx'
    contents = [
        '# Copyright 2021 The Chromium Authors',
        '# Use of this source code is governed by a BSD-style license that can be',
        '# found in the LICENSE file.',
        '# version: ' + version,
        'package: ' + package,
        'description: androidx',
        'data:',
    ]
    contents.extend('- file: ' + f for f in data_files)

    with open(cipd_yaml_path, 'w') as out:
        out.write('\n'.join(contents))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v',
                        '--verbose',
                        dest='verbose_count',
                        default=0,
                        action='count',
                        help='Verbose level (multiple times for more)')
    parser.add_argument('--local-repo',
                        help='Path to a locally androidx maven repo to use '
                        'instead of fetching the latest.')
    parser.add_argument(
        '--no-roll',
        action='store_true',
        help='If passed then we will not try rolling the '
        'latest androidx but use the currently rolled version.')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING - 10 * args.verbose_count,
        format='%(levelname).1s %(relativeCreated)6d %(message)s')

    if args.local_repo:
        version = 'local'
        dir_list = _create_local_dir_list(args.local_repo)
        androidx_snapshot_repository_url = ('file://' +
                                            os.path.abspath(args.local_repo))
    else:
        if args.no_roll:
            version = _get_current_androidx_version()
            logging.info('Resolved current androidx version to %s', version)
        else:
            version = _get_latest_androidx_version()
            logging.info('Resolved latest androidx version to %s', version)

        dir_list = _download_and_parse_build_info(version)
        androidx_snapshot_repository_url = _build_snapshot_repository_url(
            version)
        # Prepend '0' to version to avoid conflicts with previous version format.
        version = 'cr-0' + version

    if os.path.exists(_CIPD_PATH):
        shutil.rmtree(_CIPD_PATH)
    os.mkdir(_CIPD_PATH)

    dependency_version_map = _parse_dir_list(dir_list)
    _process_build_gradle(
        os.path.join(_ANDROIDX_PATH, 'build.gradle.template'),
        os.path.join(_CIPD_PATH, 'build.gradle'), dependency_version_map,
        androidx_snapshot_repository_url)
    shutil.copyfile(os.path.join(_ANDROIDX_PATH, 'BUILD.gn.template'),
                    os.path.join(_CIPD_PATH, 'BUILD.gn'))

    fetch_all_cmd = [
        _FETCH_ALL_PATH, '--android-deps-dir', _CIPD_PATH,
        '--ignore-vulnerabilities'
    ] + ['-v'] * args.verbose_count
    # Overrides do not work with local snapshots since the repository_url is
    # different.
    if not args.local_repo:
        for subpath, url in _OVERRIDES:
            fetch_all_cmd += ['--override-artifact', f'{subpath}:{url}']
    env = os.environ.copy()
    # Silence the --local warning in fetch_all.py that is not applicable here.
    env['SWARMING_TASK_ID'] = '1'
    subprocess.run(fetch_all_cmd, check=True, env=env)

    version_txt_path = os.path.join(_CIPD_PATH, 'VERSION.txt')
    with open(version_txt_path, 'w') as f:
        f.write(version)

    libs_dir = os.path.join(_CIPD_PATH, 'libs')
    yaml_path = os.path.join(_CIPD_PATH, 'cipd.yaml')
    _write_cipd_yaml(libs_dir,
                     version,
                     yaml_path,
                     experimental=bool(args.local_repo))


if __name__ == '__main__':
    main()

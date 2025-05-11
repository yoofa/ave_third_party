#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2025 youfa <vsyfar@gmail.com>
#
# Distributed under terms of the GPLv2 license.

"""
copy directories and files from google third_party repo

usage: copy_google_third_party.py GOOGLE_THIRD_PARTY_DIR DEST_DIR
"""

import os
import shutil
import sys

# copy directory list
dir_list = [
    "abseil-cpp",
    "accessibility_test_framework",
    "android_build_tools",
    "android_deps",
    "android_sdk",
    "android_toolchain",
    "androidx",
    "aosp_dalvik",
    "byte_buddy",
    "closure_compiler",
    "cpu_features",
    "flatbuffers",
    "google_benchmark",
    "googletest",
    "google-truth",
    "hamcrest",
    "icu4j",
    "ijar",
    "jdk",
    "jinja2",
    "jni_zero",
    "jsoncpp",
    "junit",
    "kotlinc",
    "kotlin_stdlib",
    "libc++",
    "libc++abi",
    "llvm-libc",
    "markupsafe",
    "opus",
    "protobuf",
    "protobuf-javascript",
    "r8",
    "re2",
    "robolectric",
    "sqlite4java",
    "turbine",
    "zlib",
]

file_list = [
    "libjpeg.gni"
]

def copy_item(src_path, dest_path):
    if os.path.isdir(src_path):
        print(f"Copying directory: {src_path} -> {dest_path}")
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        shutil.copytree(src_path, dest_path)
    elif os.path.isfile(src_path):
        print(f"Copying file: {src_path} -> {dest_path}")
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(src_path, dest_path)
    else:
        print(f"Warning: {src_path} does not exist, skipping.")

#main
def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    src_root = os.path.abspath(sys.argv[1])
    dest_root = os.path.dirname(os.path.abspath(__file__))  # script directory

    for rel_path in dir_list:
        src = os.path.join(src_root, rel_path)
        dest = os.path.join(dest_root, rel_path)
        copy_item(src, dest)

    for rel_path in file_list:
        src = os.path.join(src_root, rel_path)
        dest = os.path.join(dest_root, rel_path)
        copy_item(src, dest)
    

if __name__ == "__main__":
    main()

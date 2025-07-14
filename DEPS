# dependencies file

gclient_gn_args_file = 'build/config/gclient_args.gni'
gclient_gn_args = [
  'generate_location_tags',
]

vars = {
# Keep the Chromium default of generating location tags.
'generate_location_tags': True,

# By default, we should check out everything needed to run on the main
# chromium waterfalls. More info at: crbug.com/570091.
'checkout_configuration': 'default',
'checkout_instrumented_libraries': 'checkout_linux and checkout_configuration == "default"',
'chromium_revision': '4559b6b576fc5bd8f36ad7cde13bcf5215bec9dc',
# ninja CIPD package version
# https://chrome-infra-packages.appspot.com/p/infra/3pp/tools/ninja
'ninja_package': 'infra/3pp/tools/ninja/',

# reclient CIPD package version
'reclient_version': 're_client_version:0.176.0.8c46330a-gomaip',

'buildtools_gn_version': 'git_revision:ed1abc107815210dc66ec439542bee2f6cbabc00',

# ninja CIPD package version
# https://chrome-infra-packages.appspot.com/p/infra/3pp/tools/ninja
'ninja_version': 'version:3@1.12.1.chromium.4',

# condition to allowlist deps for non-git-source processing.
'non_git_source': 'True',

}

deps = {

  # openssl
  'third_party/openssl':
    'https://github.com/yoofa/third_party_openssl.git@cebc6ad07de0de260d41771692b216574c61d677',

  # chromium 
  'build':
    'https://chromium.googlesource.com/chromium/src/build@64e296c42a93fbd27acc9a94713e4289273409b2',
  'buildtools':
    'https://chromium.googlesource.com/chromium/src/buildtools@a660247d3c14a172b74b8e832ba1066b30183c97',
  'buildtools/linux64': {
    'packages': [
      {
        'package': 'gn/gn/linux-${{arch}}',
        'version': Var('buildtools_gn_version'),
      }
    ],
    'dep_type': 'cipd',
    'condition': 'checkout_linux',
  },
  'buildtools/mac': {
    'packages': [
      {
        'package': 'gn/gn/mac-${{arch}}',
        'version': Var('buildtools_gn_version'),
      }
    ],
    'dep_type': 'cipd',
    'condition': 'checkout_mac',
  },
  'buildtools/win': {
    'packages': [
      {
        'package': 'gn/gn/windows-amd64',
        'version': Var('buildtools_gn_version'),
      }
    ],
    'dep_type': 'cipd',
    'condition': 'checkout_win',
  },
  'buildtools/reclient': {
    'packages': [
      {
         # https://chrome-infra-packages.appspot.com/p/infra/rbe/client/
        'package': 'infra/rbe/client/${{platform}}',
        'version': Var('reclient_version'),
      }
    ],
    'dep_type': 'cipd',
    # Reclient doesn't have linux-arm64 package.
    'condition': 'not (host_os == "linux" and host_cpu == "arm64")',
  },

  'testing':
    'https://chromium.googlesource.com/chromium/src/testing@63412fdcdfe281e6b9531a5e1086a59c0b9e6909',

  'tools/clang/dsymutil': {
    'packages': [
      {
        'package': 'chromium/llvm-build-tools/dsymutil',
        'version': 'M56jPzDv1620Rnm__jTMYS62Zi8rxHVq7yw0qeBFEgkC',
      }
    ],
    'condition': 'checkout_mac',
    'dep_type': 'cipd',
  },

  'tools':
    'https://chromium.googlesource.com/chromium/src/tools@6820cc03cc8a4b1fb99747f30e8249d138a70981',

  'third_party/depot_tools':
    'https://chromium.googlesource.com/chromium/tools/depot_tools.git@80d1969422e75e8e9eecafa46074074b289e2568',

  'third_party/clang-format/script':
    'https://chromium.googlesource.com/external/github.com/llvm/llvm-project/clang/tools/clang-format.git@37f6e68a107df43b7d7e044fd36a13cbae3413f2',
  'third_party/libc++/src':
    'https://chromium.googlesource.com/external/github.com/llvm/llvm-project/libcxx.git@2e25154d49c29fa9aa42c30ad4a027bd30123434',
  'third_party/libc++abi/src':
    'https://chromium.googlesource.com/external/github.com/llvm/llvm-project/libcxxabi.git@8205ccf0f23545ebcd8846363ea1d29e77917a22',
  'third_party/llvm-libc/src':
    'https://chromium.googlesource.com/external/github.com/llvm/llvm-project/libc.git@12809bfa855813dcef51871e2ee3155e53ed35ea',
  'third_party/libunwind/src':
    'https://chromium.googlesource.com/external/github.com/llvm/llvm-project/libunwind.git@e55d8cf51c6db1fdd4bb56c158945ec59772c8ee',


  'third_party/ninja': {
    'packages': [
      {
        'package': Var('ninja_package') + '${{platform}}',
        'version': Var('ninja_version'),
      }
    ],
    'condition': 'non_git_source',
    'dep_type': 'cipd',
  },

  'third_party/googletest/src':
    'https://chromium.googlesource.com/external/github.com/google/googletest.git@2b6b042a77446ff322cd7522ca068d9f2a21c1d1',
  'third_party/re2/src':
    'https://chromium.googlesource.com/external/github.com/google/re2.git@6dcd83d60f7944926bfd308cc13979fc53dd69ca',

  'third_party/google_benchmark/src': {
    'url': 'https://chromium.googlesource.com/external/github.com/google/benchmark.git@761305ec3b33abf30e08d50eb829e19a802581cc',
  },

  'third_party/google-truth/src': {
      'url': 'https://chromium.googlesource.com/external/github.com/google/truth.git@33387149b465f82712a817e6744847fe136949b3',
      'condition': 'checkout_android',
  },

  'third_party/jsoncpp/source':
    'https://chromium.googlesource.com/external/github.com/open-source-parsers/jsoncpp.git@42e892d96e47b1f6e29844cc705e148ec4856448', # from svn 248

  'third_party/perfetto':
    'https://android.googlesource.com/platform/external/perfetto.git@a0c2bc7919f7467cf4a8287c8389c3f96a3fcbac',
  'third_party/protobuf-javascript/src':
    'https://chromium.googlesource.com/external/github.com/protocolbuffers/protobuf-javascript' + '@' + 'e34549db516f8712f678fcd4bc411613b5cc5295',

  'third_party/libsrtp':
    'https://chromium.googlesource.com/chromium/deps/libsrtp.git@a52756acb1c5e133089c798736dd171567df11f5',

  'third_party/catapult':
    'https://chromium.googlesource.com/catapult.git@b15611f18b506cf9dbc03e9bf87dbc8df549ccce',

  'third_party/ffmpeg':
    'https://chromium.googlesource.com/chromium/third_party/ffmpeg.git@d10a0f8bf5ddcce572df95105152bc74041cae0c',
  'third_party/nasm': {
      'url': 'https://chromium.googlesource.com/chromium/deps/nasm.git@f477acb1049f5e043904b87b825c5915084a9a29'
  },
  'third_party/libyuv':
    'https://chromium.googlesource.com/libyuv/libyuv.git@10592b60c0b2c33210b7752454253dc2625b4305',
  'third_party/libjpeg_turbo':
    'https://chromium.googlesource.com/chromium/deps/libjpeg_turbo.git@927aabfcd26897abb9776ecf2a6c38ea5bb52ab6',

  ### Android
  'third_party/android_sdk/public': {
      'packages': [
          {
              'package': 'chromium/third_party/android_sdk/public/build-tools/35.0.0',
              'version': 'DxwAZ3hD551Neu6ycuW5CPnXFrdleRBd93oX1eB_m9YC',
          },
          {
              'package': 'chromium/third_party/android_sdk/public/emulator',
              'version': '9lGp8nTUCRRWGMnI_96HcKfzjnxEJKUcfvfwmA3wXNkC',
          },
          {
              'package': 'chromium/third_party/android_sdk/public/platform-tools',
              'version': 'WihaseZR6cojZbkzIqwGhpTp92ztaGfqq8njBU8eTXYC',
          },
          {
              'package': 'chromium/third_party/android_sdk/public/platforms/android-35',
              'version': 'kIXA-9XuCfOESodXEdOBkW5f1ytrGWdbp3HFp1I8A_0C',
          },
          {
              'package': 'chromium/third_party/android_sdk/public/cmdline-tools',
              'version': 'bCFMX8oYIRJ_tP3tzaPcTKNqOAVdNk5TV_cwMp3GmE8C',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  'third_party/android_toolchain/ndk': {
    'packages': [
      {
        'package': 'chromium/third_party/android_toolchain/android_toolchain',
        'version': 'Idl-vYnWGnM8K3XJhM3h6zjYVDXlnljVz3FE00V9IM8C',
      },
    ],
    'condition': 'checkout_android',
    'dep_type': 'cipd',
  },

  'third_party/androidx/cipd': {
    'packages': [
      {
          'package': 'chromium/third_party/androidx',
          'version': 'VWuP17o8bAsMqJ5b_3fu60qkAIWd905hpPI83flbNrMC',
      },
    ],
    'condition': 'checkout_android and non_git_source',
    'dep_type': 'cipd',
  },

  'third_party/android_build_tools/manifest_merger/cipd': {
      'packages': [
          {
               'package': 'chromium/third_party/android_build_tools/manifest_merger',
               'version': 'yd6w2zQr48NAkrzrzEj2OmMzI-kANsmD6lvKhfXluAsC',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

 'third_party/android_build_tools/aapt2/cipd': {
      'packages': [
          {
              'package': 'chromium/third_party/android_build_tools/aapt2',
              'version': '_lNsOL_GGlXLOIMGtrbMOqNd7TQHabaP1q8SlvUpFbMC',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  'third_party/android_build_tools/bundletool/cipd': {
      'packages': [
          {
               'package': 'chromium/third_party/android_build_tools/bundletool',
               'version': 'tal0sHGlqsDFNFQ5lV1zRomrRs0Ppq6ngUOYbACAAUwC',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  'third_party/android_build_tools/error_prone/cipd': {
      'packages': [
          {
               'package': 'chromium/third_party/android_build_tools/error_prone',
               'version': 'Q3oiuVxuq1jkWhjfnfCSviXK8BbbB9n6_4jz3x_Mo3kC',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  'third_party/android_build_tools/error_prone_javac/cipd': {
      'packages': [
          {
               'package': 'chromium/third_party/android_build_tools/error_prone_javac',
               'version': '7EcHxlEXEaLRWEyHIAxf0ouPjkmN1Od6jkutuo0sfBIC',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  # TODO(webrtc:42223878): This is only needed for //base.
  'third_party/android_build_tools/nullaway/cipd': {
      'packages': [
          {
               'package': 'chromium/third_party/android_build_tools/nullaway',
               'version': '65WJkoinJEXvtu9xwdDNDb3QCbqBAl8FKDpgnXr3iiEC',
          },
      ],
      'condition': 'checkout_android and non_git_source',
      'dep_type': 'cipd',
  },

  'third_party/r8/cipd': {
      'packages': [
          {
              'package': 'chromium/third_party/r8',
              'version': 'DJU_YH-xmuJ4kRnli6eXC-q9Q21-GPFj4YVZyAqKSWoC',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },
  # This duplication is intentional, so we avoid updating the r8.jar used by
  # dexing unless necessary, since each update invalidates all incremental
  # dexing and unnecessarily slows down all bots.
  'third_party/r8/d8/cipd': {
      'packages': [
          {
              'package': 'chromium/third_party/r8',
              'version': 'U3Jf_ewWOZyxa6vyO3wjNIgm8XIz1yFk-4k3-wqDL44C',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  'third_party/jdk/current': {
      'packages': [
          {
              'package': 'chromium/third_party/jdk',
              'version': 'G-WIGWdFIBTPPhv2xPK_lTfI5N7WmfCBh0oTKqX-c5sC',
          },
      ],
      # Needed on Linux for use on chromium_presubmit (for checkstyle).
      'condition': '(checkout_android or checkout_linux) and non_git_source',
      'dep_type': 'cipd',
  },

  # Deprecated - only use for tools which are broken real JDK.
  # Not used by WebRTC. Added for compatibility with Chromium.
  'third_party/jdk11': {
      'packages': [
          {
              'package': 'chromium/third_party/jdk',
              # Do not update this hash - any newer hash will point to JDK17+.
              'version': 'egbcSHbmF1XZQbKxp_PQiGLFWlQK65krTGqQE-Bj4j8C',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  'third_party/kotlin_stdlib/cipd': {
      'packages': [
          {
              'package': 'chromium/third_party/kotlin_stdlib',
              'version': 'z7NenFzvjmGieRhzC5IhUKe-nO3U6xA5VwUilO3GZLgC',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  'third_party/kotlinc/current': {
      'packages': [
          {
              'package': 'chromium/third_party/kotlinc',
              'version': 'VgYl1YO2AM2qu-RYvdko61h4YtNnJeZlGWWppX7vJq8C',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

  'third_party/turbine/cipd': {
      'packages': [
          {
              'package': 'chromium/third_party/turbine',
              'version': 'qNNUfaj7w4cSHTjVawVaZpq0pABVec9LcFebN19wm4EC',
          },
      ],
      'condition': 'checkout_android',
      'dep_type': 'cipd',
  },

 'third_party/colorama/src':
    'https://chromium.googlesource.com/external/colorama.git@3de9f013df4b470069d03d250224062e8cf15c49',

}

hooks = [
  {
    # Ensure that the DEPS'd "depot_tools" has its self-update capability
    # disabled.
    'name': 'disable_depot_tools_selfupdate',
    'pattern': '.',
    'action': [
        'python',
        'third_party/depot_tools/update_depot_tools_toggle.py',
        '--disable',
    ],
  },
  {
    'name': 'sysroot_arm',
    'pattern': '.',
    'condition': 'checkout_linux and checkout_arm',
    'action': ['python', 'build/linux/sysroot_scripts/install-sysroot.py',
               '--arch=arm'],
  },
  {
    'name': 'sysroot_arm64',
    'pattern': '.',
    'condition': 'checkout_linux and checkout_arm64',
    'action': ['python', 'build/linux/sysroot_scripts/install-sysroot.py',
               '--arch=arm64'],
  },
  {
    'name': 'sysroot_x86',
    'pattern': '.',
    'condition': 'checkout_linux and (checkout_x86 or checkout_x64)',
    # TODO(mbonadei): change to --arch=x86.
    'action': ['python', 'build/linux/sysroot_scripts/install-sysroot.py',
               '--arch=i386'],
  },
  {
    'name': 'sysroot_mips',
    'pattern': '.',
    'condition': 'checkout_linux and checkout_mips',
    # TODO(mbonadei): change to --arch=mips.
    'action': ['python', 'build/linux/sysroot_scripts/install-sysroot.py',
               '--arch=mipsel'],
  },
  {
    'name': 'sysroot_x64',
    'pattern': '.',
    'condition': 'checkout_linux and checkout_x64',
    # TODO(mbonadei): change to --arch=x64.
    'action': ['python', 'build/linux/sysroot_scripts/install-sysroot.py',
               '--arch=amd64'],
  },
  {
    # Case-insensitivity for the Win SDK. Must run before win_toolchain below.
    'name': 'ciopfs_linux',
    'pattern': '.',
    'condition': 'checkout_win and host_os == "linux"',
    'action': [ 'python',
                'third_party/depot_tools/download_from_google_storage.py',
                '--no_resume',
                '--no_auth',
                '--bucket', 'chromium-browser-clang/ciopfs',
                '-s', 'build/ciopfs.sha1',
    ]
  },
  {
    # Update the Windows toolchain if necessary. Must run before 'clang' below.
    'name': 'win_toolchain',
    'pattern': '.',
    'condition': 'checkout_win',
    'action': ['python', 'build/vs_toolchain.py', 'update', '--force'],
  },
  {
    # Update the Mac toolchain if necessary.
    'name': 'mac_toolchain',
    'pattern': '.',
    'condition': 'checkout_mac',
    'action': ['python', 'build/mac_toolchain.py'],
  },
  {
    # Note: On Win, this should run after win_toolchain, as it may use it.
    'name': 'clang',
    'pattern': '.',
    'action': ['python', 'tools/clang/scripts/update.py'],
  },

  {                                                                                                 
    # Update LASTCHANGE.                                                                            
    'name': 'lastchange',                                                                           
    'pattern': '.',                                                                                 
    'action': ['python', 'build/util/lastchange.py',                                            
               '-o', 'build/util/LASTCHANGE'],                                                  
  },
]

# Copyright (c) IBM Corporation and Others. All Rights Reserved.
# very loosely based on icu.gyp from Chromium:
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'icu_src_derb': [
      '<(icu_path)/source/tools/genrb/derb.c',
      '<(icu_path)/source/tools/genrb/derb.cpp'
    ],
  },
  'includes': [ '../../icu_config.gypi' ],
  'targets': [
    {
      'target_name': 'icui18n',
      'toolsets': [ 'target', 'host' ],
      'includes': [ 'common.gypi' ],
      'conditions' : [
        ['_toolset=="target"', {
          'type': '<(library)',
          'sources': [
            '<@(icu_src_i18n)'
          ],
          ## if your compiler can dead-strip, these exclusions will
          ## make ZERO difference to binary size.
          ## Made ICU-specific for future-proofing.
          'conditions': [
            [ 'icu_ver_major == 55', { 'sources!': [
              # alphabetic index
              '<(icu_path)/source/i18n/alphaindex.cpp',
              # BOCSU
              # misc
              '<(icu_path)/source/i18n/regexcmp.cpp',
              '<(icu_path)/source/i18n/regexcmp.h',
              '<(icu_path)/source/i18n/regexcst.h',
              '<(icu_path)/source/i18n/regeximp.cpp',
              '<(icu_path)/source/i18n/regeximp.h',
              '<(icu_path)/source/i18n/regexst.cpp',
              '<(icu_path)/source/i18n/regexst.h',
              '<(icu_path)/source/i18n/regextxt.cpp',
              '<(icu_path)/source/i18n/regextxt.h',
              '<(icu_path)/source/i18n/region.cpp',
              '<(icu_path)/source/i18n/region_impl.h',
              '<(icu_path)/source/i18n/reldatefmt.cpp',
              '<(icu_path)/source/i18n/reldatefmt.h'
              '<(icu_path)/source/i18n/scientificformathelper.cpp',
              '<(icu_path)/source/i18n/tmunit.cpp',
              '<(icu_path)/source/i18n/tmutamt.cpp',
              '<(icu_path)/source/i18n/tmutfmt.cpp',
              '<(icu_path)/source/i18n/uregex.cpp',
              '<(icu_path)/source/i18n/uregexc.cpp',
              '<(icu_path)/source/i18n/uregion.cpp',
              '<(icu_path)/source/i18n/uspoof.cpp',
              '<(icu_path)/source/i18n/uspoof_build.cpp',
              '<(icu_path)/source/i18n/uspoof_conf.cpp',
              '<(icu_path)/source/i18n/uspoof_conf.h',
              '<(icu_path)/source/i18n/uspoof_impl.cpp',
              '<(icu_path)/source/i18n/uspoof_impl.h',
              '<(icu_path)/source/i18n/uspoof_wsconf.cpp',
              '<(icu_path)/source/i18n/uspoof_wsconf.h',
            ]}],
            [ 'icu_ver_major == 57', { 'sources!': [

              # alphabetic index
              '<(icu_path)/source/i18n/alphaindex.cpp',
              # BOCSU
              # misc
              '<(icu_path)/source/i18n/regexcmp.cpp',
              '<(icu_path)/source/i18n/regexcmp.h',
              '<(icu_path)/source/i18n/regexcst.h',
              '<(icu_path)/source/i18n/regeximp.cpp',
              '<(icu_path)/source/i18n/regeximp.h',
              '<(icu_path)/source/i18n/regexst.cpp',
              '<(icu_path)/source/i18n/regexst.h',
              '<(icu_path)/source/i18n/regextxt.cpp',
              '<(icu_path)/source/i18n/regextxt.h',
              '<(icu_path)/source/i18n/region.cpp',
              '<(icu_path)/source/i18n/region_impl.h',
              '<(icu_path)/source/i18n/reldatefmt.cpp',
              '<(icu_path)/source/i18n/reldatefmt.h'
              '<(icu_path)/source/i18n/scientificformathelper.cpp',
              '<(icu_path)/source/i18n/tmunit.cpp',
              '<(icu_path)/source/i18n/tmutamt.cpp',
              '<(icu_path)/source/i18n/tmutfmt.cpp',
              '<(icu_path)/source/i18n/uregex.cpp',
              '<(icu_path)/source/i18n/uregexc.cpp',
              '<(icu_path)/source/i18n/uregion.cpp',
              '<(icu_path)/source/i18n/uspoof.cpp',
              '<(icu_path)/source/i18n/uspoof_build.cpp',
              '<(icu_path)/source/i18n/uspoof_conf.cpp',
              '<(icu_path)/source/i18n/uspoof_conf.h',
              '<(icu_path)/source/i18n/uspoof_impl.cpp',
              '<(icu_path)/source/i18n/uspoof_impl.h',
              '<(icu_path)/source/i18n/uspoof_wsconf.cpp',
              '<(icu_path)/source/i18n/uspoof_wsconf.h',
            ]}],
            ],
          'include_dirs': [
            '<(icu_path)/source/i18n',
          ],
          'defines': [
            'U_I18N_IMPLEMENTATION=1',
          ],
          'dependencies': [ 'icuucx', ],
          'direct_dependent_settings': {
            'include_dirs': [
              '<(icu_path)/source/i18n',
            ],
          },
          'export_dependent_settings': [ 'icuucx', ],
        }],
        ['_toolset=="host"', {
          'type': 'none',
          'dependencies': [ 'icutools' ],
          'export_dependent_settings': [ 'icutools' ],
        }],
      ],
    }, # icui18n
    # This exports actual ICU data
    {
      'target_name': 'icudata',
      'type': '<(library)',
      'toolsets': [ 'target' ],
      'includes': [ 'common.gypi' ],
      'conditions': [
        [ 'OS == "win"', {
          'conditions': [
            [ 'icu_small == "false"', { # and OS=win
              # full data - just build the full data file, then we are done.
              'sources': [ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major)<(icu_endianness)_dat.obj' ],
              'dependencies': [ 'genccode#host' ],
              'actions': [
                {
                  'action_name': 'icudata',
                  'msvs_quote_cmd': 0,
                  'inputs': [ '<(icu_data_in)' ],
                  'outputs': [ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major)<(icu_endianness)_dat.obj' ],
                  'action': [ '<(PRODUCT_DIR)/genccode',
                              '-o',
                              '-d', '<(SHARED_INTERMEDIATE_DIR)',
                              '-n', 'icudata',
                              '-e', 'icudt<(icu_ver_major)',
                              '<@(_inputs)' ],
                },
              ],
            }, { # icu_small == TRUE and OS == win
              # link against stub data primarily
              # then, use icupkg and genccode to rebuild data
              'dependencies': [ 'icustubdata', 'genccode#host', 'icupkg#host', 'genrb#host', 'iculslocs#host' ],
              'export_dependent_settings': [ 'icustubdata' ],
              'actions': [
                {
                  # trim down ICU
                  'action_name': 'icutrim',
                  'msvs_quote_cmd': 0,
                  'inputs': [ '<(icu_data_in)', 'icu_small.json' ],
                  'outputs': [ '<(SHARED_INTERMEDIATE_DIR)/icutmp/icudt<(icu_ver_major)<(icu_endianness).dat' ],
                  'action': [ 'python',
                              'icutrim.py',
                              '-P', '<(PRODUCT_DIR)/.', # '.' suffix is a workaround against GYP assumptions :(
                              '-D', '<(icu_data_in)',
                              '--delete-tmp',
                              '-T', '<(SHARED_INTERMEDIATE_DIR)/icutmp',
                              '-F', 'icu_small.json',
                              '-O', 'icudt<(icu_ver_major)<(icu_endianness).dat',
                              '-v',
                              '-L', '<(icu_locales)'],
                },
                {
                  # build final .dat -> .obj
                  'action_name': 'genccode',
                  'msvs_quote_cmd': 0,
                  'inputs': [ '<(SHARED_INTERMEDIATE_DIR)/icutmp/icudt<(icu_ver_major)<(icu_endianness).dat' ],
                  'outputs': [ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major)<(icu_endianness)_dat.obj' ],
                  'action': [ '<(PRODUCT_DIR)/genccode',
                              '-o',
                              '-d', '<(SHARED_INTERMEDIATE_DIR)/',
                              '-n', 'icudata',
                              '-e', 'icusmdt<(icu_ver_major)',
                              '<@(_inputs)' ],
                },
              ],
              # This file contains the small ICU data.
              'sources': [ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major)<(icu_endianness)_dat.obj' ],
            } ] ], #end of OS==win and icu_small == true
        }, { # OS != win
          'conditions': [
            [ 'icu_small == "false"', {
              # full data - just build the full data file, then we are done.
              'sources': [ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major)_dat.c' ],
              'dependencies': [ 'genccode#host', 'icupkg#host', ],
              'include_dirs': [
                '<(icu_path)/source/common',
              ],
              'actions': [
                {
                   # Swap endianness (if needed), or at least copy the file
                   'action_name': 'icupkg',
                   'inputs': [ '<(icu_data_in)' ],
                   'outputs':[ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major)<(icu_endianness).dat' ],
                   'action': [ '<(PRODUCT_DIR)/icupkg',
                               '-t<(icu_endianness)',
                               '<@(_inputs)',
                               '<@(_outputs)',
                             ],
                },
                {
                   # Rename without the endianness marker
                   'action_name': 'copy',
                   'inputs': [ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major)<(icu_endianness).dat' ],
                   'outputs':[ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major).dat' ],
                   'action': [ 'cp',
                               '<@(_inputs)',
                               '<@(_outputs)',
                             ],
                },
                {
                  'action_name': 'icudata',
                  'inputs': [ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major).dat' ],
                  'outputs':[ '<(SHARED_INTERMEDIATE_DIR)/icudt<(icu_ver_major)_dat.c' ],
                  'action': [ '<(PRODUCT_DIR)/genccode',
                              '-e', 'icudt<(icu_ver_major)',
                              '-d', '<(SHARED_INTERMEDIATE_DIR)',
                              '-f', 'icudt<(icu_ver_major)_dat',
                              '<@(_inputs)' ],
                },
              ], # end actions
            }, { # icu_small == true ( and OS != win )
              # link against stub data (as primary data)
              # then, use icupkg and genccode to rebuild small data
              'dependencies': [ 'icustubdata', 'genccode#host', 'icupkg#host', 'genrb#host', 'iculslocs#host', ],
              'export_dependent_settings': [ 'icustubdata' ],
              'actions': [
                {
                  # trim down ICU
                  'action_name': 'icutrim',
                  'inputs': [ '<(icu_data_in)', 'icu_small.json' ],
                  'outputs': [ '<(SHARED_INTERMEDIATE_DIR)/icutmp/icudt<(icu_ver_major)<(icu_endianness).dat' ],
                  'action': [ 'python',
                              'icutrim.py',
                              '-P', '<(PRODUCT_DIR)',
                              '-D', '<(icu_data_in)',
                              '--delete-tmp',
                              '-T', '<(SHARED_INTERMEDIATE_DIR)/icutmp',
                              '-F', 'icu_small.json',
                              '-O', 'icudt<(icu_ver_major)<(icu_endianness).dat',
                              '-v',
                              '-L', '<(icu_locales)'],
                }, {
                  # rename to get the final entrypoint name right
                   'action_name': 'rename',
                   'inputs': [ '<(SHARED_INTERMEDIATE_DIR)/icutmp/icudt<(icu_ver_major)<(icu_endianness).dat' ],
                   'outputs': [ '<(SHARED_INTERMEDIATE_DIR)/icutmp/icusmdt<(icu_ver_major).dat' ],
                   'action': [ 'cp',
                               '<@(_inputs)',
                               '<@(_outputs)',
                             ],
                }, {
                  # build final .dat -> .obj
                  'action_name': 'genccode',
                  'inputs': [ '<(SHARED_INTERMEDIATE_DIR)/icutmp/icusmdt<(icu_ver_major).dat' ],
                  'outputs': [ '<(SHARED_INTERMEDIATE_DIR)/icusmdt<(icu_ver_major)_dat.c' ],
                  'action': [ '<(PRODUCT_DIR)/genccode',
                              '-d', '<(SHARED_INTERMEDIATE_DIR)',
                              '<@(_inputs)' ],
                },
              ],
              # This file contains the small ICU data
              'sources': [ '<(SHARED_INTERMEDIATE_DIR)/icusmdt<(icu_ver_major)_dat.c' ],
              # for umachine.h
              'include_dirs': [
                '<(icu_path)/source/common',
              ],
            }]], # end icu_small == true
        }]], # end OS != win
    }, # end icudata
    # icustubdata is a tiny (~1k) symbol with no ICU data in it.
    # tools must link against it as they are generating the full data.
    {
      'target_name': 'icustubdata',
      'type': '<(library)',
      'toolsets': [ 'target' ],
      'includes': [ 'common.gypi' ],
      'sources': [
        '<@(icu_src_stubdata)'
      ],
      'include_dirs': [
        '<(icu_path)/source/common',
      ],
    }, # icudata
    # this target is for v8 consumption.
    # it is icuuc + stubdata
    # it is only built for target
    {
      'target_name': 'icuuc',
      'type': 'none',
      'toolsets': [ 'target', 'host' ],
      'includes': [ 'common.gypi' ],
      'conditions' : [
        ['_toolset=="host"', {
          'dependencies': [ 'icutools' ],
          'export_dependent_settings': [ 'icutools' ],
        }],
        ['_toolset=="target"', {
          'dependencies': [ 'icuucx', 'icudata' ],
          'export_dependent_settings': [ 'icuucx', 'icudata' ],
        }],
      ],
    }, # icuuc
    # This is the 'real' icuuc.
    {
      'target_name': 'icuucx',
      'type': '<(library)',
      'toolsets': [ 'target' ],
      'includes': [ 'common.gypi' ],
      'sources': [
        '<@(icu_src_common)',
      ],
          ## if your compiler can dead-strip, this will
          ## make ZERO difference to binary size.
          ## Made ICU-specific for future-proofing.
      'conditions': [
        [ 'icu_ver_major == 55', { 'sources!': [

          # bidi- not needed (yet!)
          '<(icu_path)/source/common/ubidi.c',
          '<(icu_path)/source/common/ubidiimp.h',
          '<(icu_path)/source/common/ubidiln.c',
          '<(icu_path)/source/common/ubidiwrt.c',
          #'<(icu_path)/source/common/ubidi_props.c',
          #'<(icu_path)/source/common/ubidi_props.h',
          #'<(icu_path)/source/common/ubidi_props_data.h',
          # and the callers
          '<(icu_path)/source/common/ushape.cpp',
        ]}],
        [ 'icu_ver_major == 57', { 'sources!': [
          # work around http://bugs.icu-project.org/trac/ticket/12451
          # (benign afterwards)
          '<(icu_path)/source/common/cstr.cpp',

          # bidi- not needed (yet!)
          '<(icu_path)/source/common/ubidi.c',
          '<(icu_path)/source/common/ubidiimp.h',
          '<(icu_path)/source/common/ubidiln.c',
          '<(icu_path)/source/common/ubidiwrt.c',
          #'<(icu_path)/source/common/ubidi_props.c',
          #'<(icu_path)/source/common/ubidi_props.h',
          #'<(icu_path)/source/common/ubidi_props_data.h',
          # and the callers
          '<(icu_path)/source/common/ushape.cpp',
        ]}],
        [ 'OS == "solaris"', { 'defines': [
          '_XOPEN_SOURCE_EXTENDED=0',
        ]}],
      ],
      'include_dirs': [
        '<(icu_path)/source/common',
      ],
      'defines': [
        'U_COMMON_IMPLEMENTATION=1',
      ],
      'cflags_c': ['-std=c99'],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(icu_path)/source/common',
        ],
        'conditions': [
          [ 'OS=="win"', {
            'link_settings': {
              'libraries': [ '-lAdvAPI32.lib', '-lUser32.lib' ],
            },
          }],
        ],
      },
    }, # 'icuucx'
    # tools library. This builds all of ICU together.
    {
      'target_name': 'icutools',
      'type': '<(library)',
      'toolsets': [ 'host' ],
      'includes': [ 'common.gypi' ],
      # warning C4477: 'sprintf' : format string '%lu' requires an argument of type 'unsigned long'
      'msvs_disabled_warnings': [4477],
      'sources': [
        '<@(icu_src_tools)',
        '<@(icu_src_common)',
        '<@(icu_src_i18n)',
        '<@(icu_src_stubdata)',
      ],
      'sources!': [
        '<(icu_path)/source/tools/toolutil/udbgutil.cpp',
        '<(icu_path)/source/tools/toolutil/udbgutil.h',
        '<(icu_path)/source/tools/toolutil/dbgutil.cpp',
        '<(icu_path)/source/tools/toolutil/dbgutil.h',
      ],
      'include_dirs': [
        '<(icu_path)/source/common',
        '<(icu_path)/source/i18n',
        '<(icu_path)/source/tools/toolutil',
      ],
      'defines': [
        'U_COMMON_IMPLEMENTATION=1',
        'U_I18N_IMPLEMENTATION=1',
        'U_IO_IMPLEMENTATION=1',
        'U_TOOLUTIL_IMPLEMENTATION=1',
        #'DEBUG=0', # http://bugs.icu-project.org/trac/ticket/10977
      ],
      'cflags_c': ['-std=c99'],
      'conditions': [
        ['OS == "solaris"', {
          'defines': [ '_XOPEN_SOURCE_EXTENDED=0' ]
        }]
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(icu_path)/source/common',
          '<(icu_path)/source/i18n',
          '<(icu_path)/source/tools/toolutil',
        ],
        'conditions': [
          [ 'OS=="win"', {
            'link_settings': {
              'libraries': [ '-lAdvAPI32.lib', '-lUser32.lib' ],
            },
          }],
        ],
      },
    }, # icutools
    # This tool is needed to rebuild .res files from .txt,
    # or to build index (res_index.txt) files for small-icu
    {
      'target_name': 'genrb',
      'type': 'executable',
      'toolsets': [ 'host' ],
      'includes': [ 'common.gypi' ],
      'dependencies': [ 'icutools', ],
      'sources': [
        '<@(icu_src_genrb)'
      ],
      # derb is a separate executable
      # (which is not currently built)
      'sources!': [
        '<@(icu_src_derb)',
        'no-op.cc',
      ],
    }, # genrb
    # This tool is used to rebuild res_index.res manifests
    {
      'target_name': 'iculslocs',
      'toolsets': [ 'host' ],
      'type': 'executable',
      'includes': [ 'common.gypi' ],
      'dependencies': [ 'icutools', ],
      'sources': [
        'iculslocs.cc',
        'no-op.cc',
      ],
    }, # iculslocs
    # This tool is used to package, unpackage, repackage .dat files
    # and convert endianesses
    {
      'target_name': 'icupkg',
      'toolsets': [ 'host' ],
      'type': 'executable',
      'includes': [ 'common.gypi' ],
      'dependencies': [ 'icutools', ],
      'sources': [
        '<@(icu_src_icupkg)',
        'no-op.cc',
      ],
    }, # icupkg
    # this is used to convert .dat directly into .obj
    {
      'target_name': 'genccode',
      'type': 'executable',
      'toolsets': [ 'host' ],
      'includes': [ 'common.gypi' ],
      'dependencies': [ 'icutools', ],
      'sources': [
        '<@(icu_src_genccode)',
        'no-op.cc',
      ],
    }, # genccode
  ],
}


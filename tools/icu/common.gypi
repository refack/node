{
  'configurations': {
    'Debug': {
      'cflags': [
        '-Wno-deprecated-declarations',
        '-Wno-strict-aliasing'
      ],
      'cflags_cc!': [ '-fno-rtti' ],
      'cflags_cc': [ '-frtti' ],
      'xcode_settings': {
        'GCC_ENABLE_CPP_RTTI': 'YES',
        'WARNING_CFLAGS': [
          '-Wno-deprecated-declarations',
          '-Wno-strict-aliasing'
        ],
      },
      'msvs_settings': {
        'VCCLCompilerTool': {
          'RuntimeTypeInfo': 'true',
          'ExceptionHandling': '1',
          'AdditionalOptions': [ '/source-charset:utf-8' ],
        },
      },
      'defines': [
        'U_ATTRIBUTE_DEPRECATED=',
        '_CRT_SECURE_NO_DEPRECATE=',
        'U_STATIC_IMPLEMENTATION=1',
        'UCONFIG_NO_SERVICE=1',
        'U_ENABLE_DYLOAD=0',
        'U_STATIC_IMPLEMENTATION=1',
        'U_HAVE_STD_STRING=1',
        # TODO(srl295): reenable following pending
        # https://code.google.com/p/v8/issues/detail?id=3345
        # (saves some space)
        'UCONFIG_NO_BREAK_ITERATION=0',
      ],
    },
    'Release': {
      'cflags': [
        '-Wno-deprecated-declarations',
        '-Wno-strict-aliasing'
      ],
      'cflags_cc!': [ '-fno-rtti' ],
      'cflags_cc': [ '-frtti' ],
      'xcode_settings': {
        'GCC_ENABLE_CPP_RTTI': 'YES',
        'WARNING_CFLAGS': [
          '-Wno-deprecated-declarations',
          '-Wno-strict-aliasing'
        ],
      },
      'msvs_settings': {
        'VCCLCompilerTool': {
          'RuntimeTypeInfo': 'true',
          'ExceptionHandling': '1',
          'AdditionalOptions': [ '/source-charset:utf-8' ],
        },
      },
      'defines': [
        'U_ATTRIBUTE_DEPRECATED=',
        '_CRT_SECURE_NO_DEPRECATE=',
        'U_STATIC_IMPLEMENTATION=1',
        'UCONFIG_NO_SERVICE=1',
        'U_ENABLE_DYLOAD=0',
        'U_STATIC_IMPLEMENTATION=1',
        'U_HAVE_STD_STRING=1',
        # TODO(srl295): reenable following pending
        # https://code.google.com/p/v8/issues/detail?id=3345
        # (saves some space)
        'UCONFIG_NO_BREAK_ITERATION=0',
      ],
    },
  },
}

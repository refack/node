{
  'variables': {
    'protocol_tool_path': '../../deps/v8/third_party/inspector_protocol',
  },
  'targets': [
    {
      'target_name': 'inspector',
      'type': '<(library)',
      'defines': [
        'HAVE_INSPECTOR=1',
        'NODE_WANT_INTERNALS=1',
      ],
      'direct_dependent_settings' : {
        'defines': [
          'HAVE_INSPECTOR=1',
        ],
      },
      'include_dirs': [
        '..',
        '<(SHARED_INTERMEDIATE_DIR)',
        '../../tools/msvs/genfiles',
        '../../deps/v8/include',
        '../../deps/icu-small/source/i18n',
        '../../deps/icu-small/source/common',
        '../../deps/zlib',
        '../../deps/http_parser',
        '../../deps/cares/include',
        '../../deps/uv/include',
        '../../deps/nghttp2/lib/includes',
        '../../deps/openssl/openssl/include',
      ],
      'sources': [
        'inspector_agent.cc',
        'inspector_io.cc',
        'inspector_js_api.cc',
        'inspector_socket.cc',
        'inspector_socket_server.cc',
        'main_thread_interface.cc',
        'node_string.cc',
        'tracing_agent.cc',
        'inspector_agent.h',
        'inspector_io.h',
        'inspector_socket.h',
        'inspector_socket_server.h',
        'main_thread_interface.h',
        'node_string.h',
        'tracing_agent.h',
        'node_protocol/Forward.h',
        'node_protocol/Protocol.cpp',
        'node_protocol/Protocol.h',
        'node_protocol/NodeTracing.cpp',
        'node_protocol/NodeTracing.h',
      ],
      'dependencies': [
        'generate_concatenated_protocol',
      ],
    },
    {
      'target_name': 'generate_concatenated_protocol',
      'type': 'none',
      'inputs': [
        '../../deps/v8/src/inspector/js_protocol.pdl',
        'node_protocol.json',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/v8_inspector_protocol_json.h',
      ],
      'actions': [
        {
          'action_name': 'v8_inspector_convert_protocol_to_json',
          'inputs': [
            '../../deps/v8/src/inspector/js_protocol.pdl',
          ],
          'outputs': [
            '<(SHARED_INTERMEDIATE_DIR)/js_protocol.json',
          ],
          'action': [
            'python',
            '<(protocol_tool_path)/ConvertProtocolToJSON.py',
            '<@(_inputs)',
            '<@(_outputs)',
          ],
        },
        {
          'action_name': 'concatenate_protocols',
          'inputs': [
            '<(SHARED_INTERMEDIATE_DIR)/js_protocol.json',
            'node_protocol.json',
          ],
          'outputs': [
            '<(SHARED_INTERMEDIATE_DIR)/concatenated_protocol.json',
          ],
          'action': [
            'python',
            '<(protocol_tool_path)/ConcatenateProtocols.py',
            '<@(_inputs)',
            '<@(_outputs)',
          ],
        },
        {
          'action_name': 'v8_inspector_compress_protocol_json',
          'process_outputs_as_sources': 1,
          'inputs': [
            '<(SHARED_INTERMEDIATE_DIR)/concatenated_protocol.json',
          ],
          'outputs': [
            '<(SHARED_INTERMEDIATE_DIR)/v8_inspector_protocol_json.h',
          ],
          'action': [
            'python',
            '../../tools/compress_json.py',
            '<@(_inputs)',
            '<@(_outputs)',
          ],
        },
      ],
    },
  ]
}
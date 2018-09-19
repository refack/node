{
  'variables': {
    'protocol_tool_path': '../../tools/inspector_protocol',
    'node_inspector_path': '../../src/inspector',
    'node_inspector_generated_sources': [
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/Forward.h',
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/Protocol.cpp',
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/Protocol.h',
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/NodeTracing.cpp',
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/NodeTracing.h',
    ],
    'node_protocol_files': [
      '<(protocol_tool_path)/lib/Allocator_h.template',
      '<(protocol_tool_path)/lib/Array_h.template',
      '<(protocol_tool_path)/lib/Collections_h.template',
      '<(protocol_tool_path)/lib/DispatcherBase_cpp.template',
      '<(protocol_tool_path)/lib/DispatcherBase_h.template',
      '<(protocol_tool_path)/lib/ErrorSupport_cpp.template',
      '<(protocol_tool_path)/lib/ErrorSupport_h.template',
      '<(protocol_tool_path)/lib/Forward_h.template',
      '<(protocol_tool_path)/lib/FrontendChannel_h.template',
      '<(protocol_tool_path)/lib/Maybe_h.template',
      '<(protocol_tool_path)/lib/Object_cpp.template',
      '<(protocol_tool_path)/lib/Object_h.template',
      '<(protocol_tool_path)/lib/Parser_cpp.template',
      '<(protocol_tool_path)/lib/Parser_h.template',
      '<(protocol_tool_path)/lib/Protocol_cpp.template',
      '<(protocol_tool_path)/lib/ValueConversions_h.template',
      '<(protocol_tool_path)/lib/Values_cpp.template',
      '<(protocol_tool_path)/lib/Values_h.template',
      '<(protocol_tool_path)/templates/Exported_h.template',
      '<(protocol_tool_path)/templates/Imported_h.template',
      '<(protocol_tool_path)/templates/TypeBuilder_cpp.template',
      '<(protocol_tool_path)/templates/TypeBuilder_h.template',
      '<(protocol_tool_path)/CodeGenerator.py',
    ]
  },
  'defines': [
    'HAVE_INSPECTOR=1',
  ],
  'sources': [
    '../../src/inspector_agent.cc',
    '../../src/inspector_io.cc',
    '../../src/inspector_agent.h',
    '../../src/inspector_io.h',
    '../../src/inspector_js_api.cc',
    '../../src/inspector_socket.cc',
    '../../src/inspector_socket.h',
    '../../src/inspector_socket_server.cc',
    '../../src/inspector_socket_server.h',
    '../../src/inspector/main_thread_interface.cc',
    '../../src/inspector/main_thread_interface.h',
    '../../src/inspector/node_string.cc',
    '../../src/inspector/node_string.h',
    '../../src/inspector/tracing_agent.cc',
    '../../src/inspector/tracing_agent.h',
    '<@(node_inspector_generated_sources)'
  ],
  'include_dirs': [
    '<(SHARED_INTERMEDIATE_DIR)/include', # for inspector
    '<(SHARED_INTERMEDIATE_DIR)',
    '<(SHARED_INTERMEDIATE_DIR)/src', # for inspector
  ],
  'actions': [
    {
      'action_name': 'convert_node_protocol_to_json',
      'inputs': [
        '<(SHARED_INTERMEDIATE_DIR)/node_protocol.pdl',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/node_protocol.json',
      ],
      'action': [
        'python',
        'tools/inspector_protocol/ConvertProtocolToJSON.py',
        '<@(_inputs)',
        '<@(_outputs)',
      ],
    },
    {
      'action_name': 'node_protocol_generated_sources',
      'inputs': [
        '<(SHARED_INTERMEDIATE_DIR)/node_protocol_config.json',
        '<(SHARED_INTERMEDIATE_DIR)/node_protocol.json',
        '<@(node_protocol_files)',
      ],
      'outputs': [
        '<@(node_inspector_generated_sources)',
      ],
      'action': [
        'python',
        'tools/inspector_protocol/CodeGenerator.py',
        '--jinja_dir', '<@(protocol_tool_path)/..',
        '--output_base', '<(SHARED_INTERMEDIATE_DIR)/src/',
        '--config', '<(SHARED_INTERMEDIATE_DIR)/node_protocol_config.json',
      ],
      'message': 'Generating node protocol sources from protocol json',
    },
    {
      'action_name': 'v8_inspector_convert_protocol_to_json',
      'inputs': [
        '<(SHARED_INTERMEDIATE_DIR)/js_protocol.pdl',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/js_protocol.json',
      ],
      'action': [
        'python',
        'tools/inspector_protocol/ConvertProtocolToJSON.py',
        '<@(_inputs)',
        '<@(_outputs)',
      ],
    },
    {
      'action_name': 'concatenate_protocols',
      'inputs': [
        '<(SHARED_INTERMEDIATE_DIR)/js_protocol.json',
        '<(SHARED_INTERMEDIATE_DIR)/node_protocol.json',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/concatenated_protocol.json',
      ],
      'action': [
        'python',
        'tools/inspector_protocol/ConcatenateProtocols.py',
        '<@(_inputs)',
        '<@(_outputs)',
      ],
    },
    {
      'action_name': 'v8_inspector_compress_protocol_json',
      'inputs': [
        '<(SHARED_INTERMEDIATE_DIR)/concatenated_protocol.json',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/v8_inspector_protocol_json.h',
      ],
      'action': [
        'python',
        'tools/compress_json.py',
        '<@(_inputs)',
        '<@(_outputs)',
      ],
    },
  ],
}
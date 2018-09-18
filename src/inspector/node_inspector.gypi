{
  'defines': [
    'HAVE_INSPECTOR=1',
  ],
  'sources': [
    '<(DEPTH)/src/inspector_agent.cc',
    '<(DEPTH)/src/inspector_io.cc',
    '<(DEPTH)/srd/inspector_agent.h',
    '<(DEPTH)/srd/inspector_io.h',
    '<(DEPTH)/srd/inspector_js_api.cc',
    '<(DEPTH)/srd/inspector_socket.cc',
    '<(DEPTH)/srd/inspector_socket.h',
    '<(DEPTH)/srd/inspector_socket_server.cc',
    '<(DEPTH)/srd/inspector_socket_server.h',
    '<(DEPTH)/srd/inspector/main_thread_interface.cc',
    '<(DEPTH)/srd/inspector/main_thread_interface.h',
    '<(DEPTH)/srd/inspector/node_string.cc',
    '<(DEPTH)/srd/inspector/node_string.h',
    '<(DEPTH)/srd/inspector/tracing_agent.cc',
    '<(DEPTH)/srd/inspector/tracing_agent.h',
    '<@(node_inspector_generated_sources)'
  ],
  'include_dirs': [
    '<(SHARED_INTERMEDIATE_DIR)/include', # for inspector
    '<(SHARED_INTERMEDIATE_DIR)',
    '<(SHARED_INTERMEDIATE_DIR)/src', # for inspector
  ],
  'variables': {
    'protocol_path': '<(DEPTH)/tools/inspector_protocol',
    'node_inspector_path': '<(DEPTH)/srd/inspector',
    'node_inspector_generated_sources': [
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/Forward.h',
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/Protocol.cpp',
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/Protocol.h',
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/NodeTracing.cpp',
      '<(SHARED_INTERMEDIATE_DIR)/src/node/inspector/protocol/NodeTracing.h',
    ],
    'node_protocol_files': [
      '<(protocol_path)/lib/Allocator_h.template',
      '<(protocol_path)/lib/Array_h.template',
      '<(protocol_path)/lib/Collections_h.template',
      '<(protocol_path)/lib/DispatcherBase_cpp.template',
      '<(protocol_path)/lib/DispatcherBase_h.template',
      '<(protocol_path)/lib/ErrorSupport_cpp.template',
      '<(protocol_path)/lib/ErrorSupport_h.template',
      '<(protocol_path)/lib/Forward_h.template',
      '<(protocol_path)/lib/FrontendChannel_h.template',
      '<(protocol_path)/lib/Maybe_h.template',
      '<(protocol_path)/lib/Object_cpp.template',
      '<(protocol_path)/lib/Object_h.template',
      '<(protocol_path)/lib/Parser_cpp.template',
      '<(protocol_path)/lib/Parser_h.template',
      '<(protocol_path)/lib/Protocol_cpp.template',
      '<(protocol_path)/lib/ValueConversions_h.template',
      '<(protocol_path)/lib/Values_cpp.template',
      '<(protocol_path)/lib/Values_h.template',
      '<(protocol_path)/templates/Exported_h.template',
      '<(protocol_path)/templates/Imported_h.template',
      '<(protocol_path)/templates/TypeBuilder_cpp.template',
      '<(protocol_path)/templates/TypeBuilder_h.template',
      '<(protocol_path)/CodeGenerator.py',
    ]
  },
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
        '<(DEPTH)/tools/inspector_protocol/ConvertProtocolToJSON.py',
        '<@(_inputs)',
        '<@(_outputs)',
      ],
    },
    {
      'action_name': 'node_protocol_generated_sources',
      'process_outputs_as_sources': 0,
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
        '<(protocol_path)/CodeGenerator.py',
        '--jinja_dir', '<@(protocol_path)/..',
        '--output_base', '<(SHARED_INTERMEDIATE_DIR)/src/',
        '--config', '<(SHARED_INTERMEDIATE_DIR)/node_protocol_config.json',
      ],
      'message': 'Generating node protocol sources from protocol json',
    },
    {
      'action_name': 'v8_inspector_convert_protocol_to_json',
      'process_outputs_as_sources': 0,
      'inputs': [
        '<(SHARED_INTERMEDIATE_DIR)/js_protocol.pdl',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/js_protocol.json',
      ],
      'action': [
        'python',
        '<(protocol_path)/tools/inspector_protocol/ConvertProtocolToJSON.py',
        '<@(_inputs)',
        '<@(_outputs)',
      ],
    },
    {
      'action_name': 'concatenate_protocols',
      'process_outputs_as_sources': 0,
      'inputs': [
        '<(SHARED_INTERMEDIATE_DIR)/js_protocol.json',
        '<(SHARED_INTERMEDIATE_DIR)/node_protocol.json',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/concatenated_protocol.json',
      ],
      'action': [
        'python',
        '<(protocol_path)/tools/inspector_protocol/ConcatenateProtocols.py',
        '<@(_inputs)',
        '<@(_outputs)',
      ],
    },
    {
      'action_name': 'v8_inspector_compress_protocol_json',
      'process_outputs_as_sources': 0,
      'inputs': [
        '<(SHARED_INTERMEDIATE_DIR)/concatenated_protocol.json',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/v8_inspector_protocol_json.h',
      ],
      'action': [
        'python',
        '<(protocol_path)/tools/compress_json.py',
        '<@(_inputs)',
        '<@(_outputs)',
      ],
    },
  ],
}
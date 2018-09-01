{
  'variables': {
    'protocol_tool_path': '../../tools/inspector_protocol',
    'node_inspector_generated_sources': [
      'node_protocol/Forward.h',
      'node_protocol/Protocol.cpp',
      'node_protocol/Protocol.h',
      'node_protocol/NodeTracing.cpp',
      'node_protocol/NodeTracing.h',
    ],
  },
  'targets': [
    {
      'target_name': 'node_protocol_generated_sources',
      'type': 'none',
      'toolsets': ['host'],
      'actions': [
        {
          'action_name': 'convert_node_protocol_to_json',
          'inputs': [
            'node_protocol.pdl',
          ],
          'outputs': [
            'node_protocol.json',
          ],
          'action': [
            'python',
            '<(protocol_tool_path)/ConvertProtocolToJSON.py',
            '<@(_inputs)',
            '<@(_outputs)',
          ],
        },
        {
          'action_name': 'node_protocol_generated_sources',
          'inputs': [
            'node_protocol_config.json',
          ],
          'outputs': [
            '<@(node_inspector_generated_sources)',
          ],
          'action': [
            'python',
            '<(protocol_tool_path)/CodeGenerator.py',
            '--jinja_dir', '<@(protocol_tool_path)/..',
            '--output_base', '.',
            '--config', '<@(_inputs)',
          ],
          'message': 'Generating node protocol sources from protocol json',
        },
      ]
    },
    {
      'target_name': 'generate_concatenated_inspector_protocol',
      'type': 'none',
      'inputs': [
        'deps/v8/src/inspector/js_protocol.pdl',
        '<@(node_inspector_generated_sources)',
      ],
      'outputs': [
        '<(SHARED_INTERMEDIATE_DIR)/node_protocol/v8_inspector_protocol_json.h',
      ],
      'actions': [
        {
          'action_name': 'v8_inspector_convert_protocol_to_json',
          'inputs': [
            'deps/v8/src/inspector/js_protocol.pdl',
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
            '<(SHARED_INTERMEDIATE_DIR)/node_protocol/v8_inspector_protocol_json.h',
          ],
          'action': [
            'python',
            'tools/compress_json.py',
            '<@(_inputs)',
            '<@(_outputs)',
          ],
        },
      ],
    },
  ]
}
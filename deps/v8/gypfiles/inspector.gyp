# Copyright 2016 the V8 project authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'protocol_path': '../third_party/inspector_protocol',
    'inspector_path': '../src/inspector',
  },
  'includes': [
    'inspector.gypi',
    '../third_party/inspector_protocol/inspector_protocol.gypi',
  ],
  'targets': [
    { 'target_name': 'inspector_injected_script',
      'type': 'none',
      'actions': [
        {
          'action_name': 'protocol_compatibility',
          'inputs': [
            '<(inspector_path)/js_protocol.json',
          ],
          'outputs': [
            '<@(SHARED_INTERMEDIATE_DIR)/src/js_protocol.stamp',
          ],
          'action': [
            'python',
            '<(protocol_path)/CheckProtocolCompatibility.py',
            '--stamp', '<@(_outputs)',
            '<(inspector_path)/js_protocol.json',
          ],
          'message': 'Checking inspector protocol compatibility',
        },
        {
          'action_name': 'protocol_generated_sources',
          'inputs': [
            '<(inspector_path)/js_protocol.json',
            '<(inspector_path)/inspector_protocol_config.json',
            '<@(inspector_protocol_files)',
          ],
          'outputs': [
            '<@(inspector_generated_sources)',
          ],
          'action': [
            'python',
            '<(protocol_path)/CodeGenerator.py',
            '--jinja_dir', '../third_party',
            '--output_base', '<(SHARED_INTERMEDIATE_DIR)/src/inspector',
            '--config', '<(inspector_path)/inspector_protocol_config.json',
          ],
          'message': 'Generating inspector protocol sources from protocol json',
        },
        {
          'action_name': 'convert_js_to_cpp_char_array',
          'inputs': [
            '<(inspector_path)/build/xxd.py',
            '<(inspector_injected_script_source)',
          ],
          'outputs': [
            '<(inspector_generated_injected_script)',
          ],
          'action': [
            'python',
            '<(inspector_path)/build/xxd.py',
            'InjectedScriptSource_js',
            '<(inspector_path)/injected-script-source.js',
            '<@(_outputs)'
          ],
        },
      ]
    },
  ],
}

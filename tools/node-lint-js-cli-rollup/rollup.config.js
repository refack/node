'use strict'

const resolve = require('rollup-plugin-node-resolve')
const commonjs = require('rollup-plugin-commonjs')
const json = require('rollup-plugin-json')

module.exports = {
  input: 'src/cli-entry.js',
  output: {
    file: 'dist/lint-js.js',
    format: 'cjs',
    sourcemap: true
  },
  external: [
    'stream',
    'path',
    'module',
    'util',
    'tty',
    'os',
    'fs',
    'events',
    'assert',
    'constants'
  ],
  plugins: [
    {
      name: 'brute-replace',
      transform (code, id) {
        const normID = id.replace(__dirname, '').replace(/\\+/g, '/')
        if (normID === '/node_modules/circular-json/build/circular-json.node.js') {
          code = code.replace(/^this/gm, 'module.exports')
        }
        else if (normID === '/node_modules/unified-args/lib/options.js') {
          code = code.replace('\'./schema\'', '\'./schema.json\'')
        }
        return {
          code: code,
          map: null
        }
      }
    },
    json({
      preferConst: true
    }),
    commonjs(),
    resolve({
      customResolveOptions: {
        moduleDirectory: 'node_modules'
      }
    }),
  ]
}

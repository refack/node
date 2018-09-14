'use strict'
const util = require('util')
const vm = require('vm')
const fs = require('fs')
const { resolve, join } = require('path')
const EventEmitter = require('events');
const testCommon = require('../test/common');

const TOO_HARD = [
  'test-async-wrap-promise-after-enabled.js',
  'test-async-wrap-pop-id-during-load.js',
  'test-async-wrap-trigger-id.js',
  'test-async-wrap-destroyid.js',
  'test-bootstrap-modules.js',
  'test-buffer-alloc.js',
  'test-buffer-bindingobj-no-zerofill.js',
  'test-buffer-iterator.js',
  'test-buffer-constructor-node-modules-paths.js',
  'test-buffer-prototype-inspect.js',
  'test-buffer-zero-fill-cli.js',
  'test-child-process-bad-stdio.js',
  'test-child-process-custom-fds.js',
  'test-child-process-default-options.js',
  'test-child-process-detached.js',
  'test-child-process-env.js',
  'test-child-process-exec-env.js',
  'test-child-process-exec-timeout.js',
  'test-child-process-exec-kill-throws.js',
  'test-child-process-fork-closed-channel-segfault.js',
  'test-assert-async.js',
]
const TOO_SLOW = [
  'test-buffer-indexof.js'
]
const errSemntinal = new Error('ggg');
class FakeProc extends EventEmitter {
  constructor (filename) {
    super();
    this.argv = [process.argv[0], filename];
    this.execPath = process.execPath;
    this.stdout = process.stdout;
    this.binding = process.binding;
    this.nextTick = process.nextTick;
    this.emitWarning = () => {};
    this.exit = () => { throw errSemntinal };
    this.env = Object.assign({}, process.env);
    this.cwd = process.cwd;
  }
}

testCommon.skip = () => { throw errSemntinal };

class Global extends Object {
  static get name() { return 'global' }
}

let i = 1
function runTest (file) {
  const filename = resolve(file)
  console.log(`${++i} at (${filename}:1)`);
  const code = fs.readFileSync(filename, {encoding: 'utf8'})
    .replace(/\.\.\/common/g, '../test/common')
  const sandbox = {
    __filename: filename,
    require,
    ArrayBuffer,
    Error,
    TypeError,
    RangeError,
    process: new FakeProc(filename),
    global: new Global(),
    Buffer,
    setImmediate,
  }
  if (file.endsWith('test-assert-checktag.js')) {
    sandbox.global = global;
    sandbox.process = process;
  }
//  global.__proto__ = { get name() { return 'global'; } };
  try {
    vm.runInNewContext(code, sandbox, {filename})
  } catch (e) {
    if (e !== errSemntinal) throw e;
  }
  sandbox.process.emit('exit');
  while (global.mustCallChecks.length) {
    global.mustCallChecks.pop();
  }
  // console.log(Object.keys(sandbox).length)
}

const dirCont = fs.readdirSync(process.argv[2], {withFileTypes: true})
  .filter((e) => e.isFile() &&
    e.name.includes('.js') &&
    !e.name.includes('async-hooks') &&
    // !e.name.includes('async-w') &&
    !e.name.includes('deprecation') &&
    !TOO_HARD.includes(e.name) &&
    !TOO_SLOW.includes(e.name)
  )
  .map((e) => join(process.argv[2], e.name))
for (const ent of dirCont) {
  runTest(ent)
}

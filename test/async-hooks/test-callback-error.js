'use strict';
const common = require('../common');
const assert = require('assert');
const spawnSync = require('child_process').spawnSync;
const async_hooks = require('async_hooks');
const initHooks = require('./init-hooks');

const arg = process.argv[2];
switch (arg) {
  case 'test_init_callback':
    initHooks({
      oninit: common.mustCall(() => { throw new Error(arg); })
    }).enable();
    async_hooks.emitInit(
      async_hooks.executionAsyncId(),
      `${arg}_type`,
      async_hooks.triggerAsyncId()
    );
    return;

  case 'test_callback':
    initHooks({
      onbefore: common.mustCall(() => { throw new Error(arg); })
    }).enable();
    async_hooks.emitInit(
      async_hooks.executionAsyncId(),
      `${arg}_type`,
      async_hooks.triggerAsyncId()
    );
    async_hooks.emitBefore(async_hooks.executionAsyncId());
    return;

  case 'test_callback_abort':
    initHooks({
      oninit: common.mustCall(() => { throw new Error(arg); })
    }).enable();
    async_hooks.emitInit(
      async_hooks.executionAsyncId(),
      `${arg}_type`,
      async_hooks.triggerAsyncId()
    );
    return;
}

// this part should run only for the master test
assert.ok(!arg);
{
  const child = spawnSync(process.execPath, [__filename, 'test_init_callback']);
  assert.ifError(child.error);
  const test_init_first_line = child.stderr.toString().split(/[\r\n]+/g)[0];
  assert.strictEqual(test_init_first_line, 'Error: test_init_callback');
  assert.strictEqual(child.status, 1);
}

{
  const child = spawnSync(process.execPath, [__filename, 'test_callback']);
  assert.ifError(child.error);
  const test_callback_first_line = child.stderr.toString().split(/[\r\n]+/g)[0];
  assert.strictEqual(test_callback_first_line, 'Error: test_callback');
  assert.strictEqual(child.status, 1);
}

{
  const args = [
    '--abort-on-uncaught-exception',
    __filename,
    'test_callback_abort'
  ];
  // Timeout is set because this case is known to be problematic, probably
  // because of the core dump generated because of the `abort()`, so
  // stdout and stderr are logged for further analysis.
  // Ref: https://github.com/nodejs/node/issues/13527
  // Ref: https://github.com/nodejs/node/pull/13559
  const child = spawnSync(process.execPath, args, { timeout: 15 * 1000 });
  if (child.error && child.error.code === 'ETIMEDOUT') {
    console.log('   ==== stdout ====  ');
    console.log(child.stdout.toString());
    console.log('   ==== stderr ====  ');
    console.log(child.stderr.toString());
    assert.fail(child.error);
  }
  assert.strictEqual(child.stdout.toString(), '');

  const firstLineStderr = child.stderr.toString().split(/[\r\n]+/g)[0].trim();
  assert.strictEqual(firstLineStderr, 'Error: test_callback_abort');
}

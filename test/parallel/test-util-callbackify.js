'use strict';
const common = require('../common');

// This test checks that the semantics of `util.callbackify` are as described in
// the API docs

const assert = require('assert');
const { callbackify } = require('util');
const { join } = require('path');
const { execFile } = require('child_process');
const fixtureDir = join(common.fixturesDir, 'uncaught-exceptions');
const sentinelValues = [
  'hello world',
  null,
  undefined,
  { key: 'value' },
  Symbol('I am a symbol'),
  function ok() {},
  ['array', 'with', 4, 'values'],
  new Error('boo')
];

{
  // Test that the resolution value is passed as second argument to callback
  for (const sentinel of sentinelValues) {
    async function asyncFn() {
      return await Promise.resolve(sentinel);
    }

    const cbAsyncFn = callbackify(asyncFn);

    cbAsyncFn(common.mustCall((err, ret) => {
      assert.ifError(err);
      assert.strictEqual(ret, sentinel);
    }));

    function promiseFn() {
      return Promise.resolve(sentinel);
    }

    const cbPromiseFn = callbackify(promiseFn);

    cbPromiseFn(common.mustCall((err, ret) => {
      assert.ifError(err);
      assert.strictEqual(ret, sentinel);
    }));
  }
}

{
  // Test that rejection reason is passed as first argument to callback
  for (const sentinel of sentinelValues) {
    async function asyncFn() {
      return await Promise.reject(sentinel);
    }

    const cbAsyncFn = callbackify(asyncFn);

    cbAsyncFn(common.mustCall((err, ret) => {
      assert.strictEqual(ret, undefined);
      if (err instanceof Error) {
        if ('reason' in err) {
          assert.strictEqual(err.code, 'NULL_REJECTION');
          assert.strictEqual(err.reason, sentinel);
        } else {
          assert.strictEqual(String(sentinel).endsWith(err.message), true);
        }
      } else {
        assert.strictEqual(err, sentinel);
      }
    }));
  }

  for (const sentinel of sentinelValues) {
    function promiseFn() {
      return Promise.reject(sentinel);
    }

    const cbPromiseFn = callbackify(promiseFn);

    cbPromiseFn(common.mustCall((err, ret) => {
      assert.strictEqual(ret, undefined);
      if (err instanceof Error) {
        if ('reason' in err) {
          assert.strictEqual(err.code, 'NULL_REJECTION');
          assert.strictEqual(err.reason, sentinel);
        } else {
          assert.strictEqual(String(sentinel).endsWith(err.message), true);
        }
      } else {
        assert.strictEqual(err, sentinel);
      }
    }));
  }
}

{
  // Test that arguments passed to callbackified function are passed to original
  for (const sentinel of sentinelValues) {
    async function asyncFn(arg) {
      assert.strictEqual(arg, sentinel);
      return await Promise.resolve(arg);
    }

    const cbAsyncFn = callbackify(asyncFn);

    cbAsyncFn(sentinel, common.mustCall((err, ret) => {
      assert.ifError(err);
      assert.strictEqual(ret, sentinel);
    }));

    function promiseFn(arg) {
      assert.strictEqual(arg, sentinel);
      return Promise.resolve(arg);
    }

    const cbPromiseFn = callbackify(promiseFn);

    cbPromiseFn(sentinel, common.mustCall((err, ret) => {
      assert.ifError(err);
      assert.strictEqual(ret, sentinel);
    }));
  }
}

{
  // Test that `this` binding is the same for callbackified and original
  for (const sentinel of sentinelValues) {
    const iAmThis = {
      fn(arg) {
        assert.strictEqual(this, iAmThis);
        return Promise.resolve(arg);
      },
    };
    iAmThis.cbFn = callbackify(iAmThis.fn);

    iAmThis.cbFn(sentinel, common.mustCall(function(err, ret) {
      assert.ifError(err);
      assert.strictEqual(ret, sentinel);
      assert.strictEqual(this, iAmThis);
    }));

    const iAmThat = {
      async fn(arg) {
        assert.strictEqual(this, iAmThat);
        return await Promise.resolve(arg);
      },
    };
    iAmThat.cbFn = callbackify(iAmThat.fn);

    iAmThat.cbFn(sentinel, common.mustCall(function(err, ret) {
      assert.ifError(err);
      assert.strictEqual(ret, sentinel);
      assert.strictEqual(this, iAmThat);
    }));
  }
}

{
  // Test that callback that throws emits an `uncaughtException` event
  const fixture = join(fixtureDir, 'callbackify1.js');
  execFile(
    process.argv[0],
    [fixture],
    common.mustCall((err, stdout, stderr) => {
      assert.strictEqual(err.code, 1);
      assert.strictEqual(Object.getPrototypeOf(err).name, 'Error');
      assert.strictEqual(stdout, '');
      const errLines = stderr.trim().split(/[\r\n]+/g);
      const errLine = errLines.find((l) => /^Error/.exec(l));
      assert.strictEqual(errLine, `Error: ${fixture}`);
    })
  );
}

{
  // Test that handled `uncaughtException` works and passes rejection reason
  const fixture = join(fixtureDir, 'callbackify2.js');
  execFile(
    process.argv[0],
    [fixture],
    common.mustCall((err, stdout, stderr) => {
      assert.ifError(err);
      assert.strictEqual(stdout.trim(), fixture);
      assert.strictEqual(stderr, '');
    })
  );
}

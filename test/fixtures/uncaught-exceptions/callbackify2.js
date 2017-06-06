'use strict';

// Used to test the `uncaughtException` err object

const assert = require('assert');
const { callbackify } = require('util');

{
  const sentinel = new Error(__filename);
  process.once('uncaughtException',(err) => {
    assert.strictEqual(err, sentinel);
    console.log(err.message);
  });
  async function fn3() {
    return await Promise.reject(sentinel);
  }
  const cbFn = callbackify(fn3);

  cbFn((err, ret) => assert.ifError(err));
}

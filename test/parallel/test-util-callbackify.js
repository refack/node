'use strict';
const common = require('../common');


const assert = require('assert');
const { callbackify } = require('util');


{
  const sentinel = 'hello world';
  async function fn() {
    return await Promise.resolve(sentinel);
  }
  const cbFn = callbackify(fn);

  cbFn(common.mustCall((err, ret) => {
    if (err) assert.ifError(err);
    assert.strictEqual(ret, sentinel);
  }));
}

{
  const sentinel = 'hello world 2';
  function fn2() {
    return Promise.resolve(sentinel);
  }
  const cbFn = callbackify(fn2);

  cbFn(common.mustCall((err, ret) => {
    if (err) assert.ifError(err);
    assert.strictEqual(ret, sentinel);
  }));
}

{
  const sentinel = new Error('hello world 3');
  process.once('uncaughtException', common.mustCall((err) => {
    assert.strictEqual(err, sentinel);
  }));
  async function fn3() {
    return await Promise.reject(sentinel);
  }
  const cbFn = callbackify(fn3);

  cbFn(common.mustCall((err, ret) => {
    if (err) assert.ifError(err);
    common.mustNotCall('should not reach here')();
  }));
}

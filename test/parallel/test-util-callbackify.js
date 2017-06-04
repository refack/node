'use strict';
const common = require('../common');


const assert = require('assert');
const { callbackify } = require('util');
const { join } = require('path');
const { execFile } = require('child_process');
const fixtureDir = join(common.fixturesDir, 'uncaught-exceptions');

{
  const sentinel = 'hello world';
  async function fn() {
    return await Promise.resolve(sentinel);
  }
  const cbFn = callbackify(fn);

  cbFn(common.mustCall((err, ret) => {
    assert.ifError(err);
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
    assert.ifError(err);
    assert.strictEqual(ret, sentinel);
  }));
}

{
  async function fn3() {
    return await Promise.reject(null);
  }
  const cbFn = callbackify(fn3);

  cbFn(common.mustCall((err, ret) => {
    assert.strictEqual(Object.getPrototypeOf(err).name, 'Error');
    assert.strictEqual(err.message, 'null');
  }));
}

{
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

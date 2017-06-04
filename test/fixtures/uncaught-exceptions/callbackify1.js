'use strict';

// Used to test `uncaughtException` is emitted

const { callbackify } = require('util');

{
  const sentinel = new Error(__filename);

  async function fn3 () {
    return await Promise.reject(sentinel);
  }

  const cbFn = callbackify(fn3);

  cbFn((err, ret) => {
    throw err;
  });
}

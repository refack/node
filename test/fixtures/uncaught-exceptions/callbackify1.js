'use strict';

// Used to test that `uncaughtException` is emitted

const { callbackify } = require('util');

{
  async function fn3() { }

  const cbFn = callbackify(fn3);

  cbFn((err, ret) => {
    throw new Error(__filename);
  });
}

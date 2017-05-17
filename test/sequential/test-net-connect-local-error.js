'use strict';
const common = require('../common');
const assert = require('assert');
const net = require('net');

const client = net.connect({
  port: 13,
  localPort: common.PORT,
  localAddress: common.localhostIPv4
});

client.on('error', common.mustCall(function onError(err) {
  assert.strictEqual(err.syscall, 'connect');
  assert.strictEqual(err.code, 'ECONNREFUSED');
  assert.strictEqual(err.localPort, common.PORT + 1);
  assert.strictEqual(err.localAddress, common.localhostIPv4);
  assert.strictEqual(
    err.message,
    `connect ECONNREFUSED ${err.address}:${err.port} ` +
    `- Local (${err.localAddress}:${err.localPort})`
  );
}));

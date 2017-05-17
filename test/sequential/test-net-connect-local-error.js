'use strict';
const common = require('../common');
const assert = require('assert');
const net = require('net');

const NEVER_PORT = 26;
const localPort = common.PORT;
const client = net.connect({
  port: NEVER_PORT,
  localPort,
  localAddress: common.localhostIPv4
}, common.mustNotCall());

client.on('error', common.mustCall(function onError(err) {
  assert.strictEqual(err.syscall, 'connect');
  assert.strictEqual(err.code, 'ECONNREFUSED');
  assert.strictEqual(err.port, NEVER_PORT);
  assert.strictEqual(err.localPort, localPort);
  assert.strictEqual(err.localAddress, common.localhostIPv4);
  assert.strictEqual(
    err.message,
    `connect ECONNREFUSED ${err.address}:${err.port} ` +
    `- Local (${err.localAddress}:${err.localPort})`
  );
}));

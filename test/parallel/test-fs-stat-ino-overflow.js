'use strict';

const common = require('../common');
const assert = require('assert');

const fs = require('fs');
const promiseFs = require('fs').promises;
const path = require('path');
const tmpdir = require('../common/tmpdir');

tmpdir.refresh();

let testIndex = 0;

function getFilename() {
  const filename = path.join(tmpdir.path, `test-file-${++testIndex}`);
  fs.writeFileSync(filename, 'test');
  return filename;
}

function verifyStats(bigintStats, numStats) {
  const keys = [
    'dev', 'mode', 'nlink', 'uid', 'gid', 'rdev', 'size',
  ];
  if (!common.isWindows) {
    keys.push('blocks', 'blksize', 'ino');
  }
  for (const key of keys) {
    const nVal = numStats[key];
    const bVal = bigintStats[key];
    assert.strictEqual(
      bigintStats[key], BigInt(numStats[key]),
      `bigintStats.${key}: ${bVal} is not equal to numStats.${key}: ${nVal}`
    );
    assert.ok(
      Number.isSafeInteger(nVal),
      `numStats.${key}: ${nVal} is not a safe integer`
    );
  }
}

{
  const filename = getFilename();
  const bigintStats = fs.statSync(filename, { bigint: true });
  const numStats = fs.statSync(filename);
  verifyStats(bigintStats, numStats);
}

{
  const filename = __filename;
  const bigintStats = fs.statSync(filename, { bigint: true });
  const numStats = fs.statSync(filename);
  verifyStats(bigintStats, numStats);
}

{
  const filename = __dirname;
  const bigintStats = fs.statSync(filename, { bigint: true });
  const numStats = fs.statSync(filename);
  verifyStats(bigintStats, numStats);
}

{
  const filename = getFilename();
  const fd = fs.openSync(filename, 'r');
  const bigintStats = fs.fstatSync(fd, { bigint: true });
  const numStats = fs.fstatSync(fd);
  verifyStats(bigintStats, numStats);
  fs.closeSync(fd);
}

{
  const filename = getFilename();
  fs.stat(filename, { bigint: true }, (err, bigintStats) => {
    fs.stat(filename, (err, numStats) => {
      verifyStats(bigintStats, numStats);
    });
  });
}

{
  const filename = getFilename();
  const fd = fs.openSync(filename, 'r');
  fs.fstat(fd, { bigint: true }, (err, bigintStats) => {
    fs.fstat(fd, (err, numStats) => {
      verifyStats(bigintStats, numStats);
      fs.closeSync(fd);
    });
  });
}

(async function() {
  const filename = getFilename();
  const bigintStats = await promiseFs.stat(filename, { bigint: true });
  const numStats = await promiseFs.stat(filename);
  verifyStats(bigintStats, numStats);
})();

(async function() {
  const filename = getFilename();
  const handle = await promiseFs.open(filename, 'r');
  const bigintStats = await handle.stat({ bigint: true });
  const numStats = await handle.stat();
  verifyStats(bigintStats, numStats);
  await handle.close();
})();

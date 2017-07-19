'use strict';
var http = require('http');

// This code crashes the process
http.createServer((req, res) => {
  res.on('error', (err) => console.error('res had error:', err));

  res.write('hello');
  res.end();
  setImmediate(() => {
    res.write('world');
  });
}).listen(9000);

// This code works as expected
http.createServer((req, res) => {
  res.on('error', (err) => console.error('res had error:', err));

  res.write('hello');
  res.end();
  res.write('world');
}).listen(9001);

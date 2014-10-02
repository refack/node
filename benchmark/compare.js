'use strict';
/*globals console */
var fs = require('fs');
var path = require('path');


var usage = 'node benchmark/compare.js ' +
            '<node-binary1> <node-binary2> ' +
            '[--html] [--red|-r] [--green|-g]';
var show = 'both';
var execs = [];
var nodes = [];
var html = false;
var verbose = false;

for (var i = 2; i < process.argv.length; i++) {
  var arg = process.argv[i];
  switch (arg) {
    case '--verbose': case '-v':
      verbose = true;
      break;
    case '--red': case '-r':
      show = show === 'green' ? 'both' : 'red';
      break;
    case '--green': case '-g':
      show = show === 'red' ? 'both' : 'green';
      break;
    case '--html':
      html = true;
      break;
    case '-h': case '-?': case '--help':
      console.log(usage);
      process.exit(0);
      break;
    default:
      execs.push(arg);
      break;
  }
}

var start, green, red, white, reset, end;
if (!html) {
  start = '';
  green = '\x1b[1;32m';
  red = '\x1b[1;31m';
  white = '\x1b[1;30m';
  reset = '\x1b[m';
  end = '';
} else {
  start = '<pre style="background-color:#333;color:#eee" >';
  green = '<span style="background-color:#0f0;color:#000">';
  red =   '<span style="background-color:#f00;color:#fff">';
  white = '<span style="background-color:#333;color:#eee">';
  reset = '</span>';
  end =   '</pre >';
}

if (execs.length !== 2)
  console.error('usage:\n  %s', usage) || process.exit(1);

var spawn = require('child_process').spawn;
var results = {};
var toggle = 1;
var r = (+process.env.NODE_BENCH_RUNS || 1) * 2;


function run() {
  if (--r < 0)
    return compare();
  toggle = ++toggle % 2;

  var nodePath = path.resolve(execs[toggle]);
  console.error(nodePath);
  var child1 = spawn(nodePath, ['-e', "console.log(process.version, process.arch, process.platform)"]);
  child1.stdout.setEncoding('utf8');
  child1.stderr.pipe(process.stderr);

  var node = '';
  child1.stdout.on('data', function(c) {
    node += c;
  });

  child1.on('close', function(code) {
    node = node.trim();
    nodes.push(node);
    console.error('running %s - %s', nodePath, node);

    var args = process.execArgv.concat(path.join(__dirname, 'common.js'));
    var child = spawn(nodePath, args);
    child.stdout.setEncoding('utf8');
    child.stderr.pipe(process.stderr);

    var out = '';
    child.stdout.on('data', function (c) {
      if (verbose) console.error(c.trim());
      out += c;
    });

    child.on('close', function (code) {
      if (code) {
        console.error('%s exited with code=%d', nodePath, code);
        process.exit(code);
        return;
      }
      out.trim().split(/\r?\n/).forEach(function (line) {
        line = line.trim();
        if (!line)
          return;

        var s = line.split(' :');
        var num = +(s.pop().trim());
        if (!num && num !== 0)
          return;

        line = s[0].trim();
        var res = (toggle === 0) ? {} : results[line];
        if (!res) return;
        results[line] = res;
        results[line][node] = results[line][node] || [];
        results[line][node].push(num);
      });

      run();
    });
  });
}
run();


function compare() {
  // each result is an object with {"foo.js arg=bar":12345,...}
  // compare each thing, and show which node did the best.
  // node[0] is shown in green, node[1] shown in red.
  var maxLen = -Infinity;
  var util = require('util');
  console.log(start);

  Object.keys(results).map(function(bench) {
    var res = results[bench];
    var n0 = avg(res[nodes[0]]);
    var n1 = avg(res[nodes[1]]);

    var rawPct = (n1 - n0) / n0 * 100;
    var pct = ('        ' + rawPct.toFixed(2)).slice(-9, -1);

    var r = n0 > n1 ? red: green;
    if (Math.abs(rawPct) < 5) r = white;

    if (show === 'green' && r === red || show === 'red' && r === green)
      return;

    var r0 = util.format('%s: %s', nodes[0], ("         " + n0.toPrecision(5)).slice(-10));
    var r1 = util.format('%s%s: %s%s', r, nodes[1], ("         " + n1.toPrecision(5)).slice(-10), reset);
    pct = r + pct + '%' + reset;
    var comp = util.format('%s %s', r0, r1);
    maxLen = Math.max(bench.length + pct.length + comp.length + 1, maxLen);
    return [bench, comp, pct];
  }).filter(function(l) {
    return l;
  }).forEach(function(line) {
    var bench = line[0];
    var comp = line[1];
    var pct = line[2];
    var dotLen = maxLen - bench.length - pct.length - comp.length;
    var dots = new Array(Math.max(0, dotLen)).join('.');
    console.log(bench, dots, comp, pct);
  });
  console.log(end);
}


function avg(list) {
  if (!list || list.length == 0) return Infinity;
  if (list.length >= 3) {
    list = list.sort();
    var q = Math.floor(list.length / 4) || 1;
    list = list.slice(q, -q);
  }
  return list.reduce(function(a, b) {
    return a + b;
  }, 0) / list.length;
}

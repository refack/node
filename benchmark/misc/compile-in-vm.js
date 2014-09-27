var fs = require('fs');
var path = require('path');
var vm = require('vm');
var common = require('../common.js');
var bench = common.createBenchmark(compile, { reps: [50, 100, 200] });

function compile(conf) {
  var codes = {};
  var nodes = ['..'];
  while (nodes.length) {
    var node = nodes.pop();
    if (fs.statSync(node).isDirectory())
      nodes = nodes.concat(fs.readdirSync(node)
                .map(function (nn) { return path.join(node, nn); }));
    else if (path.extname(node) === '.js')
      codes[node] = fs.readFileSync(node, 'utf8');
  }
  conf.scripts = Object.keys(codes).length;

  
  bench.start();
  var all = 0;
  for (var i = 0; i < conf.reps; ++i) {
    var scripts = Object.keys(codes).reduce(function (s, k) {
      var code = codes[k];
      try {
        var temp = new vm.Script(code, {displayErrors: false, filename: k});
        return s + 1;
      } catch (e) {
        return s;
      }
    }, 0);
    all += scripts;
    conf.compiled = scripts;
  }
  conf.total = all;
  bench.end(conf.reps);
}

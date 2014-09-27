var common = require('../common.js');
var bench = common.createBenchmark(main, {
  type: 'Array Buffer Int8Array Uint8Array Int16Array Uint16Array Int32Array Uint32Array Float32Array Float64Array'.split(' '),
  millions: [25]
});

function main(conf) {
  var type = conf.type;
  var clazz = global[type];

  bench.start();
  var arrz = [];
  var strings = [];
  for (var i = 0; i < conf.millions; ++i) {
    arrz[i] = new clazz(1e6 + i);
    strings[i] = [].join.call(arrz[i]);
  }
  bench.end(conf.millions);
}

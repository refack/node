var common = require('../common.js');

var bench = common.createBenchmark(main, {
  thousands: [500],
  type: ['depth', 'breadth']
});

function main(conf) {
  if (conf.type === 'breadth') {
    breadth(+conf.thousands);
  } else {
    conf.thousands = Math.ceil(Math.log(+conf.thousands) / Math.log(2));
    depth(conf.thousands);
  }
}

function depth(m) {
  var N = m * 1e3;
  var n = 0;
  bench.start();
  setTimeout(cb);
  function cb() {
    n++;
    if (n === N)
      bench.end(m);
    else
      setTimeout(cb);
  }
}

function breadth(m) {
  var N = m * 1e3;
  var n = 0;
  bench.start();
  function cb() {
    n++;
    if (n === N)
      bench.end(m);
  }
  for (var i = 0; i < N; i++) {
    setTimeout(cb);
  }
}

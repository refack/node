import os
import sys

script_dir = os.path.dirname(__file__)
node_root  = os.path.normpath(os.path.join(script_dir, os.pardir))
gyp_path = os.path.join(node_root, 'deps','npm','node_modules','node-gyp',
                        'gyp','pylib')
sys.path.insert(0, gyp_path)
import gyp

# Directory within which we want all generated files (including Makefiles)
# to be written.
output_dir = os.path.join(os.path.abspath(node_root), '..', 'nodeout')

def run_gyp(args):
  # GYP bug.
  # On msvs it will crash if it gets an absolute path.
  # On Mac/make it will crash if it doesn't get an absolute path.
  arg_path = node_root if sys.platform == 'win32' else os.path.abspath(node_root)
  args.append(os.path.join(arg_path, 'node.gyp'))
  common_fn  = os.path.join(arg_path, 'common.gypi')
  options_fn = os.path.join(arg_path, 'config.gypi')
  options_fips_fn = os.path.join(arg_path, 'config_fips.gypi')

  if os.path.exists(common_fn):
    args.extend(['-I', common_fn])

  if os.path.exists(options_fn):
    args.extend(['-I', options_fn])

  if os.path.exists(options_fips_fn):
    args.extend(['-I', options_fips_fn])

  args.append('--depth=' + node_root)

  # Tell gyp to write the Makefiles into output_dir
  args.extend(['--generator-output', output_dir])

  # Tell make to write its output into the same dir
  args.extend(['-Goutput_dir=' + output_dir])

  args.append('-Dcomponent=static_library')
  args.append('-Dlibrary=static_library')

  # Don't compile with -B and -fuse-ld=, we don't bundle ld.gold.  Can't be
  # set in common.gypi due to how deps/v8/build/toolchain.gypi uses them.
  args.append('-Dlinux_use_bundled_binutils=0')
  args.append('-Dlinux_use_bundled_gold=0')
  args.append('-Dlinux_use_gold_flags=0')

  rc = gyp.main(args)
  if rc != 0:
    print 'Error running GYP'
    sys.exit(rc)


if __name__ == '__main__':
  args = sys.argv[1:]
  gyp_args = list(args)
  run_gyp(gyp_args)

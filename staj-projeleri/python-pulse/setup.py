#!/usr/bin/python
from distutils.core import setup, Extension
import commands as cmd


def pkgconfig_libs(args):
  lib = ["pulse","pulse-mainloop-glib"]
  for token in cmd.getoutput("pkg-config --libs  %s"% (args)).split():
    lib.append(token[2:])
  print "----pkgconfig_libs-----"
  for i in lib:
    print i
  return lib

def pkgconfig_inc(args):
  inc = ["/usr/include"]
  for token in cmd.getoutput("pkg-config --cflags %s"% (args)).split():
    inc.append(token[2:])
  print "-----pkgconfig_inc------"
  for i in inc:
    print i
  return inc


module1 = Extension('test',
                    define_macros = [('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
                    include_dirs = pkgconfig_inc("gtk+-2.0"),
                    libraries = pkgconfig_libs("gtk+-2.0"),
                    library_dirs = ['/usr/lib/pulse-0.9/modules'],
                    sources = ['src/test.c','src/func.c'])

setup (name = 'PackageName',
       version = '1.0',
       description = 'This is a demo package',
       author = 'Martin v. Loewis',
       author_email = 'martin@v.loewis.de',
       url = 'http://www.python.org/doc/current/ext/building.html',
       long_description = '''
This is really just a demo package.
''',
       ext_modules = [module1])

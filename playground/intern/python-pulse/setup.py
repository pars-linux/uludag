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


module1 = Extension('pypulse',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    include_dirs = pkgconfig_inc("gtk+-2.0"),
                    libraries = pkgconfig_libs("gtk+-2.0"),
                    library_dirs = ['/usr/lib/pulse-0.9/modules'],
                    sources = ['src/pypulse.c','src/func.c'])

setup (name = 'python-pulse',
       version = '0.1',
       description = 'experimental python bindings for pulseaudio',
       author = 'M.Burak Alkan',
       author_email = 'mburakalkan@gmail.com',
       url = 'http://svn.pardus.org.tr/uludag/trunk/staj-projeleri/python-pulse/',
       long_description = ''' ''',
       ext_modules = [module1])

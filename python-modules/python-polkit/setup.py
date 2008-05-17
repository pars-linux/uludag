#!/usr/bin/python
#-*- coding: utf-8 -*-

from distutils.core import setup, Extension

import os
import sys
prefix = os.environ.get("prefix", "/usr")

from distutils.core import setup, Extension
import subprocess as S

def pkg_config(package):
    library_path=[]
    libs=[]
    include_path=[]
    try:
        output,err = \
                   S.Popen('pkg-config --libs-only-L %s' % package,
                           shell=True, stdin=S.PIPE, stdout=S.PIPE,
                           close_fds=True).communicate()
        if output:
            for p in output.split():
                library_path.append(p.strip()[2:])
        output,err = \
                   S.Popen('pkg-config --libs-only-l %s' % package,
                           shell=True, stdin=S.PIPE, stdout=S.PIPE,
                           close_fds=True).communicate()
        if output:
            for p in output.split():
                libs.append(p.strip()[2:])
        output,err = \
                   S.Popen('pkg-config --cflags-only-I %s' % package,
                           shell=True, stdin=S.PIPE, stdout=S.PIPE,
                           close_fds=True).communicate()
        if output:
            for p in output.split():
                include_path.append(p.strip()[2:])
    except:
        print >> sys.stderr, "Failed to find pkg-config"
    return include_path,library_path,libs

pk_include_dirs, pk_library_dirs, pk_libs = pkg_config("dbus-1 polkit-dbus polkit-grant")


setup(name="pypolkit",
      version="0.1",
      description="Python bindings for polkit-grant",
      long_description="Python bindings for polkit-grant",
      license="GNU GPL2",
      author="Bahadır Kandemir",
      author_email="bahadir@pardus.org.tr",
      url="http://svn.pardus.org.tr/uludag/trunk/python-modules/python-polkit/",
      py_modules = ["polkit"],
      ext_modules = [Extension('_polkit',
                               sources=['pypolkit.c'],
                               include_dirs=pk_include_dirs,
                               libraries=pk_libs,
                               library_dirs=pk_library_dirs,
                               )],
      )

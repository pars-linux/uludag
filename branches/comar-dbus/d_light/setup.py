#!/usr/bin/python
#-*- coding: utf-8 -*-

from distutils.core import setup, Extension

setup(name="d_light",
      version="0.1",
      description="Lightweight Python bindings for DBus",
      long_description="Lightweight Python bindings for DBus",
      license="GNU GPL2",
      author="Bahadır Kandemir",
      author_email="bahadir@pardus.org.tr",
      url="http://www.pardus.org.tr/",
      packages = ['d_light'],
      ext_modules = [Extension('d_light.d_light',
                               sources=['d_light/d_light.c', '../comar/src/utility.c', '../comar/src/pydbus.c'],
                               libraries=['dbus-1'],
                               include_dirs=['../comar/include', '/usr/include/dbus-1.0', '/usr/lib/dbus-1.0/include'])],
      )

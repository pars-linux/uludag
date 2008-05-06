#!/usr/bin/python
#-*- coding: utf-8 -*-

from distutils.core import setup, Extension

setup(name="pypolkit",
      version="0.1",
      description="Python bindings for polkit-grant",
      long_description="Python bindings for polkit-grant",
      license="GNU GPL2",
      author="Bahadır Kandemir",
      author_email="bahadir@pardus.org.tr",
      url="http://www.pardus.org.tr/",
      ext_modules = [Extension('pypolkit',
                               sources=['pypolkit.c'],
                               libraries=['polkit-grant'],
                               include_dirs=['/usr/include/PolicyKit'])],
      )

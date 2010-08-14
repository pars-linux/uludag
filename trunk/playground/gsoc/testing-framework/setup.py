#! /usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import sys
from disutils.core import setup


setup(
      name='Package Tesing Framework',
      version='1.0',
      author='Sukhbir Singh',
      author_email='sukhbir.in@gmail.com',
      maintainer='Semen Cirit',
      maintainer_email='scirit@pardus.org.tr',      
      url='http://www.pardus.org.tr',
      description='A package testing framework for Pardus GNU/ Linux',
      license='GNU GPL',
      package_dir = {'': 'src'},
      packages = ['testcases', 'testcases.ui'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: Qt',          
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',          
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX :: Linux',          
          'Programming Language :: Python :: 2.6',
          'Topic :: Software Development :: Testing'
          ]
     )

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup

setup(name='ahenk-setup',
      version='1.9.26',
      description='Setup tools for for Ahenk Remote Management Framework',
      author='Bahadır Kandemir',
      author_email='bahadir@pardus.org.tr',
      url='http://www.pardus.org.tr/',
      scripts=['ahenk_setup'],
      data_files=[('/usr/share/ahenk-setup/schema', ['schema/%s' % x for x in os.listdir('schema') if not x.startswith(".")])]
     )

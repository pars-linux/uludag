#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup

setup(name='ahenk-setup',
      version='1.9.9',
      description='Setup tools for for Ahenk Remote Management Framework',
      author='Bahadır Kandemir',
      author_email='bahadir@python.net',
      url='http://www.pardus.org.tr/',
      scripts=['ahenk_setup'],
      data_files=[('/usr/share/ahenk-setup/schema', ['schema/%s' % x for x in os.listdir('schema')])]
     )

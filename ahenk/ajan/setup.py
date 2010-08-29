#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='Ajan',
      version='2.0',
      description='Agent for Ahenk Remote Management Framework',
      author='Bahadır Kandemir',
      author_email='bahadir@python.net',
      url='http://www.pardus.org.tr/',
      packages=['ahenk', 'ahenk.agent'],
      scripts=['ahenk_agent.py'],
      data_files=[('/var/lib/ahenk-agent/', ['modules/mod_software.py']),
                  ('/etc', ['etc/ahenk-agent.conf'])
                  ]
     )

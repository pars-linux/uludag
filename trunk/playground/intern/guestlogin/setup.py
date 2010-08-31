#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='guestlogin',
      version='0.1',
      description='PAM module for guest access.',
      author='Mesutcan Kurt',
      author_email='mesutcank@gmail.com',
      url='http://www.pardus.org.tr/',
      data_files=[('/lib/security', ['guestlogin.py']),
                  ('/etc/security', ['guestlogin.conf'])
                  ]
     )




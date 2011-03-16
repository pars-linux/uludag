#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='ahenk-agent',
      version='1.9.21',
      description='Agent for Ahenk Remote Management Framework',
      author='Bahadır Kandemir',
      author_email='bahadir@python.net',
      url='http://www.pardus.org.tr/',
      packages=['ahenk', 'ahenk.agent'],
      scripts=['ahenk_agent',
               'utils/ahenk_software_update',
               'utils/ahenk_firewall',
               'utils/ahenk_firewall_reset',
               'utils/ahenk_authentication'],
      data_files=[('/var/lib/ahenk-agent/', ['modules/mod_software.py',
                                             'modules/mod_webservices.py',
                                             'modules/mod_authentication.py',
                                             'modules/mod_firewall.py',
                                             'modules/mod_services.py',
                                            ]),
                  ('/etc/ahenk', ['etc/ahenk-agent.conf']),
                  ]
     )

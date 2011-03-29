#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='ahenk-lider',
      version='1.9.23',
      description='Agent for Ahenk Remote Management Framework',
      author='Bahadır Kandemir',
      author_email='bahadir@python.net',
      url='http://www.pardus.org.tr/',
      packages=['lider', 'lider.helpers', 'lider.plugins',
                'lider.plugins.plugin_authentication',
                'lider.plugins.plugin_firewall',
                'lider.plugins.plugin_services',
                'lider.plugins.plugin_software',
                'lider.plugins.plugin_summary',
                'lider.plugins.plugin_web',
                'lider.widgets',
                'lider.widgets.list_item'],
      scripts=['ahenk_lider'],
      data_files=[('/usr/share/ahenk-lider/', ['data/firewall.fwb'])],
     )

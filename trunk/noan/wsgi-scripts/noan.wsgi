#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append('/home/oguz/django-projects')
sys.path.append('/home/oguz/django-projects/noan')
os.environ['DJANGO_SETTINGS_MODULE'] = 'noan.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

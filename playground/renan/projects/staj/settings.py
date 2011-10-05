#!/usr/bin/python
# -*- coding: utf-8 -*-

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Renan Çakırerk', 'renan@pardus.org.tr'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'internshop'
DATABASE_USER = 'root'
DATABASE_PASSWORD = '12345'
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Istanbul'
LANGUAGE_CODE = 'tr'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@90jz*3*bvmal6t35vyre*3m5&as--(x1sgg&3cz9#3e=1)ysc2cc*@a'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'staj.urls'

TEMPLATE_DIRS = (
    #'/home/rcakirerk/workspace/pardus/playground/renan/projects/staj/templates',
    '/home/pars/workspace/staj/templates',
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'staj.form',
    'staj.captcha'
)

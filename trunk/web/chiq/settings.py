#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

ADMINS = ()
MANAGERS = ADMINS

# Site configuration
SITE_NAME = 'Pardus'
SITE_DESC = 'PARDUS :: TÜBİTAK UEKAE'

DEBUG = True
TESTING = True
TEMPLATE_DEBUG = DEBUG
WEB_URL = 'http://127.0.0.1:8000'
DOCUMENT_ROOT = '/home/jnmbk/public_html/web/chiq'

DATABASE_ENGINE = 'mysql'
#DATABASE_ENGINE = "mysql"
DATABASE_NAME = 'chiq'
DATABASE_USER = 'chiq'
DATABASE_PASSWORD = '******'
DATABASE_HOST = 'localhost'
DATABASE_PORT = ''

# Email
DEFAULT_FROM_EMAIL = 'noreply@pardus.org.tr'
#EMAIL_USE_TLS = True

TAG_PER_PAGE = 10

TIME_ZONE = 'Europe/Istanbul'
LANGUAGE_CODE = 'tr'
SITE_ID = 1

MEDIA_ROOT = '%s/media/' % DOCUMENT_ROOT
MEDIA_URL = '%s/media/' % WEB_URL
ADMIN_MEDIA_PREFIX = '/media/'
WEBALIZER_DIR = ''

SECRET_KEY = 'n9-*x3!&!(x*z_!13)cyxil4fh+ov_+3!y($&4t7iit=)d)=93'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'chiq.context_processors.testing',
    'django.core.context_processors.auth',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'chiq.flatpages.middleware.FlatpageFallbackMiddleware',
    'chiq.middleware.threadlocals.ThreadLocals',
)

ROOT_URLCONF = 'chiq.urls'

TEMPLATE_DIRS = (
    '%s/templates' % DOCUMENT_ROOT,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'chiq.flatpages',
    'chiq.st',
    'chiq.upload',
    'chiq.webalizer',
)

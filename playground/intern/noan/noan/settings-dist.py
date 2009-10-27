# -*- coding: utf-8 -*-
# Django settings for noan project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Your Name', 'account@yourdomain.com'),
)

MANAGERS = ADMINS

# Database
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/path_to/noan/db/noan.sqlite3'

# Local time zone for this installation.
TIME_ZONE = 'Europe/Istanbul'

# Language code for this installation.
LANGUAGE_CODE = 'tr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
MEDIA_ROOT = '/path_to/noan/media/'

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = 'http://noan/media/'

# URL prefix for admin media
ADMIN_MEDIA_PREFIX = '/admin-media/'

# URL that handle to redirect for login and logout.

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/repository/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@yxfqa*3vv8%1!93scf5cwcztx-gurqmm1shk68b&(m6l_xoi!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    # 'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'noan.middleware.threadlocals.ThreadLocals',
    # 'noan.middleware.qcount.SQLLogMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'noan.context_processors.distros',
)

ROOT_URLCONF = 'noan.urls'

TEMPLATE_DIRS = (
    '/path_to/noan/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'noan.repository',
)

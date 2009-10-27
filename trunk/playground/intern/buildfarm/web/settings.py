# -*- coding: utf-8 -*-
#
# Copyright © 2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
# Default django settings for buildfarm web interface

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('S.Çağlar Onur', 'caglar@pardus.org.tr'),
    ('Ozan Çağlayan', 'ozancag@gmail.com'),
)

# Don't forget to define these!
DOCUMENT_ROOT = '/home/ozan/uludag/trunk/staj-projeleri/buildfarm/web'
WEB_URL = ''

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'db/buildfarm.db'   # Or path to database file if using sqlite3.
DATABASE_USER = ''                  # Not used with sqlite3.
DATABASE_PASSWORD = ''              # Not used with sqlite3.
DATABASE_HOST = ''                  # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                  # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Istanbul'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'tr'

LANGUAGES = (
    ('en', ('English')),
    ('tr', ('Turkish')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/static/' % DOCUMENT_ROOT

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '%s/static/' % WEB_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@yom@$))7s!*9l)j97gjv8iu+!m@qhp985s16#7bzl6vm7(5*v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'web.urls'

TEMPLATE_DIRS = (
    '%s/templates' % DOCUMENT_ROOT,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'web.ciftci',
)

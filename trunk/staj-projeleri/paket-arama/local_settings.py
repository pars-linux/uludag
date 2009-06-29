# -*- coding: utf-8 -*-
# Can add/remove a version support here
versions = ['pardus-2009', 'pardus-2008', 'contrib-2008']
default_version = 'pardus-2009'

# Paths
WEB_URL = 'http://paketler.pardus.org.tr/search'
DOCUMENT_ROOT = '/var/www/paketler.pardus.org.tr/htdocs/search'

# DB Settings
DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'search'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

LIST_SIZE = 100
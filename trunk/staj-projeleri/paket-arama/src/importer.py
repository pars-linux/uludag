"""Imports the given compressed file (bz2) into mysql database"""
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

db_name = 'search'
user = 'root'

files = ['arama2009.sql', 'arama2008.sql', 'arama2007.sql']

for file_name in files:
    print 'Uncompressing the bz2 file %s ...' % file_name
    os.system('bzip2 -d %s.bz2' % file_name)
    print 'Import operation starting...'
    os.system('mysql -u %s %s < %s' % (user, db_name, file_name)) 
    print 'Import of %s finished.' % file_name
print 'Import operation finished...'

"""Imports the given compressed file (bz2) into mysql database"""
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

db_name = 'arama'
user = 'root'
file_name = 'arama.sql'

print 'Uncompressing the bz2 file...'
os.system('bzip2 -d %s.bz2' % file_name)
print 'Import operation starting...'
os.system('mysql -u %s %s < %s' % (user, db_name, file_name)) 
print 'Import operation finished...'

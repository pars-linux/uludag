"""
Generates INSERT SQL Statements for each package-file statement and
appends these statements at every 50 package into a file.
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-


import pisi
import sys
import os


# Determine version
try:
    f = open('/etc/pardus-release')
    content = f.readline()
    f.close()
    import string.digits
    version = filter(lambda c : c in string.digits, content)[:4]
except:
    version = '2008'
    
    
debug = False
file_name = 'arama%s.sql' % version


if len(sys.argv) > 1:
    if sys.argv[1] in ['--debug', '-d', '-v']:
        debug = True
    else:
        debug = False
    
    if sys.argv[1] in ['--help', '-h']:
        print """Usage: python sqlgen.py [option]
        Options:
        -h        Help
        --help
        
        -d        Debugging
        --debug
        -v"""
        sys.exit()



if os.path.exists('./%s.bz2' % file_name):
    os.rename('./%s.bz2' % file_name, './%s-old.bz2' %  file_name)
    if debug: print "Renamed old file."

f = open(file_name, "w")
f.write("""BEGIN;
DROP TABLE IF EXISTS files%(version)s;
CREATE TABLE `files%(version)s` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `package` varchar(60) NOT NULL,
    `path` varchar(200) NOT NULL
)
;
COMMIT;
""" % {'version':version})
f.close()
if debug: print "Written drop/create table statements."
if debug: print "Fetching package information from pisi."

pi     = pisi.db.installdb.InstallDB()
statements = ""
installed_packages = pi.list_installed()
counter = 0
index = 1

if debug: print "Writing package information starting..."
for package in installed_packages:
    if debug: print "Package: %s" % package 
    # Get the file list for a package
    files = [file.path for file in pi.get_files(package).list]
    
    # For each file, generate an INSERT INTO statement and append it
    for file in files:
        statements += "INSERT INTO files%s VALUES('%d', '%s', '/%s');\n" % (version, index, package, file)
        index += 1
    counter+=1
    if counter == 50:
        f = open(file_name, "a")
        f.write(statements)
        f.close()
        statements = ""
        counter = 0
        if debug: print "Appended to the file..."

if debug: print 'Adding index'
f = open(file_name, "a")
f.write('CREATE INDEX package_index USING BTREE on files%s(package);\n' % version)
f.close()

if debug: print 'Compressing...'
# os.system('tar -czf arama.tar.gz arama.sql')
os.system('bzip2 -z %s' % file_name)
if debug: print 'Finished...'

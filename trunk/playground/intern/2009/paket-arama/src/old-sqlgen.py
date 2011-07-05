#ifndef SQLGEN_PY
#define SQLGEN_PY
"""
Generates INSERT SQL Statements for each package-file statement and
appends these statements at every 50 package into a file.
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-


import pisi
import sys
import os

def append_to_file(file_name, content):
    f = open(file_name, "a")
    f.write(content)
    f.close()

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
contrib = False # This is not a contrib buildfarm, unless otherwise specified.




if len(sys.argv) > 1:
    if sys.argv[1] in ['--debug', '-d', '-v']:
        debug = True
    else:
        debug = False

    contrib_parameters = ['--contrib', '-c']
    if len(sys.argv) > 2 and (sys.argv[1] in contrib_parameters or sys.argv[2] in contrib_parameters):
        contrib = True
        version += 'contrib'

    if sys.argv[1] in ['--help', '-h']:
        print """Usage: python sqlgen.py [option]
        Options:
        -h        Help
        --help
        
        -d        Debugging
        --debug
        -v
        
        -c        Contrib Repo
        --contrib"""
        sys.exit()


file_name = 'arama%s.sql' % version

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

statements = ""
if version[:4] == '2008':
    pi = pisi.db.installdb.InstallDB()
    installed_packages = pi.list_installed()

    # If this is a contrib build-farm, then find out the contrib packages.
    if contrib:
        packagedb = pisi.db.packagedb.PackageDB()
#        contrib_packages = set(installed_packages).intersection(packagedb.list_packages("contrib-2008"))
        contrib_packages = set(installed_packages) - set(packagedb.list_packages("pardus-2008"))
elif version[:4] == '2007':
    pisi.api.init()
    pi = pisi.installdb.init()
    installed_packages = pi.list_installed()        
else:
    print "Unknown version!"
    raise

counter = 0
index = 1

if debug: print "Writing package information starting..."

# If this is a contrib buildfarm, only scan the contrib packages...
if contrib:
    installed_packages = contrib_packages

for package in installed_packages:
    if debug: print "Package: %s" % package 
    # Get the file list for a package
    if version[:4] == '2007':
        files = [file.path for file in pi.files(package).list]
    elif version[:4] == '2008':
        files = [file.path for file in pi.get_files(package).list]
    #else:
        # for pisi api changes...
    #    files = [file.path for file in pi.get_files(package).list]
    # For each file, generate an INSERT INTO statement and append it

    for file in files:
        to_be_added = '''INSERT INTO files%s VALUES(%d, "%s", "/%s");
''' % (version, index, package, file)

        statements += to_be_added
        index += 1
    counter+=1
    if counter == 50:
        append_to_file(file_name, statements)
        statements = ""
        counter = 0
        if debug: print "Appended to the file..."

if counter != 0:
    append_to_file(file_name, statements)
        
if version[0:4] == '2007':
    pisi.installdb.finalize()
    pisi.api.finalize()
    
if debug: print 'Adding index'
f = open(file_name, "a")
f.write('CREATE INDEX package_index USING BTREE on files%s(package);\n' % version)
f.close()

if debug: print 'Compressing...'
# os.system('tar -czf arama.tar.gz arama.sql')
os.system('bzip2 -z %s' % file_name)
if debug: print 'Finished...'
#endif // SQLGEN_PY

"""
Generates INSERT SQL Statements for each package-file statement and
appends these statements at every 50 package into a file.
"""

import pisi
import time
import sys
import os

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

if os.path.exists('./output.sql'):
    os.rename('./output.sql','./old-output.sql') 

start = time.time()

pi     = pisi.db.installdb.InstallDB()
statements = ""
installed_packages = pi.list_installed()
counter = 0

for package in installed_packages:
    if debug: print "Package: %s" % package 
    # Get the file list for a package
    files = [file.path for file in pi.get_files(package).list]
    
    # For each file, generate an INSERT INTO statement and append it
    for file in files:
        statements += "INSERT INTO files VALUES('%s', '/%s');\n" % (package, file)
        
    counter+=1
    if counter == 50:
        f = open("output.sql", "a")
        f.write(statements)
        f.close()
        statements = ""
        counter = 0
        print "Appended..."

finish = time.time()
diff = finish - start
print 'Time:', diff
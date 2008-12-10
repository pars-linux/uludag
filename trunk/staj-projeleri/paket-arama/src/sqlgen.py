"""
Generates INSERT SQL Statements for each package-file statement and
appends these statements at every 50 package into a file.
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-


import pisi
import sys
import os
import getopt
import piksemel
import string
import gzip
#import bz2

def append_to_file(file_name, content):
    f = open(file_name, "a")
    f.write(content)
    f.close()
    
def underscorize(repo_name):
    return repo_name.replace("-", "_")

def parse_package_names_from_doc(doc):
    return dict(map(lambda x: (x.getTagData("Name"), gzip.zlib.compress(x.toString())), doc.tags("Package")))

def remove_bz2(filename):
    if filename.endswith("bz2"):
        filename = filename.split(".bz2")[0]
    return filename
    
def package_list_from_index(index_path):
    index_path = remove_bz2(index_path)
    doc = piksemel.parse(index_path)
    x = parse_package_names_from_doc(doc)
    return x.keys()
    
def usage():
    print """Usage: python sqlgen.py [options] [arguments]
    Options:
    -h        Help
    --help
    
    -v        Verbose mode
    --verbose
    -d
    --debug
    
    Arguments:
    -r REPO_NAME
    --repo=REPONAME
    repo=REPO_NAME
    
    -i REPO_INDEX
    --index=REPO_INDEX
    index=REPO_INDEX
    """

# -------- ARGUMENT PARSING STARTS--------------
try:
    opts, args = getopt.getopt(sys.argv[1:], "hvr:i:o:", ["help", "repo=", "index=", "output="])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
verbose = False

repo = None
index = None
output = None

for o, a in opts:
    if o in ("-v", "--verbose", "--debug", "-d"):
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-r", "--repo"):
        repo = a
    elif o in ("-i", "--index"):
        index = a
    elif o in ("-o", "--output"):
        output = remove_bz2(a)
    else:
        assert False, "unhandled option"

assert repo!=None
assert index!=None
assert output!=None

# -------- ARGUMENT PARSING ENDED--------------

# -------- VERSION DETECTION --------------
version = filter(lambda x:x in string.digits, repo)
print repo,index,output,version
assert len(version)==4
# -----------------------------------------


f = open(output, "w")
f.write("""BEGIN;
DROP TABLE IF EXISTS %(repo)s;
CREATE TABLE `%(repo)s` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `package` varchar(60) NOT NULL,
    `path` varchar(200) NOT NULL
)
;
COMMIT;
""" % {'repo': underscorize(repo)})
f.close()
if verbose: print "Written drop/create table statements."
if verbose: print "Fetching package information from pisi."

statements = ""
if version == '2008':
    installed_packages = package_list_from_index(index) # Assuming all the packages are installed!
    pi = pisi.db.installdb.InstallDB()
elif version == '2007':
    pisi.api.init()
    pi = pisi.installdb.init()
    installed_packages = pi.list_installed()
    # TODO: ADD 2007 XML parsing here?
else:
    print "Unknown version!"
    raise

counter = 0
index = 1

if verbose: print "Writing package information starting..."

for package in installed_packages:
    if verbose: print "Package: %s" % package 
    # Get the file list for a package
    if version == '2007':
        files = [file.path for file in pi.files(package).list]
    elif version == '2008':
        try:
            files = [file.path for file in pi.get_files(package).list]
        except:
            if verbose: print "Passing %s..." % package
            continue
    #else:
        # for pisi api changes...
    #    files = [file.path for file in pi.get_files(package).list]
    # For each file, generate an INSERT INTO statement and append it

    for file in files:
        to_be_added = '''INSERT INTO %s VALUES(%d, "%s", "/%s");
''' % (underscorize(repo), index, package, file)

        statements += to_be_added
        index += 1
    counter+=1
    if counter == 50:
        append_to_file(output, statements)
        statements = ""
        counter = 0
        if verbose: print "Appended to the file..."

if counter != 0:
    append_to_file(output, statements)
        
if version == '2007':
    pisi.installdb.finalize()
    pisi.api.finalize()
    
if verbose: print 'Adding index'
f = open(output, "a")
f.write('CREATE INDEX package_index USING BTREE on %s;\n' % underscorize(repo))
f.close()

if verbose: print 'Compressing...'
os.system('bzip2 -z %s' % output)
if verbose: print 'Finished...'
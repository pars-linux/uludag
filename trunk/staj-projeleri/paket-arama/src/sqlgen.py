# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
SQL Generator for the Package Search system.

Generates INSERT SQL Statements for each package-file statement and
appends these statements at every 50 package into a file.
"""

import pisi
import sys
import os
import getopt
import piksemel
import string
import gzip

def append_to_file(file_name, content):
    """Appends the given content to the file"""
    f = open(file_name, "a")
    f.write(content)
    f.close()
    
def underscorize(repo_name):
    """Replaces -s to _ to comply with MySQL rules"""
    return repo_name.replace("-", "_")

def remove_bz2(filename):
    """Get the unzipped filename"""
    if filename.endswith("bz2"):
        filename = filename.split(".bz2")[0]
    return filename
    
def parse_package_names_from_doc(doc):
    """Parses package names from the piksemel document."""
    return dict(map(lambda x: (x.getTagData("Name"), gzip.zlib.compress(x.toString())), doc.tags("Package")))
    
def package_list_from_index(index_path):
    """Returns the package list of a repo, given the repo's index."""
    index_path = remove_bz2(index_path)
    doc = piksemel.parse(index_path)
    x = parse_package_names_from_doc(doc)
    return x.keys()
    
def usage():
    """Prints the usage of the script."""
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
    
    -i REPO_INDEX_PATH
    --index=REPO_INDEX_PATH
    index=REPO_INDEX_PATH
    
    -o OUTPUT_PATH
    --output=OUTPUT_PATH
    output=OUTPUT_PATH
    """

# -------- ARGUMENT PARSING STARTS---------
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
        index_path = a
    elif o in ("-o", "--output"):
        output = remove_bz2(a)
    else:
        assert False, "unhandled option"

try:
    assert repo!=None
    assert index_path!=None
    assert output!=None
except Exception, e:
    usage()
    sys.exit(2)

# -------- ARGUMENT PARSING ENDED---------

# -------- REMOVE OLD FILES --------------
if os.path.exists(output):
    os.remove(output)
if os.path.exists(output+".bz2"):
    os.remove(output+".bz2")
# ------- CLEAR!-------------------------

# -------- VERSION DETECTION --------------
version = filter(lambda x:x in string.digits, repo)
assert len(version)==4
# -----------------------------------------

# -------- SQL HEADER ---------------------
f = open(output, "w")
f.write("""BEGIN;
/*DROP TABLE IF EXISTS packages;*/
CREATE TABLE `packages` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `repo` varchar(30) NOT NULL,
    `package` varchar(60) NOT NULL,
    `path` varchar(200) NOT NULL
)
;
COMMIT;
""") # % {'repo': underscorize(repo)})
f.close()
# ------------------------------------------

if verbose: print "Written drop/create table statements."
if verbose: print "Fetching package information from pisi."

# ---------- PACKAGE LIST ------------------
if version in ('2008','2009'):
    installed_packages = package_list_from_index(index_path) # Assuming all the packages are installed!
    pi = pisi.db.installdb.InstallDB()
elif version == '2007':
    pisi.api.init()
    pi = pisi.installdb.init()
    installed_packages = pi.list_installed()
    # TODO: ADD 2007 XML parsing here?
else:
    print "Unknown version!"
    raise

# ------------------------------------------

# ---------- PACKAGE CONTENTS --------------
statements = ""
package_counter = 0
record_index = 1
problematic_packages = []

if verbose: print "Writing package information starting..."

for package in installed_packages:
    if verbose: print "Package: %s" % package 
    # Get the file list for a package
    try:
        if version == '2007':
            files = [thefile.path for thefile in pi.files(package).list]
        elif version in ('2008','2009'):
            files = [thefile.path for thefile in pi.get_files(package).list]
        #else:
        # for pisi api changes in the future...
        #    files = [thefile.path for thefile in pi.get_files(package).list]
    except:
           problematic_packages.append(package)
           continue

    # For each file, generate an INSERT INTO statement and append it
    for thefile in files:
        to_be_added = '''INSERT INTO packages VALUES(%d, "%s",  "%s", "/%s");
''' % (record_index,underscorize(repo), package, thefile)
        statements += to_be_added
        record_index += 1
    # Package FINISHED!
    package_counter+=1
    # Clear at some periods.
    if package_counter == 50:
        append_to_file(output, statements)
        statements = ""
        package_counter = 0
        if verbose: print "Appended to the file..."
# If there are remaining statements not written yet, write them.
if package_counter != 0:
    append_to_file(output, statements)

# Finalize the database if it is Pardus 2007.
if version == '2007':
    pisi.installdb.finalize()
    pisi.api.finalize()

# Add index and make it faster!
if verbose: print 'Adding index'
f = open(output, "a")
f.write('CREATE INDEX package_index USING BTREE on packages(package);\n')
f.write('CREATE INDEX repo_index USING BTREE on packages(repo);\nCOMMIT;\n')
f.close()

# Compress the SQL file.
if verbose: print 'Compressing...'
os.system('bzip2 -z %s' % output)

# Warn if there are any problematic packages...
if problematic_packages:
    print "Warning! These packages are not included as they don't seem to be installed on the system:", ",".join(problematic_packages)

print 'Finished...'

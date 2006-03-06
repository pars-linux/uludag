# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# misc. utility functions, including process and file utils

# Authors:  Eray Ozkural <eray@uludag.org.tr>
#           Baris Metin <baris@uludag.org.tr>
#           S. Caglar Onur <caglar@uludag.org.tr>
#           A. Murat Eren <meren@uludag.org.tr>

# standard python modules
import os
import re
import sys
import sha
import shutil
import string
import statvfs
import operator

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

# pisi modules
import pisi
import pisi.context as ctx

class Error(pisi.Error):
    pass

class FileError(Error):
    pass


#########################
# spec validation utility #
#########################

class Checks:
    def __init__(self):
        self.list = []
    
    def add(self, err):
        self.list.append(err)
    
    def join(self, list):
        self.list.extend(list)
    
    def has_tag(self, var, section, name):
        if not var:
            self.list.append(_("%s section should have a '%s' tag") % (section, name))

    def has_error():
        return len(self.list)>0
        
    def print_errors(list):
        for x in list:
            ctx.ui.error(x)
    print_errors = staticmethod(print_errors)

#########################
# string/list/functional#
#########################

def every(pred, seq):
    return reduce(operator.and_, map(pred, seq))

def any(pred, seq):
    return reduce(operator.or_, map(pred, seq))

def unzip(seq):
    return zip(*seq)

def concat(l):
    '''concatenate a list of lists'''
    return reduce( operator.concat, l )

def strlist(l):
    """concatenate string reps of l's elements"""
    return "".join(map(lambda x: str(x) + ' ', l))

def multisplit(str, chars):
    """ split str with any of chars"""
    l = [str]
    for c in chars:
        l = concat(map(lambda x:x.split(c), l))
    return l

def same(l):
    '''check if all elements of a sequence are equal'''
    if len(l)==0:
        return True
    else:
        last = l.pop()
        for x in l:
            if x!=last:
                return False
        return True

def prefix(a, b):
    '''check if sequence a is a prefix of sequence b'''
    if len(a)>len(b):
        return False
    for i in range(0,len(a)):
        if a[i]!=b[i]:
            return False
    return True

def remove_prefix(a,b):
    "remove prefix a from sequence b"
    assert prefix(a,b)
    return b[len(a):]


##############################
# Process Releated Functions #
##############################

def run_batch(cmd, realtime = False):
    """run command non-interactively/realtime and report return value and output"""
    ctx.ui.info(_('running ') + cmd)
    p = os.popen(cmd)
    if realtime:
        while 1:
            line = p.readline()
            if not line:
                break
            ctx.ui.debug(line[:-1])
        return p.close()
    else:
        lines = p.readlines()
    ret = p.close()
    ctx.ui.debug(_('return value %s') % ret)
    successful = ret == None
    if not successful:
        ctx.ui.error(_('Failed command: %s') % cmd + strlist(lines))
    return (successful,lines)

######################
# Terminal functions #
######################

def has_xterm():
    return os.environ.has_key("TERM") and sys.stderr.isatty()
    
def xterm_title(message):
    """sets message as a console window's title"""
    if os.environ.has_key("TERM") and sys.stderr.isatty():
        terminalType = os.environ["TERM"]
        for term in ["xterm", "Eterm", "aterm", "rxvt", "screen", "kterm", "rxvt-unicode"]:
            if terminalType.startswith(term):
                sys.stderr.write("\x1b]2;"+str(message)+"\x07")
                sys.stderr.flush()
                break

def xterm_title_reset():
    """resets console window's title"""
    if os.environ.has_key("TERM"):
        terminalType = os.environ["TERM"]
        xterm_title(os.environ["TERM"])

    
#############################
# Path Processing Functions #
#############################

def splitpath(a):
    """split path into components and return as a list
    os.path.split doesn't do what I want like removing trailing /"""
    comps = a.split(os.path.sep)
    if comps[len(comps)-1]=='':
        comps.pop()
    return comps

def makepath(comps, relative = False, sep = os.path.sep):
    """reconstruct a path from components"""
    path = reduce(lambda x,y: x + sep + y, comps, '')
    if relative:
        return path[len(sep):]
    else:
        return path

def parentpath(a, sep = os.path.sep):
    # remove trailing '/'
    a = a.rstrip(sep)
    return a[:a.rfind(sep)]

def parenturi(a):
    return parentpath(a, '/')

# I'm not sure how necessary this is. Ahem.
def commonprefix(l):
    """an improved version of os.path.commonprefix,
    returns a list of path components"""
    common = []
    comps = map(splitpath, l)
    for i in range(0, min(len,l)):
        compi = map(lambda x: x[i], comps) # get ith slice
        if same(compi):
            common.append(compi[0])
    return common

# but this one is necessary
def subpath(a, b):
    "find if path a is before b in the directory tree"
    return prefix(splitpath(a), splitpath(b))

def removepathprefix(prefix, path):
    "remove path prefix a from b, finding the pathname rooted at a"
    comps = remove_prefix(splitpath(prefix), splitpath(path))
    if len(comps) > 0:
        return join_path(*tuple(comps))
    else:
        return ""

def absolute_path(path):
    "determine if given @path is absolute"
    comps = splitpath(path)
    return comps[0] == ''

def join_path(a, *p):
    """Join two or more pathname components, inserting '/' as needed"""
    """The python original version has a silly logic"""
    path = a
    for b in p:
        b = b.lstrip('/')
        if path == '' or path.endswith('/'):
            path +=  b
        else:
            path += '/' + b
    return path

####################################
# File/Directory Related Functions #
####################################

def check_file(file, mode = os.F_OK):
    "shorthand to check if a file exists"
    if not os.access(file, mode):
        raise FileError("File " + file + " not found")
    return True

def check_dir(dir):
    """check if directory exists, and create if it doesn't.
    works recursively"""
    dir = dir.strip().rstrip("/")
    if not os.access(dir, os.F_OK):
        os.makedirs(dir)

def clean_dir(path):
    "Remove all content of a directory (top)"
    # don't reimplement the wheel
    if os.path.exists(path):
        shutil.rmtree(path)

def creation_time(file):
    """returns the creation time of the given file"""
    if check_file(file):
        import time
        st = os.stat(file)
        return time.localtime(st.st_ctime)

def dir_size(dir):
    """ calculate the size of files under a dir
    based on the os module example"""
    # It's really hard to give an approximate value for package's
    # installed size. Gettin a sum of all files' sizes if far from
    # being true. Using 'du' command (like Debian does) can be a
    # better solution :(.
    # Not really, du calculates size on disk, this is much better -- exa
    from os.path import getsize, islink, isdir, exists
    join = join_path

    if exists(dir) and (not isdir(dir) and not islink(dir)):
        #so, this is not a directory but file..
        return getsize(dir)

    if islink(dir):
        return long(len(os.readlink(dir)))

    def sizes():
        for root, dirs, files in os.walk(dir):
            yield sum([getsize(join(root, name)) for name in files if not islink(join(root,name))])
            yield sum([long(len(os.readlink((join(root, name))))) for name in files if islink(join(root,name))])
    return sum( sizes() )

def copy_file(src,dest):
    """copy source file to destination file"""
    check_file(src)
    check_dir(os.path.dirname(dest))
    shutil.copyfile(src, dest)

# FIXME: this should be done in a much much simpler way
# as it stands, it seems to be a kludge to solve
# an unrelated problem
def get_file_hashes(top, excludePrefix=None, removePrefix=None):
    """Generator function iterates over a toplevel path and returns the
    (filePath, sha1Hash) tuples for all files. If excludePrefixes list
    is given as a parameter, function will exclude the filePaths
    matching those prefixes. The removePrefix string parameter will be
    used to remove prefix from filePath while matching excludes, if
    given."""

    def sha1_sum(f, data=False):
        func = None
        if data:
            func = sha1_data
        else:
            func = sha1_file

        try:
            return func(f)
        except FileError, e:
            if os.path.islink(f):
                ctx.ui.info(_("Including external link '%s'") % f)
            elif os.path.isdir(f):
                ctx.ui.info(_("Including directory '%s'") % f)
            else:
                raise e
            return None

    def has_excluded_prefix(filename):
        if excludePrefix and removePrefix:
            tempfnam = remove_prefix(removePrefix, filename)
            for p in excludePrefix:
                if tempfnam.startswith(p):
                    return 1
        return 0

    # handle single file
    if os.path.isfile(top):
        yield (top, sha1_sum(top))
        return

    # handle single symlink declaration here.
    if os.path.islink(top):
        yield (top, sha1_sum(os.readlink(top), True))
        return

    for root, dirs, files in os.walk(top, topdown=False):
        #bug 339
        if os.path.islink(root) and not has_excluded_prefix(root):
            #yield the symlink..
            #bug 373
            yield (root, sha1_sum(os.readlink(root), True))
            excludePrefix.append(remove_prefix(removePrefix, root) + "/")
            continue

        #bug 397
        for dir in dirs:
            d = join_path(root, dir)
            if os.path.islink(d) and not has_excluded_prefix(d):
                yield (d, sha1_sum(os.readlink(d), True))
                excludePrefix.append(remove_prefix(removePrefix, d) + "/")

        #bug 340
        if os.path.isdir(root) and not has_excluded_prefix(root):
            parent, r, d, f = root, '', '', ''
            for r, d, f in os.walk(parent, topdown=False): pass
            if not f and not d:
                yield (parent, sha1_sum(parent))

        for fname in files:
            f = join_path(root, fname)
            if has_excluded_prefix(f):
                continue
            #bug 373
            elif os.path.islink(f):
                yield (f, sha1_sum(os.readlink(f), True))
            else:
                yield (f, sha1_sum(f))

def copy_dir(src, dest):
    """copy source dir to destination dir recursively"""
    shutil.copytree(src, dest)

def check_file_hash(filename, hash):
    """Check the files integrity with a given hash"""
    return sha1_file(filename) == hash

def sha1_file(filename):
    """calculate sha1 hash of filename"""
    # Broken links can cause problem!
    try:
        m = sha.new()
        f = file(filename, 'rb')
        for line in f:
            m.update(line)
        return m.hexdigest()
    except IOError:
        raise FileError(_("I/O Error: Cannot calculate SHA1 hash of %s") % filename)

def sha1_data(data):
    """calculate sha1 hash of given data"""
    try:
        m = sha.new()
        m.update(data)
        return m.hexdigest()
    except:
        raise Error(_("Cannot calculate SHA1 hash of given data"))

def uncompress(patchFile, compressType="gz", targetDir=None):
    """uncompresses a file and returns the path of the uncompressed
    file"""
    if targetDir:
        filePath = join_path(targetDir,
                                os.path.basename(patchFile))
    else:
        filePath = os.path.basename(patchFile)

    if compressType == "gz":
        from gzip import GzipFile
        obj = GzipFile(patchFile)
    elif compressType == "bz2":
        from bz2 import BZ2File
        obj = BZ2File(patchFile)

    open(filePath, "w").write(obj.read())
    return filePath


def do_patch(sourceDir, patchFile, level = 0, target = ''):
    """simple function to apply patches.."""
    cwd = os.getcwd()
    os.chdir(sourceDir)
    
    if level == None:
        level = 0
    if target == None:
        target = ''

    check_file(patchFile)
    (successful, lines) = run_batch("patch -p%d %s< %s" % 
                                    (level, target, patchFile))
    if not successful:
        raise Error(_("ERROR: patch (%s) failed: %s") % (patchFile,
                                                         strlist (lines)))

    os.chdir(cwd)


def strip_directory(top, package_name, excludelist=[]):
    for root, dirs, files in os.walk(top):
        for fn in files:
            frpath = join_path(root, fn)
            
            # Some upstream sources have buggy libtool and ltmain.sh with them, 
            # which causes wrong path entries in *.la files. And these wrong path
            # entries sometimes triggers compile-time errors or linkage problems. 
            # Instead of patching all these buggy sources and maintain these patches,
            # PISI removes wrong paths...
            extension = os.path.splitext(frpath)[1]
            if extension == ".la":
                # FIXME: I'm regular expr. idiot, so one can convert this to python...
                os.system("sed -i -e 's~-L/var/tmp/pisi/[[:graph:]]* ~~g' %s" % frpath)
                
            # real path in .pisi package
            p = '/' + removepathprefix(top, frpath)
            strip = True
            for exclude in excludelist:
                if p.startswith(exclude):
                    strip = False
                    ctx.ui.debug("%s [%s]" %(p, "NoStrip"))

            if strip:
                if strip_file(frpath, package_name):
                    ctx.ui.debug("%s [%s]" %(p, "stripped"))
                

def strip_file(filepath, package_name):
    """strip a file"""
    p = os.popen("file \"%s\"" % filepath)
    o = p.read()

    def run_strip(f, flags=""):
        p = os.popen("strip %s %s" %(flags, f))
        ret = p.close()
        if ret:
            ctx.ui.warning(_("strip command failed for file '%s'!") % f)

    def save_elf_debug(f, package_name):
        """copy debug info into /debug/PACKAGE_NAME/file.debug file"""
        try:
            os.makedirs("/debug/%s" % package_name)
        except OSError:
            pass
        p = os.popen("objcopy --only-keep-debug %s /debug/%s/%s.debug" % (f, package_name, os.path.basename(f)))
        ret = p.close()
        if ret:
            ctx.ui.warning(_("objcopy (keep-debug) command failed for file '%s'!") % f)
        
        """mark binary/shared objects to use /debug/PACKAGE_NAME/file.debug"""
        p = os.popen("objcopy --add-gnu-debuglink=/debug/%s/%s.debug %s" % (package_name, os.path.basename(f), f))
        ret = p.close()
        if ret:
            ctx.ui.warning(_("objcopy (add-debuglink) command failed for file '%s'!") % f)

    if "current ar archive" in o:
        run_strip(filepath, "-g")
        return True

    elif "SB executable" in o:
        if ctx.config.values.build.debug == "True":
            save_elf_debug(filepath, package_name)
        run_strip(filepath)
        return True

    elif "SB shared object" in o:
        if ctx.config.values.build.debug == "True":
            save_elf_debug(filepath, package_name)
        run_strip(filepath, "--strip-unneeded")
        # FIXME: warn for TEXTREL
        return True

    return False

def partition_freespace(directory):
    """ returns free space of given directory's partition """
    st = os.statvfs(directory)
    return st[statvfs.F_BSIZE] * st[statvfs.F_BFREE]

def clean_locks(top = '.'):
    for root, dirs, files in os.walk(top):
        for fn in files:
            if fn.endswith('.lock'):
                path = join_path(root, fn)
                ctx.ui.info(_('Removing lock %s'), path)
                os.unlink(path)

########################################
# Package/Repository Related Functions #
########################################

def package_name(name, version, release, build, prependSuffix=True):
    fn = name + '-' + version + '-' + release
    if build:
        fn += '-' + str(build)
    if prependSuffix:
        fn += ctx.const.package_suffix
    return fn

def is_package_name(fn, package_name = None):
    "check if fn is a valid filename for given package_name"
    "if not given a package name, see if fn fits the package name rules"
    if (package_name==None) or fn.startswith(package_name + '-'):
        if fn.endswith(ctx.const.package_suffix):
            # get version string, skip separator '-'
            verstr = fn[len(package_name) + 1:
                        len(fn)-len(ctx.const.package_suffix)]
            import string
            for x in verstr.split('-'):
                # weak rule: version components after '-' start with a digit
                if x is '' or (not x[0] in string.digits):
                    return False
            return True
    return False

def env_update():

    ctx.ui.info(_('Updating environment...'))
    env_dir = join_path(ctx.config.dest_dir(), "/etc/env.d")
    profile_file = join_path(ctx.config.dest_dir(), "/etc/profile.env")
    ldconf_file = join_path(ctx.config.dest_dir(), "/etc/ld.so.conf")

    if not os.path.exists(env_dir):
        os.makedirs(env_dir, 0755)

    list = []
    for file in os.listdir(env_dir):
        if not os.path.isdir(join_path(env_dir, file)):
            list.append(file)

    list.sort()

    keys = {}
    for file in list:
        f = open(join_path(env_dir, file), "r")
        for line in f:
            if not re.search("^#", line.strip()):
                currentLine = line.strip().split("=")

                try:
                    if keys.has_key(currentLine[0]):
                        keys[currentLine[0]] += ":" + currentLine[1].replace("\"", "")
                    else:
                        keys[currentLine[0]] = currentLine[1].replace("\"", "")
                except IndexError:
                    pass

    # generate profile.env
    f = open(profile_file, "w")
    for key in keys:
        f.write("export %s=\"%s\"\n" % (key, keys[key]))
    f.close()

    # generate ld.so.conf
    f = open(ldconf_file, "w")
    if keys.has_key("LDPATH"):
        for path in keys["LDPATH"].split(":"):
            f.write("%s\n" % path)
    f.close()

    # run ldconfig
    run_batch("/sbin/ldconfig -X -r %s" % ctx.config.dest_dir())
    
def pure_package_name(package_name):
    "return pure package name from given string"
    "ex: package_name=tasma-1.0.3-5-2.pisi, returns tasma"
 
    if package_name.endswith(ctx.const.package_suffix):
        package_name = package_name.rstrip(ctx.const.package_suffix)

    return '-'.join([part for part in package_name.split('-') if part[0] not in string.digits])
 
def generate_pisi_file(patchFile, fromFile, toFile):
    run_batch("xdelta patch %s %s %s" % (patchFile, fromFile, toFile))

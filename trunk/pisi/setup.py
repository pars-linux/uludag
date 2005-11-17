#!/usr/bin/env python
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
# Authors: {eray,gurer}@uludag.org.tr

import os
import shutil
import glob
import sys
from distutils.core import setup
from distutils.command.install import install

sys.path.insert(0, '.')
import pisi

i18n_domain = "pisi"
i18n_languages = "tr"

class Install(install):
    def run(self):
        install.run(self)
        self.installi18n()
        self.installdoc()
    
    def installi18n(self):
        for lang in i18n_languages.split(' '):
            print "Installing '%s' translations..." % lang
            os.popen("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            if not self.root:
                self.root = "/"
            destpath = os.path.join(self.root, "usr/share/locale/%s/LC_MESSAGES" % lang)
            try:
                os.makedirs(destpath)
            except:
                pass
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "%s.mo" % i18n_domain))

    def installdoc(self): #TODO: not decided if we have to
        os.chdir('doc')
        for tex in glob.glob('*.tex'):
            print 'Compiling', tex
            os.system('latex %s' % tex)
            dvi = tex[:-3] + 'dvi'
            ps = tex[:-3] + 'ps'
            os.system('dvips %s -o %s' % (dvi, ps))
            destpath = os.path.join(self.root, "usr/share/doc/pisi")
            try:
                os.makedirs(destpath)
            except:
                pass
            print 'Installing', ps          
            shutil.copy(ps, os.path.join(destpath, ps))
        os.chdir('..')

setup(name="pisi",
    version= pisi.__version__,
    description="PISI (Packages Installed Successfully as Intended)",
    long_description="PISI is the package management system of Pardus Linux.",
    license="GNU GPL2",
    author="Pardus Developers",
    author_email="pisi@uludag.org.tr",
    url="http://www.uludag.org.tr/eng/pisi/",
    package_dir = {'': ''},
    packages = ['pisi', 'pisi.cli', 'pisi.actionsapi', 'pisi.pxml'],
    scripts = ['pisi-cli', 'tools/ebuild2pisi.py', 'tools/repostats.py',
               'tools/find-lib-deps.py', 'tools/update-environ.py'],
    cmdclass = {
        'install' : Install
    }
    )

# the below stuff is really nice but we already have a version
# we can use this stuff for svn snapshots in a separate
# script -- exa

PISI_VERSION = pisi.__version__

def getRevision():
    import os
    try:
        p = os.popen("svn info 2> /dev/null")
        for line in p.readlines():
            line = line.strip()
            if line.startswith("Revision:"):
                return line.split(":")[1].strip()
    except:
        pass

    # doesn't working in a Subversion directory
    return None

def getVersion():
    rev = getRevision()
    if rev:
        return "-r".join([PISI_VERSION, rev])
    else:
        return PISI_VERSION

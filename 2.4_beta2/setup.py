#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 - 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import shutil
import glob
import sys
import inspect
import tempfile
from distutils.core import setup
from distutils.command.build import build
from distutils.command.install import install

sys.path.insert(0, '.')
import pisi

IN_FILES = ("pisi.xml.in",)
PROJECT = "pisi"
MIMEFILE_DIR = "usr/share/mime/packages"


class Build(build):
    def run(self):
        build.run(self)

        self.mkpath(self.build_base)

        for in_file in IN_FILES:
            name, ext = os.path.splitext(in_file)
            self.spawn(["intltool-merge", "-x", "po", in_file, os.path.join(self.build_base, name)])


class BuildPo(build):
    def run(self):
        build.run(self)
        self.build_po()

    def build_po(self):
        import optparse
        files = tempfile.mkstemp()[1]
        filelist = []

        # Include optparse module path to translate
        optparse_path = os.path.abspath(optparse.__file__).rstrip("co")

        # Collect headers for mimetype files
        for filename in IN_FILES:
            os.system("intltool-extract --type=gettext/xml %s" % filename)

        for root,dirs,filenames in os.walk("pisi"):
            for filename in filenames:
                if filename.endswith(".py"):
                    filelist.append(os.path.join(root, filename))

        filelist.extend(["pisi-cli", "pisi.xml.in.h", optparse_path])
        filelist.sort()
        with open(files, "w") as _files:
            _files.write("\n".join(filelist))

        # Generate POT file
        os.system("xgettext -L Python \
                            --default-domain=%s \
                            --keyword=_ \
                            --keyword=N_ \
                            --files-from=%s \
                            -o po/%s.pot" % (PROJECT, files, PROJECT))

        # Update PO files
        for item in glob.glob1("po", "*.po"):
            print "Updating .. ", item
            os.system("msgmerge --update --no-wrap --sort-by-file po/%s po/%s.pot" % (item, PROJECT))

        # Cleanup
        os.unlink(files)
        for f in filelist:
            if not f.endswith(".h"):
                continue
            try:
                os.unlink(f)
            except OSError:
                pass


class Install(install):
    def run(self):
        install.run(self)
        self.installi18n()
        self.installdoc()
        self.generateConfigFile()

    def installi18n(self):
        for name in os.listdir('po'):
            if not name.endswith('.po'):
                continue
            lang = name[:-3]
            print "Installing '%s' translations..." % lang
            os.popen("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            if not self.root:
                self.root = "/"
            destpath = os.path.join(self.root, "usr/share/locale/%s/LC_MESSAGES" % lang)
            if not os.path.exists(destpath):
                os.makedirs(destpath)
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "pisi.mo"))

    def installdoc(self):
        destpath = os.path.join(self.root, "usr/share/doc/pisi")
        if not os.path.exists(destpath):
            os.makedirs(destpath)
        os.chdir('doc')
        for pdf in glob.glob('*.pdf'):
            print 'Installing', pdf
            shutil.copy(pdf, os.path.join(destpath, pdf))
        os.chdir('..')

    def generateConfigFile(self):
        import pisi.configfile
        destpath = os.path.join(self.root, "etc/pisi/")
        if not os.path.exists(destpath):
            os.makedirs(destpath)

        confFile = os.path.join(destpath, "pisi.conf")
        if os.path.isfile(confFile): # Don't overwrite existing pisi.conf
            return

        pisiconf = open(confFile, "w")

        klasses = inspect.getmembers(pisi.configfile, inspect.isclass)
        defaults = [klass for klass in klasses if klass[0].endswith('Defaults')]

        for d in defaults:
            section_name = d[0][:-len('Defaults')].lower()
            pisiconf.write("[%s]\n" % section_name)

            section_members = [m for m in inspect.getmembers(d[1]) \
                               if not m[0].startswith('__') \
                               and not m[0].endswith('__')]

            for member in section_members:
                if member[1] == None or member[1] == "":
                    pisiconf.write("# %s = %s\n" % (member[0], member[1]))
                else:
                    pisiconf.write("%s = %s\n" % (member[0], member[1]))
            pisiconf.write('\n')



setup(name="pisi",
    version= pisi.__version__,
    description="PiSi (Packages Installed Successfully as Intended)",
    long_description="PiSi is the package management system of Pardus Linux.",
    license="GNU GPL2",
    author="Pardus Developers",
    author_email="pisi@pardus.org.tr",
    url="http://www.pardus.org.tr/eng/pisi/",
    package_dir = {'': ''},
    packages = ['pisi', 'pisi.cli', 'pisi.operations', 'pisi.actionsapi', 'pisi.pxml', 'pisi.scenarioapi', 'pisi.db'],
    scripts = ['pisi-cli', 'scripts/lspisi', 'scripts/unpisi', 'scripts/check-newconfigs.py', 'scripts/revdep-rebuild'],
    cmdclass = {'build' : Build,
                'build_po' : BuildPo,
                'install' : Install}
    )

# the below stuff is really nice but we already have a version
# we can use this stuff for svn snapshots in a separate
# script, or with a parameter I don't know -- exa

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

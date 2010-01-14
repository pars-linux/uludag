#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import glob
import shutil
import sys

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install

from src.migration import about as about

def update_messages():
    # Create empty directory
    os.system("rm -rf .tmp")
    os.makedirs(".tmp")
    # Collect UI files
    for filename in glob.glob1("src/migration/gui/ui", "*.ui"):
        os.system("/usr/kde/4/bin/pykde4uic -o .tmp/ui_%s.py src/migration/gui/ui/%s" % (filename.split(".")[0], filename))
    # Collect Python files
    for filename in glob.glob1("src/migration/gui", "*.py"):
        shutil.copy("src/migration/gui/%s" % filename, ".tmp")
    # Generate POT file
    os.system("xgettext --default-domain=%s --keyword=_ --keyword=i18n --keyword=ki18n -o po/%s.pot .tmp/*" % (about.catalog, about.catalog))
    # Update PO files
    for item in os.listdir("po"):
        if item.endswith(".po"):
            os.system("msgmerge -q -o .tmp/temp.po po/%s po/%s.pot" % (item, about.catalog))
            os.system("cp .tmp/temp.po po/%s" % item)
    # Remove temporary directory
    os.system("rm -rf .tmp")

def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass

class Build(build):
    def run(self):
        # Clear all
        os.system("rm -rf build")
        # Copy codes
        os.system("cp -R src build/")
        # Copy compiled UIs and RCs
        for filename in glob.glob1("src/migration/gui/ui", "*.ui"):
            os.system("/usr/kde/4/bin/pykde4uic -o build/migration/gui/ui/%s.py src/migration/gui/ui/%s" % (filename.split(".")[0], filename))
        for filename in glob.glob1("src/migration/gui/ui", "*.qrc"):
            os.system("/usr/bin/pyrcc4 src/migration/gui/ui/%s -o build/%s_rc.py" % (filename, filename.split(".")[0]))

class Install(install):
    def run(self):
        os.system("./setup.py build")
        if self.root:
            kde_dir = "%s/usr/kde/4" % self.root
        else:
            kde_dir = "/usr/kde/4"
        bin_dir = os.path.join(kde_dir, "bin")
        locale_dir = os.path.join(kde_dir, "share/locale")
        autostart_dir = os.path.join(kde_dir, "share/applications/kde4")
        project_dir = os.path.join(kde_dir, "share/apps", about.appName)
        # Make directories
        makeDirs(bin_dir)
        #makeDirs(locale_dir)
        makeDirs(autostart_dir)
        makeDirs(project_dir)
        # Install desktop files
        for filename in glob.glob1("data", "*.desktop"):
            shutil.copy("data/%s" % filename, autostart_dir)
        # Install codes
        os.system("cp -R build/* %s/" % project_dir)
        # Install locales
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            try:
                os.makedirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            except OSError:
                pass
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % about.catalog))
        # Rename
        #shutil.move(os.path.join(project_dir, "application.py"), os.path.join(project_dir, "%s.py" % about.appName))
        # Modes
        os.chmod(os.path.join(project_dir, "%s.py" % about.appName), 0755)
        # Symlink
        try:
            if self.root:
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
            else:
                os.symlink(os.path.join(project_dir, "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
        except OSError:
            pass


if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(
      name              = about.appName,
      version           = about.version,
      description       = unicode(about.description),
      license           = unicode(about.license),
      author            = "",
      author_email      = about.bugEmail,
      url               = about.homePage,
      packages          = [''],
      package_dir       = {'': ''},
      data_files        = [],
      cmdclass          = {
                            'build': Build,
                            'install': Install,
                          }
)

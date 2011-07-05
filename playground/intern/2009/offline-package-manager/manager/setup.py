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

from src import about

def update_messages():
    # Create empty directory
    os.system("rm -rf .tmp")
    os.makedirs(".tmp")
    # Collect UI files
    for filename in glob.glob1("ui", "*.ui"):
        os.system("/usr/kde/4/bin/pykde4uic -o .tmp/ui_%s.py ui/%s" % (filename.split(".")[0], filename))
    # Collect Python files
    os.system("cp -R src/* .tmp/")
    # Generate POT file
    os.system("find .tmp -name '*.py' | xargs xgettext --default-domain=%s --keyword=_ --keyword=i18n --keyword=ki18n -o po/%s.pot" % (about.catalog, about.catalog))
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
        print "Copying PYs..."
        os.system("cp -R src/ build/")
        # Copy icons
        print "Copying Images..."
        os.system("cp -R data/ build/")
        # Copy compiled UIs and RCs
        print "Generating UIs..."
        for filename in glob.glob1("ui", "*.ui"):
            os.system("/usr/kde/4/bin/pykde4uic -o build/ui_%s.py ui/%s" % (filename.split(".")[0], filename))
        print "Generating RCs..."
        for filename in glob.glob1("data", "*.qrc"):
            os.system("/usr/bin/pyrcc4 data/%s -o build/%s_rc.py" % (filename, filename.split(".")[0]))

class Install(install):
    def run(self):
        if not os.path.exists("build/"):
            os.system("./setup.py build")
        if self.root:
            mime_icons_dir = "%s/usr/share/icons/hicolor" % self.root
            icon_dir = "%s/usr/share/icons/hicolor/128x128/apps" % self.root
            kde_dir = "%s/usr/kde/4" % self.root
        else:
            mime_icons_dir = "/usr/share/icons/hicolor"
            icon_dir = "/usr/share/icons/hicolor/128x128/apps"
            kde_dir = "/usr/kde/4"
        bin_dir = os.path.join(kde_dir, "bin")
        mime_dir = os.path.join(kde_dir, "share/mime/packages")
        locale_dir = os.path.join(kde_dir, "share/locale")
        apps_dir = os.path.join(kde_dir, "share/applications/kde4")
        project_dir = os.path.join(kde_dir, "share/apps", about.appName)
        # Make directories
        print "Making directories..."
        makeDirs(mime_icons_dir)
        makeDirs(icon_dir)
        makeDirs(mime_dir)
        makeDirs(bin_dir)
        makeDirs(locale_dir)
        makeDirs(apps_dir)
        makeDirs(project_dir)

        # Install desktop files
        print "Installing desktop files..."
        shutil.copy("data/package-manager.desktop", apps_dir)
        shutil.copy("data/package-manager.png", icon_dir)
        shutil.copy("data/packagemanager-helper.desktop", apps_dir)
        shutil.copy("data/packagemanager-offline.desktop", apps_dir)
        shutil.copy("data/package-manager.xml", mime_dir)

        # Install icons
        for size in ["16x16", "32x32", "48x48", "64x64"]:
            mime_size_dir = "%s/%s/mimetypes/" % (mime_icons_dir, size)
            makeDirs(mime_size_dir)
            shutil.copy("data/package-manager-%s.png" % size, "%s/application-x-pisi.png" % mime_size_dir)

        # Install codes
        print "Installing codes..."
        os.system("cp -R build/* %s/" % project_dir)
        print "Installing help files..."
        os.system("cp -R help %s/" % project_dir)
        # Install locales
        print "Installing locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            try:
                os.makedirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            except OSError:
                pass
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % about.catalog))
        # Rename
        print "Renaming application.py..."
        shutil.move(os.path.join(project_dir, "main.py"), os.path.join(project_dir, "%s.py" % about.appName))
        # Modes
        print "Changing file modes..."
        os.chmod(os.path.join(project_dir, "%s.py" % about.appName), 0755)
        os.chmod(os.path.join(project_dir, "pm-install.py"), 0755)
        os.chmod(os.path.join(project_dir, "pm-offline.py"), 0755)
        # Symlink
        try:
            if self.root:
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "pm-install.py"), os.path.join(bin_dir, "pm-install"))
            else:
                os.symlink(os.path.join(project_dir, "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
                os.symlink(os.path.join(project_dir, "pm-install.py"), os.path.join(bin_dir, "pm-install"))
        except OSError, e:
            pass

        # Symlink for pm-offline
        try:
            if self.root:
		os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "pm-offline.py"), os.path.join(bin_dir, "pm-offline"))
            else:
		os.symlink(os.path.join(project_dir, "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
                os.symlink(os.path.join(project_dir, "pm-offline.py"), os.path.join(bin_dir, "pm-offline"))
        except OSError, e:
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

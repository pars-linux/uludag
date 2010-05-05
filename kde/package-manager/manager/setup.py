#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
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
from distutils.command.clean import clean
from distutils.command.install import install

PROJECT = 'package-manager'
__version = '2.2.0'

def update_messages():
    # Create empty directory
    os.system("rm -rf .tmp")
    os.makedirs(".tmp")
    # Collect UI files
    for filename in glob.glob1("ui", "*.ui"):
        os.system("/usr/bin/pyuic4 -o .tmp/ui_%s.py ui/%s -g %s" % (filename.split(".")[0], filename, PROJECT))
    # Collect Python files
    os.system("cp -R src/* .tmp/")
    # Generate POT file
    os.system("find .tmp -name '*.py' | xargs xgettext --default-domain=%s --keyword=_ --keyword=i18n --keyword=ki18n -o po/%s.pot" % (PROJECT, PROJECT))
    # Update PO files
    for item in os.listdir("po"):
        if item.endswith(".po"):
            os.system("msgmerge -q -o .tmp/temp.po po/%s po/%s.pot" % (item, PROJECT))
            os.system("cp .tmp/temp.po po/%s" % item)
    # Remove temporary directory
    os.system("rm -rf .tmp")

def makeDirs(dir):
    if not os.path.exists(dir):
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
            os.system("/usr/bin/pyuic4 -o build/ui_%s.py ui/%s -g %s" % (filename.split(".")[0], filename, PROJECT))
        print "Generating RCs..."
        for filename in glob.glob1("data", "*.qrc"):
            os.system("/usr/bin/pyrcc4 data/%s -o build/%s_rc.py" % (filename, filename.split(".")[0]))

class Install(install):
    def run(self):
        os.system("./setup.py build")
        if self.root:
            mime_icons_dir = "%s/usr/share/icons/hicolor" % self.root
            icon_dir = "%s/usr/share/icons/hicolor/128x128/apps" % self.root
            kde_dir = "%s/usr/kde/4" % self.root
        else:
            mime_icons_dir = "/usr/share/icons/hicolor"
            icon_dir = "/usr/share/icons/hicolor/128x128/apps"
            kde_dir = "/usr/kde/4"
        bin_dir = "/usr/bin"
        mime_dir = "/usr/share/mime/packages"
        locale_dir = "/usr/share/locale"
        apps_dir = "/usr/share/applications"
        project_dir = os.path.join("/usr/share", PROJECT)
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
        shutil.copy("data/%s.desktop" % PROJECT, apps_dir)
        shutil.copy("data/%s.png" % PROJECT, icon_dir)
        shutil.copy("data/packagemanager-helper.desktop", apps_dir)
        shutil.copy("data/%s.xml" % PROJECT, mime_dir)

        # Install icons
        for size in ["16x16", "32x32", "48x48", "64x64"]:
            mime_size_dir = "%s/%s/mimetypes/" % (mime_icons_dir, size)
            makeDirs(mime_size_dir)
            shutil.copy("data/%s-%s.png" % (PROJECT, size), "%s/application-x-pisi.png" % mime_size_dir)

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
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % PROJECT))
        # Rename
        print "Renaming application.py..."
        shutil.move(os.path.join(project_dir, "main.py"), os.path.join(project_dir, "%s.py" % PROJECT))
        # Modes
        print "Changing file modes..."
        os.chmod(os.path.join(project_dir, "%s.py" % PROJECT), 0755)
        os.chmod(os.path.join(project_dir, "pm-install.py"), 0755)
        # Symlink
        try:
            if self.root:
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.py" % PROJECT), os.path.join(bin_dir, PROJECT))
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "pm-install.py"), os.path.join(bin_dir, "pm-install"))
            else:
                os.symlink(os.path.join(project_dir, "%s.py" % PROJECT), os.path.join(bin_dir, PROJECT))
                os.symlink(os.path.join(project_dir, "pm-install.py"), os.path.join(bin_dir, "pm-install"))
        except OSError, e:
            pass

class Uninstall(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        print 'Uninstalling ...'
        data_dir    = '/usr/share/%s' % PROJECT
        if os.path.exists(data_dir):
            print ' removing: ', data_dir
            shutil.rmtree(data_dir)
        executable = '/usr/bin/%s' % PROJECT
        if os.path.exists(executable):
            print ' removing: ', executable
            os.unlink(executable)

class Clean(clean):
    def run(self):
        print 'Cleaning ...'
        os.system('find -name *.pyc|xargs rm -rf')
        os.system('find -name *.mo|xargs rm -rf')
        for dirs in ('build', 'dist'):
            if os.path.exists(dirs):
                print ' removing: ', dirs
                shutil.rmtree(dirs)
        clean.run(self)

if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(
      name              = PROJECT,
      version           = __version,
      description       = unicode('Package Manager'),
      license           = unicode('GPL'),
      author            = '',
      author_email      = 'bugs@pardus.org.tr',
      url               = 'http://www.pardus.org.tr/eng/projects',
      packages          = [''],
      package_dir       = {'': ''},
      data_files        = [],
      cmdclass          = {
                            'build': Build,
                            'install': Install,
                            'uninstall':Uninstall,
                            'clean':Clean
                          }
)

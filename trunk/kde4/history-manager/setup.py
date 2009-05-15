#!/usr/bin/env python
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import re
import glob
import shutil

from distutils.core import setup, Extension
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.spawn import find_executable, spawn

from src.about import aboutData
from src.about import version as VERSION

PROJECT = str(aboutData.appName())

class UpdateMessages(install):
    def run(self):
        try:
            os.makedirs(".tmp")
        except OSError:
            pass
        for filename in glob.glob1("ui", "*.ui"):
            os.system("/usr/kde/4/bin/pykde4uic -o .tmp/%s.py ui/%s" % (filename.split(".")[0], filename))
        for filename in glob.glob1("src", "*.py"):
            shutil.copy("src/%s" % filename, ".tmp")
        os.system("xgettext --default-domain=comar --keyword=_ --keyword=i18n --keyword=ki18n -o po/%s.pot .tmp/*" % PROJECT)
        for item in os.listdir("po"):
            if item.endswith(".po"):
                os.system("msgmerge -q -o temp.po po/%s po/%s.pot" % (item, PROJECT))
                os.system("cp temp.po po/%s" % item)
        os.system("rm -f temp.po")

class Install(install):
    def run(self):
        if self.root:
            kde_dir = "%s/usr/kde/4" % self.root
        else:
            kde_dir = "/usr/kde/4"
        bin_dir = os.path.join(kde_dir, "bin")
        project_dir = os.path.join(kde_dir, "share/apps", PROJECT)
        service_dir = os.path.join(kde_dir, "share/kde4/services")
        locale_dir = os.path.join(kde_dir, "share/locale")
        print "Making directories..."
        try:
            os.makedirs(project_dir)
            os.makedirs(service_dir)
            os.makedirs(locale_dir)
        except OSError:
            pass
        # Copy compiled UIs and RC
        print "Generating UIs..."
        for filename in glob.glob1("ui", "*.ui"):
            os.system("/usr/kde/4/bin/pykde4uic -o %s/%s.py ui/%s" % (project_dir, filename.split(".")[0], filename))
        print "Copying UIs..."
        os.system("/usr/bin/pyrcc4 resources/data.qrc -o %s/data_rc.py" % project_dir)
        # Copy service file
        print "Copying desktop files..."
        for filename in glob.glob1("resources", "*.desktop"):
            shutil.copy("resources/%s" % filename, service_dir)
        # Copy codes
        print "Copying Python files..."
        for filename in glob.glob1("src", "*.py"):
            shutil.copy("src/%s" % filename, project_dir)
        # Copy locales
        print "Copying locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            try:
                os.makedirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            except OSError:
                pass
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % PROJECT))
        # Rename
        print "Renaming main.py..."
        shutil.move(os.path.join(project_dir, "main.py"), os.path.join(project_dir, "%s.py" % PROJECT))
        # Symlink
        print "Creating symlinks..."
        if not os.path.exists(os.path.join(project_dir, "%s.py" % PROJECT)):
            os.symlink(os.path.join(project_dir, PROJECT), os.path.join(project_dir, "%s.py" % PROJECT))
            os.symlink(os.path.join(project_dir, PROJECT), os.path.join(bin_dir, PROJECT))
        print "Changing file modes..."
        os.chmod(os.path.join(project_dir, "%s.py" % PROJECT), 0755)


setup(
      name              = PROJECT,
      version           = VERSION,
      description       = str(aboutData.shortDescription()),
      license           = str(aboutData.licenseName(0)),
      author            = str(aboutData.authors()[0].name()),
      author_email      = "bugs@pardus.org.tr",
      url               = str(aboutData.homepage()),
      packages          = [''],
      package_dir       = {'': ''},
      data_files        = [],
      cmdclass          = {
                            'install': Install,
                            'update_messages': UpdateMessages,
                          }
     )

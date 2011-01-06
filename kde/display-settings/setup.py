#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys
import glob
import tempfile

from distutils.core import setup
from distutils.command.build import build
from distutils.command.install import install

from src.displaysettings import about

PROJECT = about.appName

# For future PDS integration, uncomment the following lines
# when ready.
if True:#'kde4' in sys.argv:
    #sys.argv.remove('kde4')
    FOR_KDE_4 = True
    print 'UI files will be created for KDE 4..'

def makeDirs(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass

def update_messages():
    files = tempfile.mkstemp()[1]

    # Collect UI files
    filelist = []
    for filename in glob.glob1("ui", "*.ui"):
        if FOR_KDE_4:
            os.system("/usr/kde/4/bin/pykde4uic -o ui/ui_%s.py ui/%s" % (filename.split(".")[0], filename))
        else:
            os.system("/usr/bin/pyuic4 -o ui/ui_%s.py ui/%s -g %s" % (filename.split(".")[0], filename, PROJECT))

    # Collect headers for desktop files
    for filename in glob.glob("data/*.desktop.in"):
        os.system("intltool-extract --type=gettext/ini %s" % filename)

    filelist = os.popen("find data src ui -name '*.h' -o -name '*.py'").read().strip().split("\n")
    filelist.sort()
    with open(files, "w") as _files:
        _files.write("\n".join(filelist))

    # Generate POT file
    os.system("xgettext --default-domain=%s \
                        --keyword=_ \
                        --keyword=N_ \
                        --keyword=i18n \
                        --keyword=ki18n \
                        --kde \
                        -ci18n -ki18n:1 -ki18nc:1c,2 -ki18np:1,2 -ki18ncp:1c,2,3 -ktr2i18n:1 \
                        -kI18N_NOOP:1 -kI18N_NOOP2:1c,2 -kaliasLocale -kki18n:1 -kki18nc:1c,2 \
                        -kki18np:1,2 -kki18ncp:1c,2,3 \
                        --files-from=%s \
                        -o po/%s.pot" % (PROJECT, files, PROJECT))

    # Update PO files
    for item in glob.glob1("po", "*.po"):
        os.system("msgmerge --update --no-wrap --sort-by-file po/%s po/%s.pot" % (item, PROJECT))

    # Cleanup
    os.unlink(files)
    for f in [_f for _f in filelist if _f.startswith("ui/") or _f.endswith(".h")]:
        try:
            os.unlink(f)
        except OSError:
            pass

class Build(build):
    def run(self):
        # Clear all
        os.system("rm -rf build")

        makeDirs("build/app")
        makeDirs("build/lib/xcb")

        # Copy codes
        print "Copying PYs..."
        os.system("cp -R src/* build/app/")

        # Create xcb binding
        os.system("python xcb/py_client.py xcb/nvctrl.xml")
        self.move_file("nvctrl.py", "build/lib/xcb/")

        # Copy compiled UIs and RCs
        print "Generating UIs..."
        for filename in glob.glob1("ui", "*.ui"):
            os.system("/usr/kde/4/bin/pykde4uic -o build/app/%s/ui_%s.py ui/%s" % (about.modName, filename.split(".")[0], filename))

        print "Generating RCs..."
        for filename in glob.glob1("data", "*.qrc"):
            os.system("/usr/bin/pyrcc4 data/%s -o build/app/%s_rc.py" % (filename, filename.split(".")[0]))

class Install(install):
    def run(self):
        install.run(self)

        if self.root:
            kde_dir = "%s/usr/kde/4" % self.root
        else:
            kde_dir = "/usr/kde/4"

        bin_dir = os.path.join(kde_dir, "bin")
        locale_dir = os.path.join(kde_dir, "share/locale")
        service_dir = os.path.join(kde_dir, "share/kde4/services")
        apps_dir = os.path.join(kde_dir, "share/applications/kde4")
        project_dir = os.path.join(kde_dir, "share/apps", about.appName)

        # Make directories
        print "Making directories..."
        makeDirs(bin_dir)
        makeDirs(locale_dir)
        makeDirs(service_dir)
        makeDirs(apps_dir)
        makeDirs(project_dir)

        # Install desktop files
        print "Installing desktop files..."

        for filename in glob.glob("data/*.desktop.in"):
            os.system("intltool-merge -d po %s %s" % (filename, filename[:-3]))

        self.copy_file("data/kcm_%s.desktop" % about.modName, service_dir)
        self.copy_file("data/kcm_displaydevices.desktop", service_dir)
        self.copy_file("data/%s.desktop" % about.modName, apps_dir)

        # Install codes
        print "Installing codes..."
        os.system("cp -R build/app/* %s/" % project_dir)

        # Install locales
        print "Installing locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            try:
                os.makedirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            except OSError:
                pass
            self.copy_file("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % about.catalog))

        # Rename
        #print "Renaming application.py..."
        #self.move_file(os.path.join(project_dir, "application.py"), os.path.join(project_dir, "%s.py" % about.appName))

        # Modes
        print "Changing file modes..."
        os.chmod(os.path.join(project_dir, "%s.sh" % about.appName), 0755)

        # Symlink
        try:
            if self.root:
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.sh" % about.appName), os.path.join(bin_dir, about.appName))
            else:
                os.symlink(os.path.join(project_dir, "%s.sh" % about.appName), os.path.join(bin_dir, about.appName))
        except OSError:
            pass


if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(
      name              = about.appName,
      version           = about.version,
      description       = str(about.description.toString()),
      license           = str(about.aboutData.licenseName(about.aboutData.ShortName)),
      author            = "Pardus Developers",
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

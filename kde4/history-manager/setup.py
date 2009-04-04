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

PROJECT     = str(aboutData.appName())
DESKTOPFILE = "settings-history-manager.desktop"
KDEDIR      = "/usr/kde/4"

def getRevision():
    import os
    try:
        p = os.popen("svn info 2> /dev/null")
        for line in p.readlines():
            line = line.strip()
            if line.startswith("Revision:"):
                return line.split(":")[1].strip()
    except:
        return "UNKNOWN"

def data_files():
    return glob.glob1("src","*.py")

def py_file_name(ui_file):
    return ui_file.split('.')[0] + '.py'

def ui_files():
    return glob.glob1("ui","*.ui")

class Build(build):

    def compile_ui(self, ui_file):
        pyuic_exe = find_executable('pykde4uic')
        print ('%s -o src/%s ui/%s' % (pyuic_exe, py_file_name(ui_file), ui_file))
        os.system('%s -o src/%s ui/%s' % (pyuic_exe, py_file_name(ui_file), ui_file))

    def run(self):
        for path in ui_files():
            self.compile_ui(path)
        os.system("pyrcc4 resources/data.qrc -o src/data_rc.py")
        build.run(self)

class Clean(clean):

    def run(self):
        clean.run(self)
        if os.path.exists("src/data_rc.py"):
            os.unlink("src/data_rc.py")

class Uninstall(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        project_dir = os.path.join(KDEDIR, "share/apps", PROJECT)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        service_file = os.path.join(KDEDIR, "share/kde4/services", DESKTOPFILE)
        if os.path.exists(service_file):
            os.unlink(service_file)

i18n_domain = PROJECT
i18n_languages = ["tr"]

class Install(install):
    def run(self):
        for lang in i18n_languages:
            print "Installing '%s' translations..." % lang
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            destpath = os.path.join(KDEDIR, "share/locale/%s/LC_MESSAGES/" % lang)
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "%s.mo" % i18n_domain))
        project_dir = os.path.join(KDEDIR, "share/apps", PROJECT)
        try:
            os.makedirs(project_dir)
        except:
            pass
        for path in data_files():
            shutil.copyfile(os.path.join("src",path), os.path.join(project_dir,path))
        service_file = os.path.join(KDEDIR, "share/kde4/services", DESKTOPFILE)
        shutil.copy(os.path.join("src/",DESKTOPFILE), service_file)
        shutil.move(os.path.join(project_dir,"main.py"), os.path.join(project_dir,PROJECT))
        os.link(os.path.join(project_dir,PROJECT), os.path.join(project_dir,PROJECT+'.py'))
        os.chmod(os.path.join(project_dir,PROJECT+'.py'),0755)

setup(
      name              = PROJECT,
      version           = getRevision(),
      description       = str(aboutData.shortDescription()),
      license           = str(aboutData.licenseName(0)),
      author            = str(aboutData.authors()[0].name()),
      author_email      = "bugs@pardus.org.tr",
      url               = str(aboutData.homepage()),
      packages          = [''],
      package_dir       = {'': ''},
      data_files        = [],
      cmdclass          = {
                            'build' : Build,
                            'clean' : Clean,
                            'install': Install,
                            'uninstall': Uninstall
                          }
     )

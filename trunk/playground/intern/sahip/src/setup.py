#!/usr/bin/env python
#
# Copyright (C) 2005-2007 TUBITAK/UEKAE
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
from PyQt4 import pyqtconfig
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_lib
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.command.install import install
from distutils.spawn import find_executable, spawn

import sahip

SAHIP_VERSION = sahip.__version__

def getVersion():
    return SAHIP_VERSION

def py_file_name(ui_file):
    return os.path.splitext(ui_file)[0] + '.py'


def qt_ui_files():
    p = "sahip/*.ui"
    return glob.glob(p)

def data_files():
    p = "sahip/images/*"
    return glob.glob(p)
def resource_files():
    p = "sahip/*.qrc"
    return glob.glob(p)	

##
# build command
class SahipBuild(build):
    
    

    def add_gettext_support(self, ui_file):
        # hacky, too hacky. but works...
        py_file = py_file_name(ui_file)
        # lines in reverse order
        lines =  ["\n_ = __trans.ugettext\n",
                  "\n__trans = gettext.translation('sahip', fallback=True)",
                  "\nimport gettext"]
        f = open(py_file, "r").readlines()
        for l in lines:
            f.insert(1, l)
        x = open(py_file, "w")
        keyStart = "QtGui.QApplication.translate"
        keyEnd = ", None, QtGui.QApplication.UnicodeUTF8)"
        styleKey = "setStyleSheet"
        for l in f:
            if not l.find(keyStart)==-1 and l.find(styleKey)==-1:
                z = "%s(_(" % l.split("(")[0]
                y = l.split(",")[0]+', '
                l = l.replace(y,z)
            l = l.replace(keyEnd,")")
            l = l.replace("resources_rc","sahip.resources_rc")
            x.write(l)

    def compile_ui(self, ui_file):
        pyqt_configuration = pyqtconfig.Configuration()
        pyuic_exe = find_executable('pyuic4', pyqt_configuration.default_bin_dir)
        if not pyuic_exe:
            # Search on the $Path.
            pyuic_exe = find_executable('pyuic4')

        cmd = [pyuic_exe, ui_file, '-o']
        cmd.append(py_file_name(ui_file))
        os.system(' '.join(cmd))

    def run(self):
        for f in qt_ui_files():
            self.compile_ui(f)
            self.add_gettext_support(f)
        os.system("pyrcc4 sahip/resources.qrc -o sahip/resources_rc.py")
        build.run(self)

##
# clean command
class SahipClean(clean):

    def run(self):
        clean.run(self)

        # clean ui generated .py files
        for f in qt_ui_files():
            f = py_file_name(f)
            if os.path.exists(f):
                os.unlink(f)

##
# uninstall command
class SahipUninstall(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        sahip_dir = os.path.join(get_python_lib(), "sahip")
        if os.path.exists(sahip_dir):
            print "removing: ", sahip_dir
            shutil.rmtree(sahip_dir)

        data_dir = "/usr/share/sahip"
        if os.path.exists(data_dir):
            print "removing: ", data_dir
            shutil.rmtree(data_dir)
        bin_path = "/usr/bin/sahip"
        if os.path.exists(bin_path):
            print "removing: ", bin_path
            os.remove(bin_path)
        link_path = "/usr/share/applications/sahip.desktop"
        if os.path.exists(link_path):
            print "removing: ", link_path
            os.remove(link_path)

i18n_domain = "sahip"
i18n_languages = ["tr",
                  "es",
                  "nl"]
""",
                  "it",
                  "fr",
                  "de",
                  "pt_BR",
                  "pl",
                  "ca"]
"""
class I18nInstall(install):
    def run(self):
        install.run(self)
        shutil.copy("sahip/images/sahip.desktop", "/usr/share/applications/sahip.desktop")
        for lang in i18n_languages:
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

setup(name="sahip",
      version= getVersion(),
      description="SAHIP (XML Generator for Kahya)",
      long_description="SAHIP (XML Generator for Kahya (Silent Installer for YALI))",
      license="GNU GPL2",
      author="Ahmet Emre Aladag",
      author_email="emre@jabber.pardus.org.tr",
      url="http://www.emrealadag.com",
      packages = ['sahip'],
      package_dir = {'': ''},
      data_files = [('/usr/share/sahip', resource_files()),
      			('/usr/share/sahip/images', data_files())],
      scripts = ['sahip/sahip'],
      ext_modules = [],
      cmdclass = {
        'build' : SahipBuild,
        'clean' : SahipClean,
        'install': I18nInstall,
        'uninstall': SahipUninstall
        }
    )

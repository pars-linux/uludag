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


def py_file_name(ui_file):
    return os.path.splitext(ui_file)[0] + '.py'


def qt_ui_files():
    p = "sinerji/*.ui"
    return glob.glob(p)

def image_files():
    p = "sinerji/images/*"
    return glob.glob(p)

def resource_files():
    p = "sinerji/*.qrc"
    return glob.glob(p)	

##
# build command
class SinerjiBuild(build):
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
            l = l.replace("resources_rc","sinerji.resources_rc")
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
        os.system("pyrcc4 sinerji/resources.qrc -o sinerji/resources_rc.py")
        build.run(self)

##
# clean command
class SinerjiClean(clean):

    def run(self):
        clean.run(self)

        # clean ui generated .py files
        for f in qt_ui_files():
            f = py_file_name(f)
            if os.path.exists(f):
                os.unlink(f)

##
# uninstall command
class SinerjiUninstall(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        sinerji_dir = os.path.join(get_python_lib(), "sinerji")
        if os.path.exists(sinerji_dir):
            print "removing: ", sinerji_dir
            shutil.rmtree(sinerji_dir)

        data_dir = "/usr/share/sinerji"
        if os.path.exists(data_dir):
            print "removing: ", data_dir
            shutil.rmtree(data_dir)
        bin_path = "/usr/bin/sinerji"
        if os.path.exists(bin_path):
            print "removing: ", bin_path
            os.remove(bin_path)
        link_path = "/usr/share/applications/sinerji.desktop"
        if os.path.exists(link_path):
            print "removing: ", link_path
            os.remove(link_path)

i18n_domain = "sinerji"
i18n_languages = ["tr"]

"""               "es"
                  "nl",
                  "it",
                  "fr",
                  "de",
                  "pt_BR",
                  "es",
                  "pl",
                  "ca"]
"""
class I18nInstall(install):
    def run(self):
        install.run(self)
        shutil.copy("sinerji/images/sinerji.desktop", "/usr/share/applications/sinerji.desktop")
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

setup(name="sinerji",
      version= "0.1",
      description="Sinerji is a fronted for Synergy)",
      license="GNU GPL2",
      author="Fatih Arslan",
      author_email="fatih@arsln.org",
      url="http://blog.arsln.org",
      packages = ['sinerji'],
      package_dir = {'': ''},
      data_files = [('/usr/share/sinerji', resource_files()), ('/usr/share/sinerji/images', image_files())],
      scripts = ['sinerji/sinerji.py'],
      cmdclass = {
        'build' : SinerjiBuild,
        'clean' : SinerjiClean,
        'install': I18nInstall,
        'uninstall': SinerjiUninstall
        }
    )

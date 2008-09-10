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

import arama

ARAMA_VERSION = arama.__version__

def getVersion():
    return ARAMA_VERSION

def py_file_name(ui_file):
    return os.path.splitext(ui_file)[0] + '.py'

def data_files():
    p = 'arama/*'
    return glob.glob(p)

class AramaBuild(build):
    def run(self):
        build.run(self)

##
# clean command
class AramaClean(clean):
    def run(self):
        clean.run(self)

##
# uninstall command
class AramaUninstall(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        arama_dir = os.path.join(get_python_lib(), "arama")
        if os.path.exists(arama_dir):
            print "removing: ", arama_dir
            shutil.rmtree(arama_dir)

        data_dir = "/var/www/paketler.pardus.org.tr/arama"
        if os.path.exists(data_dir):
            print "removing: ", data_dir
            shutil.rmtree(data_dir)


i18n_domain = "arama"
i18n_languages = ["tr"]
""",
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
	    print "po/%s.mo" % lang, os.path.join(destpath, "%s.mo" % i18n_domain)
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "%s.mo" % i18n_domain))

setup(name="arama",
      version= getVersion(),
      description="Search engine for pisi package contents",
      long_description="Search engine for pisi package contents. Lists files inside a package, searches for packages or files...",
      license="GNU GPL2",
      author="Ahmet Emre Aladag",
      author_email="emre@emrealadag.com",
      url="http://www.emrealadag.com",
      packages = ['arama'],
      package_dir = {'': ''},
      data_files = [('/var/www/paketler.pardus.org.tr/arama', data_files()),],
      ext_modules = [],
      cmdclass = {
        'build' : AramaBuild,
        'clean' : AramaClean,
        'install': I18nInstall,
        'uninstall': AramaUninstall
        }
    )

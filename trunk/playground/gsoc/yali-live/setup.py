#!/usr/bin/env python
#
# Copyright (C) 2005-2008 TUBITAK/UEKAE
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

import yali4

YALI_VERSION = yali4.__version__

def qt_ui_files():
    p = "yali4/gui/Ui/*.ui"
    return glob.glob(p)

def gui_slidepics():
    p = "yali4/gui/pics/slideshow/*.png"
    return glob.glob(p)

def user_faces():
    p = "yali4/user_faces/*.png"
    return glob.glob(p)

def data_files():
    p = "yali4/data/*"
    return glob.glob(p)

def getRevision():
    import os
    try:
        p = os.popen("svn info 2> /dev/null")
        for line in p.readlines():
            line = line.strip()
            if line.startswith("Revision:"):
                return line.split(":")[1].strip()
    except:
        return ""

def getVersion():
    # don't use svn revision...
    return YALI_VERSION

def py_file_name(ui_file):
    return os.path.splitext(ui_file)[0] + '.py'

##
# build command
class YaliBuild(build):

    def add_gettext_support(self, ui_file):
        # hacky, too hacky. but it works...
        py_file = py_file_name(ui_file)
        # lines in reverse order
        lines =  ["\n_ = __trans.ugettext\n",
                  "\n__trans = gettext.translation('yali4', fallback=True)",
                  "\nimport gettext"]
        f = open(py_file, "r").readlines()
        for l in lines:
            f.insert(1, l)
        x = open(py_file, "w")
        keyStart = "QtGui.QApplication.translate"
        keyEnd = ", None, QtGui.QApplication.UnicodeUTF8)"
        keyItem = "setItemText"
        styleKey = "setStyleSheet"
        for l in f:
            if not l.find(keyStart)==-1 and l.find(styleKey)==-1:
                if not l.find(keyItem)==-1:
                    z = "%s,_(" % l.split(",")[0]
                    y = "%s,%s,"%(l.split(",")[0],l.split(",")[1])
                else:
                    z = "%s(_(" % l.split("(")[0]
                    y = l.split(",")[0]+', '
                l = l.replace(y,z)
            l = l.replace(keyEnd,")")
            l = l.replace("data_rc","yali4.data_rc")
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

    def compile_shortcut(self):
        shortcut = "gcc desktop/yali-live.c -o desktop/yali-live"
        os.system(shortcut)
        os.system("chmod a+s desktop/yali-live") 

    def run(self):
        for f in qt_ui_files():
            self.compile_ui(f)
            self.add_gettext_support(f)
        os.system("pyrcc4 yali4/data.qrc -o yali4/data_rc.py")
        self.compile_shortcut()
        build.run(self)

##
# clean command
class YaliClean(clean):

    def run(self):
        clean.run(self)

        # clean ui generated .py files
        for f in qt_ui_files():
            f = py_file_name(f)
            if os.path.exists(f):
                os.unlink(f)

        if os.path.exists("yali4/data_rc.py"):
            os.unlink("yali4/data_rc.py")
        if os.path.exists("build"):
            shutil.rmtree("build")

##
# uninstall command
class YaliUninstall(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        yali_dir = os.path.join(get_python_lib(), "yali4")
        if os.path.exists(yali_dir):
            print "removing: ", yali_dir
            shutil.rmtree(yali_dir)

        data_dir = "/usr/share/yali4"
        if os.path.exists(data_dir):
            print "removing: ", data_dir
            shutil.rmtree(data_dir)
        os.unlink("/usr/bin/yali4-bin")
        os.unlink("/usr/bin/bindYali.sh")
        os.unlink("/usr/bin/yali-live")

i18n_domain = "yali4"
i18n_languages = ["tr",
                  "nl",
                  "it",
                  "fr",
                  "de",
                  "pt_BR",
                  "es",
                  "pl",
                  "ca",
                  "sv"]

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
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "%s.mo" % i18n_domain))

setup(name="yali4",
      version= getVersion(),
      description="YALI (Yet Another Linux Installer)",
      long_description="Pardus System Installer.",
      license="GNU GPL2",
      author="Pardus Developers",
      author_email="yali@pardus.org.tr",
      url="http://www.pardus.org.tr/eng/yali/",
      packages = ['yali4', 'yali4.gui', 'yali4.gui.Ui', 'yali4.plugins'],
      package_dir = {'': ''},
      data_files = [('/usr/share/yali4/slideshow', gui_slidepics()),
                    ('/usr/share/yali4/user_faces', user_faces()),
                    ('/usr/share/yali4/data', data_files())],
      scripts = ['yali4-bin', 'start-yali4', 'bindYali.sh', 'desktop/yali-live'],
      ext_modules = [Extension('yali4._sysutils',
                               sources = ['yali4/_sysutils.c'],
                               libraries = ["ext2fs"],
                               extra_compile_args = ['-Wall']), 
                     Extension('yali4._rootcopy',
                               sources = ['yali4/_rootcopy.c'],
                               extra_compile_args = ['-Wall']),],

      cmdclass = {
        'build' : YaliBuild,
        'clean' : YaliClean,
        'install': I18nInstall,
        'uninstall': YaliUninstall
        }
    )

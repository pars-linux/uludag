#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Taha Doğan Güneş <tdgunes@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os, shutil, sys, glob
from distutils.core import setup
from distutils.command.build import build
from distutils.command.clean import clean

NAME = "texteditor"

def compile_ui(file_ui):
    os.system("pyuic4 %s -o %s/%s_ui.py" % (file_ui, NAME, file_ui.split("/")[-1][:-3]))
    

    
class cleaner(clean):
    def run(self):
        clean.run(self)
        try:
            shutil.rmtree(NAME)
            shutil.rmtree("build")
        except:pass
        try:
            for i in os.listdir(NAME):
                if file[-4:] == ".pyc":
                    os.remove(os.path.join(NAME, i))
        except:pass
         
class builder(build):
    def run(self):
        #build.run(self)
        os.mkdir(NAME)
        try:
            ui_files = glob.glob("./ui/*.ui")
            for i in ui_files:
                compile_ui(i)
        except TypeError:
            print "No .ui files to compile it to a .py file"
        ts_files = glob.glob("./data/*.ts")
        for i in ts_files:
            os.system("lrelease-qt4 %s -qm %s/%s.qm" % (i, NAME, i.split("/")[-1][:-3]))
        os.system("pyrcc4 ./data/%s.qrc -o %s/%s_rc.py" % (NAME, NAME, NAME))
        shutil.copy("./src/main.py", NAME)
        os.system("touch ./%s/__init__.py" % NAME)
        shutil.copy("./data/texteditor", NAME)
        os.chmod("./texteditor/texteditor", 0755)

datas = [('share/applications', ['data/%s.desktop' % NAME]),
         ('share/pixmaps', ['data/texteditor.png'])]

setup( name = NAME,
       version = "1.0",
       description = "Simple Text Editor",
       author = "Taha Doğan Güneş",
       author_email = "tdgunes@gmail.com",
       license = "GNU General Public License, Version 2",
       url = "http://tdgunes.org",
       packages = [NAME],
       data_files = datas,
       scripts = ["./texteditor/texteditor"],
       cmdclass = {"build" : builder, "clean":cleaner}
       )
	    
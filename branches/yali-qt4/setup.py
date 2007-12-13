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

import glob
import os

lines =  ["\n_ = __trans.ugettext\n",
          "\n__trans = gettext.translation('yali4', fallback=True)",
          "\nimport gettext"]

def qt_ui_files():
    p = "uis/*.ui"
    return glob.glob(p)

def py_file_name(ui_file):
    return ui_file.split('.')[0] + '.py'

def compile_ui(ui_file):
    pyuic_exe = "/usr/bin/pyuic4"
    py_file = py_file_name(ui_file)
    cmd = [pyuic_exe, ui_file, '-o']
    cmd.append(py_file_name(ui_file))
    print "Processing %s ..." % ui_file
    os.system(' '.join(cmd))
    print "Converting QTranslates to gettext on %s ..." % py_file
    f = open(py_file, "r").readlines()
    for l in lines:
        f.insert(1, l)
    x = open(py_file, "w")
    keyStart = "QtGui.QApplication.translate"
    keyEnd = ", None, QtGui.QApplication.UnicodeUTF8)"
    for l in f:
        if not l.find(keyStart)==-1:
            z = "%s(_(" % l.split("(")[0]
            y = l.split(",")[0]+', '
            l = l.replace(y,z)
        l = l.replace(keyEnd,")")
        x.write(l)

for f in qt_ui_files():
    compile_ui(f)
    os.system("pyrcc4 uis/data.qrc -o data_rc.py")


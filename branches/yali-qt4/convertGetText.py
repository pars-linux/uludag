#!/usr/bin/env python
import sys
py_file = sys.argv[1]
lines =  ["\n_ = __trans.ugettext\n",
          "\n__trans = gettext.translation('yali4', fallback=True)",
          "\nimport gettext"]
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


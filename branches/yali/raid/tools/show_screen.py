#!/usr/bin/python

import sys
sys.path.append("./yali4/gui")
sys.path.append("../yali4/gui")
from PyQt4 import QtGui
from PyQt4.QtCore import *

app = QtGui.QApplication(sys.argv)
win = QtGui.QMainWindow()

module_name = sys.argv[1]
m = __import__("%s" % module_name)
w = m.Widget(win)

win.setCentralWidget(w)
win.resize(800,600)
win.show()

app.connect(app, SIGNAL("lastWindowClosed()"),
            app, SLOT("quit()"))

app.exec_()

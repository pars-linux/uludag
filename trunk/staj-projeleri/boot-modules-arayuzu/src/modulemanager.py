#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from gui.ui_mainwindow import Ui_moduleManagerDlg


class ModuleManagerDlg(QtGui.QDialog, Ui_moduleManagerDlg):

    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent) 
        self.setupUi(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ModuleManagerDlg()
    form.show()
    app.exec_()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
import gui

from gui.kaptanMain import Ui_kaptanUI

class Kaptan(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_kaptanUI()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        QtCore.QObject.connect(self.ui.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)

    def slotNext(self):
        pass

    def slotBack(self):
        pass

    def disableNext(self):
        self.buttonNext.setEnabled(False)

    def disableBack(self):
        self.buttonBack.setEnabled(False)

    def enableNext(self):
        self.buttonNext.setEnabled(True)

    def enableBack(self):
        self.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.buttonBack.isEnabled()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    kaptan = Kaptan()
    kaptan.show()
    sys.exit(app.exec_())


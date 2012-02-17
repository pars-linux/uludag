#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QCursor

from ui_hm_window import Ui_MainWindow

class HM(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.detailWidget.hide()

    @QtCore.pyqtSignature("bool")
    def on_calendarWidget_selectionChanged():
        pos = self.mapFromGlobal(QCursor.pos())
        self.detailWidget.show()
        self.detailWidget.move(pos.x(), pos.y())

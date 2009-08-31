#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import sys

from common import (SHARE, getDiskInfo)
from PyQt4 import (QtCore, QtGui, uic)

class Create(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Create, self).__init__(parent)
        uic.loadUi("%s/ui/qtMain.ui" % SHARE, self)
        self.text_src = self.label_src.text()
        self.text_dst = self.label_dst.text()

        self.connect(self.button_quit, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))

        self.button_prev.hide()
        self.button_ok.hide()

    @QtCore.pyqtSignature("bool")
    def on_button_next_clicked(self):
        src = self.line_src.displayText()
        dst = self.line_dst.displayText()

        if not self.__checkSource(src):
            self.label_warning.setText("<font color=\"red\">The ISO path you have specified is invalid!</font>")

            return False

        if not self.__checkDestination(dst):
            self.label_warning.setText("<font color=\"red\">The USB disk path you have specified is invalid!</font>")

            return False

        self.label_warning.setText("<i>The paths you have specified are valid..</i>")

        id = self.stackedWidget.currentIndex()

        if id == 0:
            self.button_next.hide()
            self.button_ok.show()
            self.button_prev.show()

            self.__checkInformation(src, dst)
            self.stackedWidget.setCurrentIndex(id + 1)

        return True

    @QtCore.pyqtSignature("bool")
    def on_button_prev_clicked(self):
        id = self.stackedWidget.currentIndex()

        if id > 0:
            self.stackedWidget.setCurrentIndex(id - 1)

        if id == 1:
            self.button_prev.hide()
            self.button_ok.hide()
            self.button_next.show()

    @QtCore.pyqtSignature("bool")
    def on_button_ok_clicked(self):
        id = self.stackedWidget.currentIndex()

        self.stackedWidget.setCurrentIndex(id + 1)

    def __checkSource(self, src):
        if QtCore.QString(src).isEmpty():

            return False

        else:
            src_extension = os.path.splitext(str(src))[1] == ".iso"

            return os.path.isfile(src) and src_extension

    def __checkDestination(self, dst):
        if QtCore.QString(dst).isEmpty():
            return False

        else:
            return os.path.ismount(str(dst))

    def __checkInformation(self, src, dst):
        (capacity, available, used) = getDiskInfo(str(dst))

        self.label_info_source.setText(src)
        self.label_info_capacity.setText(str(capacity))
        self.label_info_available.setText(str(available))
        self.label_info_used.setText(str(used))

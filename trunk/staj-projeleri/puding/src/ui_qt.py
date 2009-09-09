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

        self.connect(self.button_quit, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))

    @QtCore.pyqtSignature("bool")
    def on_button_browse_image_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Select ISO Image", os.environ["HOME"], "Images (*.iso *.img)")

        self.line_image.setText(filename)

    @QtCore.pyqtSignature("bool")
    def on_button_browse_disk_clicked(self):
        print("disk clicked")

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

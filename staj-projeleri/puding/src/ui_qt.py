#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import sys

from common import (SHARE, getDiskInfo, getIsoSize, verifyIsoChecksum)
from common import PartitionUtils
from constants import DESCRIPTION
from PyQt4 import (QtCore, QtGui, uic)

class Create(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(Create, self).__init__(parent)
        uic.loadUi("%s/ui/qtMain.ui" % SHARE, self)

        self.connect(self.button_quit, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
        self.connect(self.actionQuit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))

    @QtCore.pyqtSignature("bool")
    def on_button_browse_image_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Select ISO Image", os.environ["HOME"], "Images (*.iso *.img)")

        self.line_image.setText(filename)

    @QtCore.pyqtSignature("bool")
    def on_button_browse_disk_clicked(self):
        self.browse_disk = SelectDisk()
        if self.browse_disk.exec_() == QtGui.QDialog.Accepted:
            dirname = self.browse_disk.getSelectedDirectory()

            if not dirname:
                self.warningDialog("Warning", "You should select a valid directory.")

            else:
                self.line_disk.setText(QtCore.QString(dirname))

    @QtCore.pyqtSignature("bool")
    def on_actionAbout_triggered(self):
         QtGui.QMessageBox.about(self, "About Puding", DESCRIPTION)

    @QtCore.pyqtSignature("bool")
    def on_button_create_clicked(self):
        if not self.__checkDestination(self.line_disk.displayText()):
            self.warningDialog("Directory is Invalid", "Please check the USB disk path.")

        elif not self.__checkSource(self.line_image.displayText()):
            # FIX ME: ...
            pass

    def warningDialog(self, title, message):
        QtGui.QMessageBox.warning(self, title, message, QtGui.QMessageBox.Ok)

    def progressDialog(self, src):
        progress_dialog = QtGui.QProgressDialog("Checking md5 value", "Cancel", 0, 100)

    def __checkSource(self, src):
        if QtCore.QString(src).isEmpty():
            self.warningDialog("ISO Image is Invalid", "Please check the ISO image path.")

        if not os.path.isfile(src):
            self.warningDialog("ISO Image is Invalid", "Please check the ISO image path.")

        try:
            check_iso = ProgressBar("Verify Checksum",
                                    "The checksum of the source is checking now...")


            check_iso.exec_()
            # pi.exit()

        except TypeError:
            self.warningDialog("Checksum invalid", """\
The checksum of the source cannot be validated.
Please specify a correct source or be sure that
you have downloaded the source correctly.""")

    def __checkDestination(self, dst):
        if QtCore.QString(dst).isEmpty():
            return False

        return os.path.ismount(str(dst))

    def __checkInformation(self, src, dst):
        (capacity, available, used) = getDiskInfo(str(dst))

        self.label_info_source.setText(src)
        self.label_info_capacity.setText(str(capacity))
        self.label_info_available.setText(str(available))
        self.label_info_used.setText(str(used))

class SelectDisk(QtGui.QDialog):
    def __init__(self, parent = None):
        self.partutils = PartitionUtils()
        self.partutils.detectRemovableDrives()
        self.drives = self.partutils.returnDrives()

        #print(self.drives)

        super(SelectDisk, self).__init__(parent)
        uic.loadUi("%s/ui/qtSelectDisk.ui" % SHARE, self)

        for drive in self.drives:
            self.listWidget.addItem(self.drives[drive]["label"])

        # print(self.listWidget.currentItem())

    @QtCore.pyqtSignature("bool")
    def on_button_browse_clicked(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(self, "Choose Mount Disk Path")

        if not dirname == "":
            self.line_directory.setText(dirname)

    def getSelectedDirectory(self):
        if self.line_directory.displayText() == "":
            return False

        return self.line_directory.displayText()

class ProgressIncrement(QtCore.QThread):
    def __init__(self, progressbar, src):
        QtCore.QThread.__init__(self)

        self.pbar = progressbar
        self.src = src

    def set_data(self, size):
        self.emit(QtCore.SIGNAL("maxprogress(int)"), size)

    def run(self):
        import hashlib

        checksum = hashlib.md5()
        isofile = file(self.src, "rb")
        bytes = 1024**2
        total = 0

        while bytes:
            data = isofile.read(bytes)
            checksum.update(data)
            bytes = len(data)
            total += bytes
            self.emit(QtCore.SIGNAL("incrementProgressBar()"))

        src_md5 = checksum.hexdigest()
        print(src_md5)
        print(total)

    def incrementProgress(self):
        current_value = self.pbar.value()
        self.pbar.setValue(current_value + 1)

    def maxprogress(self, value):
        self.pbar.setMaximum(value)

class ProgressBar(QtGui.QDialog):
    def __init__(self, title, message, parent = None):
        super(ProgressBar, self).__init__(parent)
        uic.loadUi("%s/ui/qtProgressBar.ui" % SHARE, self)

        self.setWindowTitle(title)
        self.label.setText(message)

        pi = ProgressIncrement(self.progressBar, src)
        iso_size = getIsoSize(src)
        pi.set_data(size = iso_size)
        pi.start()

        self.connect(self.button_cancel, QtCore.SIGNAL("clicked(bool)"), QtCore.SLOT("close()"))
        self.connect(pi, QtCore.SIGNAL("maxprogress(int)"), pi.maxprogress)
        self.connect(pi, QtCore.SIGNAL("incrementProgressBar()"), pi.incrementProgress)


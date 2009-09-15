#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import sys

from common import (SHARE, getDiskInfo, verifyIsoChecksum)
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
            #(name, md5, url) = verifyIsoChecksum(src)
            check_iso = ProgressBar("Verify Checksum", "The checksum of the source is checking now...")
            progressbar = check_iso.progressBar
            pi = ProgressIncrement(progressbar, check_iso)
            pi.start()

            QtCore.QObject.connect(pi, QtCore.SIGNAL("incrementProgressBar()"), pi.incrementProgress)
            check_iso.exec_()

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
    def __init__(self, progressbar, dialog):
        QtCore.QThread.__init__(self)

        self.pbar = progressbar
        self.dialog = dialog

    def run(self):
        import time

        for i in range(0, 101):
            if i == 100:
                self.dialog.close()
            else:
                self.emit(QtCore.SIGNAL("incrementProgressBar()"))
                time.sleep(0.04)

    def incrementProgress(self):
        current_value = self.pbar.value()
        self.pbar.setValue(current_value + 1)

class ProgressBar(QtGui.QDialog):
    def __init__(self, title, message, parent = None):
        super(ProgressBar, self).__init__(parent)
        uic.loadUi("%s/ui/qtProgressBar.ui" % SHARE, self)

        self.setWindowTitle(title)
        self.label.setText(message)
        self.progressBar.setMaximum(100)

        self.connect(self.button_cancel, QtCore.SIGNAL("clicked(bool)"), QtCore.SLOT("close()"))

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import glob
import os
import shutil
import sys

from common import SHARE
from common import getDiskInfo
from common import getMounted
from common import getIsoSize
from common import getFilesSize
from common import createConfigFile
from common import createSyslinux
from common import createUSBDirs
from common import runCommand
from common import PartitionUtils

from constants import COPYRIGHT
from constants import CORE_DEVELOPER
from constants import CORE_EMAIL
from constants import DESCRIPTION
from constants import LICENSE_NAME
from constants import NAME
from constants import MOUNT_ISO
from constants import MOUNT_USB
from constants import VERSION
from constants import URL

from puding import qtMain
from puding import qtProgressBar
from puding import qtSelectDisk

from PyQt4 import QtCore
from PyQt4 import QtGui

from releases import releases

# General variables
increment_value = 1024**2

class Create(QtGui.QMainWindow, qtMain.Ui_MainWindow):
    def __init__(self, parent = None):
        super(Create, self).__init__(parent)
        self.setupUi(self)

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
         QtGui.QMessageBox.about(self, "About Puding", """\
<b>%s</b> - %s<br />
%s<br /><br />
%s<br />
%s<br />
%s, <i>%s</i><br />
<a href="%s">%s</a>""" % (NAME, VERSION, DESCRIPTION, LICENSE_NAME, \
                          COPYRIGHT, CORE_DEVELOPER, CORE_EMAIL, URL, URL))

    @QtCore.pyqtSignature("bool")
    def on_button_create_clicked(self):
        src = str(self.line_image.displayText())
        dst = str(self.line_disk.displayText())

        if not self.__checkDestination(dst):
            self.warningDialog("Directory is Invalid", "Please check the USB disk path.")

            return False

        try:
            confirm_infos = self.confirmDialog(src, dst)

            if confirm_infos == QtGui.QMessageBox.Ok:
                createUSBDirs(dst)
                self.__createImage(src, dst)

            return True

        except TypeError: # 'bool' object is not iterable
            return False

    def confirmDialog(self, src, dst):
        (name, md5, url) = self.__getSourceInfo(src)

        confirm_message = """\
Please double check your path information. If you don't type the path to the USB stick correctly, you may damage your computer. Would you like to continue?

CD Image Path: %s
USB Device: %s (%s)

Release Name: %s
Md5sum: %s
Download URL: %s""" % (src, dst, "NULL", name, md5, url)

        confirm_infos = self.questionDialog("Confirm Informations", confirm_message)

        return confirm_infos

    def warningDialog(self, title, message,):
        QtGui.QMessageBox.warning(self, title, message, QtGui.QMessageBox.Ok)

    def questionDialog(self, title, message):
        return QtGui.QMessageBox.question(self, title, message,
                                          QtGui.QMessageBox.Cancel |
                                          QtGui.QMessageBox.Ok)

    def __getSourceInfo(self, src):
        if QtCore.QString(src).isEmpty():
            self.warningDialog("ISO Image is Invalid", "Please set an ISO image path.")

            return False

        if not os.path.isfile(src):
            self.warningDialog("ISO Image is Invalid", "Please check the ISO image path.")

            return False

        iso_size = getIsoSize(src)
        iso_size_progress = iso_size / increment_value

        check_iso = ProgressBar(title = "Verify Checksum",
                                message = "The checksum of the source is checking now...",
                                max_value = iso_size_progress)
        pi = ProgressIncrementChecksum(check_iso, src)

        # FIX ME: Why is it in here?
        def closeDialog():
            pi.quit()
            check_iso.close()

        QtCore.QObject.connect(pi, QtCore.SIGNAL("incrementProgress()"), check_iso.incrementProgress)
        QtCore.QObject.connect(pi, QtCore.SIGNAL("closeProgressDialog()"), closeDialog)

        pi.start()
        check_iso.exec_()

        if not pi.checksum():
            self.warningDialog("Checksum invalid", """\
The checksum of the source cannot be validated.
Please specify a correct source or be sure that
you have downloaded the source correctly.""")

            return False

        return pi.checksum()

    def __checkDestination(self, dst):
        if QtCore.QString(dst).isEmpty():
            return False

        return os.path.ismount(str(dst))

    def __createImage(self, src, dst):
        # Mount iso
        cmd = "fuseiso %s %s" % (src, MOUNT_ISO)
        if runCommand(cmd):
            # FIX ME: Should use warning dialog.
            return False

        create_image = ProgressBar(title = "Creating Image",
                                message = "Creating image..",
                                max_value = getFilesSize(MOUNT_ISO))
        pi = ProgressIncrementCopy(create_image, MOUNT_ISO, dst)

        def closeDialog():
            pi.quit()
            create_image.close()

        QtCore.QObject.connect(pi, QtCore.SIGNAL("incrementProgress()"), pi.incrementProgress)
        QtCore.QObject.connect(pi, QtCore.SIGNAL("updateLabel"), pi.updateLabel)
        QtCore.QObject.connect(pi, QtCore.SIGNAL("closeProgressDialog()"), closeDialog)

        pi.start()
        create_image.exec_()

        return True

class SelectDisk(QtGui.QDialog, qtSelectDisk.Ui_Dialog):
    def __init__(self, parent = None):
        self.partutils = PartitionUtils()
        self.partutils.detectRemovableDrives()
        self.drives = self.partutils.returnDrives()

        #print(self.drives)

        super(SelectDisk, self).__init__(parent)
        self.setupUi(self)

        for drive in self.drives:
            self.listWidget.addItem(self.drives[drive]["label"])

    @QtCore.pyqtSignature("bool")
    def on_button_browse_clicked(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(self, "Choose Mount Disk Path")

        if not dirname == "":
            self.line_directory.setText(dirname)

    def on_listWidget_itemClicked(self):
        item = self.listWidget.currentItem()
        label = item.text()

        for drive in self.drives:
            if self.drives[drive]["label"] == label:
                mount_directory = self.drives[drive]["mount"]
                break

        if not mount_directory:
            mount_directory = MOUNT_USB

        self.line_directory.setText(mount_directory)

    def getSelectedDirectory(self):
        if self.line_directory.displayText() == "":
            return False

        return self.line_directory.displayText()

class ProgressBar(QtGui.QDialog, qtProgressBar.Ui_Dialog):
    def __init__(self, title, message, max_value, parent = None):
        super(ProgressBar, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle(title)
        self.label.setText(message)

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(max_value)

    def incrementProgress(self):
        current_value = self.progressBar.value()
        self.progressBar.setValue(current_value + 1)

class ProgressIncrementChecksum(QtCore.QThread):
    def __init__(self, dialog, source):
        QtCore.QThread.__init__(self)

        self.progressBar = dialog.progressBar
        self.dialog = dialog
        self.src = source

        self.progressBar.setValue(0)

    def run(self):
        import hashlib

        bytes = increment_value
        checksum = hashlib.md5()
        isofile = file(self.src, "rb")

        while bytes:
            data = isofile.read(bytes)
            checksum.update(data)
            bytes = len(data)
            self.emit(QtCore.SIGNAL("incrementProgress()"))

        self.src_md5 = checksum.hexdigest()

        self.emit(QtCore.SIGNAL("closeProgressDialog()"))

    def checksum(self):
        for release in releases:
            if self.src_md5 in release['md5']:
                return release['name'], release['md5'], release['url']

        return False

class ProgressIncrementCopy(QtCore.QThread):
    def __init__(self, dialog, source, destination):
        QtCore.QThread.__init__(self)

        self.progressBar = dialog.progressBar
        self.label = dialog.label
        self.src = source
        self.dst = destination
        self.completed = 0
        self.progressBar.setValue(0)

    def run(self):
        # Create config file
        self.message = "Creating config files for boot loader..."
        self.emit(QtCore.SIGNAL("updateLabel"), self.message)
        createConfigFile(self.dst)

        # Create ldlinux.sys file
        createSyslinux(self.dst)

        # FIX ME: Should use PartitionUtils
        device = os.path.split(getMounted(self.dst))[1][:3]
        cmd = "cat /usr/lib/syslinux/mbr.bin > /dev/%s" % device
        if runCommand(cmd):
            # FIX ME: Should use warning dialog.
            return False

        # Pardus image
        pardus_image = "%s/pardus.img" % self.src
        self.size = os.stat(pardus_image).st_size
        self.message = "Copying pardus.img file..."
        self.emit(QtCore.SIGNAL("updateLabel"), self.message)
        shutil.copy(pardus_image, "%s/pardus.img" % self.dst)
        self.emit(QtCore.SIGNAL("incrementProgress()"))

        # Boot directory
        for file in glob.glob("%s/boot/*" % self.src):
            if not os.path.isdir(file):
                file_name = os.path.split(file)[1]
                self.size = os.stat(file).st_size
                self.message = "Copying %s..." % file_name
                self.emit(QtCore.SIGNAL("updateLabel"), self.message)
                shutil.copy(file, "%s/boot/%s" % (self.dst, file_name))
                self.emit(QtCore.SIGNAL("incrementProgress()"))

        # Pisi packages
        for file in glob.glob("%s/repo/*" % self.src):
            pisi = os.path.split(file)[1]
            if not os.path.exists("%s/repo/%s" % (self.dst, pisi)):
                self.size = os.stat(file).st_size
                self.message = "Copying %s..." % pisi
                self.emit(QtCore.SIGNAL("updateLabel"), self.message)
                shutil.copy(file, "%s/repo/%s" % (self.dst, pisi))
                self.emit(QtCore.SIGNAL("incrementProgress()"))

        # Unmount iso
        cmd = "fusermount -u %s" % MOUNT_ISO
        if runCommand(cmd):
            # FIX ME: Should use warning dialog.
            return False
        print("and unmount iso is OK")

    def incrementProgress(self):
        current_value = self.progressBar.value()
        self.progressBar.setValue(current_value + self.size)

    def updateLabel(self):
        self.label.setText(self.message)

# And last..
def main():
    app = QtGui.QApplication(sys.argv)
    form = Create()
    form.show()
    sys.exit(app.exec_())

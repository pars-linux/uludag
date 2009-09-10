#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from PyKDE4.kdecore import i18n

from subprocess import Popen, PIPE, STDOUT, call
from time import time

from quickformat.ui_quickformat import Ui_MainWindow
from quickformat.diskTools import DiskTools

import sys, os

fileSystems = {"Ext4":"ext4",
               "Ext3":"ext3",
               "Ext2":"ext2",
               "FAT 16 / 32":"vfat",
               "NTFS":"ntfs"}

class QuickFormat():
    def __init__(self):
        self.addFileSystems()
        self.addDisks()

    def addFileSystems(self):
        # Temporary sapce for file system list
        self.tempFileSystems = []

        # Get file system list
        for fs in fileSystems:
            self.tempFileSystems.append(fs)

        # Sort file system list
        self.tempFileSystems.sort()
        self.sortedFileSystems = self.tempFileSystems

        # Display file system list in combobox
        for fs in self.sortedFileSystems:
            ui.cmb_fileSystem.addItem(fs)

    def addDisks(self):
        # Execute
        proc = Popen("blkid -s LABEL", shell = True, stdout = PIPE,)
        output = proc.communicate()[0]

        diskPathsAndLabels = output.splitlines()

        for diskPathAndLabel in diskPathsAndLabels:
            diskPath = diskPathAndLabel.split(':')[0]
            diskLabel = diskPathAndLabel.split(':')[1]
            diskLabel = diskLabel.__getslice__(8, diskLabel.__len__()-2)

            diskPathAndLabel = diskLabel + " (" + diskPath + ")"
            print diskPathAndLabel

            ui.cmb_deviceName.addItem(diskPathAndLabel)

            print diskLabel, diskPath
        #print output
        #print "->>", diskPathsAndLabels


    def formatStarted(self):
        ui.btn_format.setDisabled(True)
        ui.progressBar.setMaximum(0)
        ui.lbl_progress.setText(i18n("Please wait while formatting..."))

    def formatSuccessful(self):
        ui.progressBar.setMaximum(1)
        ui.progressBar.setValue(1)
        ui.lbl_progress.setText("Format completed successfully")
        ui.btn_format.setDisabled(False)
        ui.btn_cancel.setText("Close")

    def formatFailed(self):
        ui.progressBar.setMaximum(1)
        ui.progressBar.setValue(0)
        ui.lbl_progress.setText("Device is in use. Please try again")
        ui.btn_format.setDisabled(False)
        ui.btn_cancel.setText("Close")


class Formatter(QtCore.QThread):
    def __init__(self, fileSystems):
        QtCore.QThread.__init__(self)
        self.fileSystems = fileSystems

    def run(self):
        self.emit(SIGNAL("formatStarted()"))

        self.formatted = self.formatDisk()

        try:
            diskTools.refreshPartitionTable(deviceName[:8])
        except:
            print "ERROR: ======= Cannot refresh partition ======="

        if self.formatted==False:
            self.emit(SIGNAL("formatFailed()"))
        else:
            self.emit(SIGNAL("formatSuccessful()"))


    def isDeviceMounted(self):
        for mountPoint in diskTools.mountList():
            if deviceName == mountPoint[0]:
                return True

    def formatDisk(self):
        deviceName = str(ui.cmb_deviceName.itemText(ui.cmb_deviceName.currentIndex()))
        deviceName = deviceName.__getslice__(deviceName.__len__() - 10, deviceName.__len__() - 1)

        self.fs = self.fileSystems[str(
            ui.cmb_fileSystem.itemText(
                ui.cmb_fileSystem.currentIndex()))]

        # If device is mounted then unmount
        if self.isDeviceMounted() == True:
            try:
                diskTools.umount(deviceName)
            except:
                return False

        # If NTFS is selected then activate quick format
        if self.fs == "ntfs":
            self.quickOption = " -Q "
        else:
            self.quickOption = ""

        self.volumeLabel = str(ui.txt_volumeLabel.text())

        # If volume label empty
        if self.volumeLabel == "":
            self.volumeLabel = "My Disk"

        # If VFAT then labeling parameter changes
        if self.fs == "vfat":
            self.labelingCommand = "-n"
        else:
            self.labelingCommand = "-L"


        # Command to execute
        command = "mkfs -t " + self.fs + self.quickOption + " " + self.labelingCommand + " '" + self.volumeLabel + "' " + deviceName
        print command

        # Execute
        proc = Popen(command, shell = True, stdout = PIPE,)

        # If theres an error then emmit error signal
        output = proc.communicate()[0]

        ### TODO:
        ### if output contains these words emmit signal
        ### errorWords = ["error", "Error", "cannot", "Cannot"] ...

###if __name__ == "__main__":
app = QtGui.QApplication(sys.argv)
_MainWindow = QtGui.QMainWindow()

deviceName = "/dev/sdb1"

ui = Ui_MainWindow()
ui.setupUi(_MainWindow)

ui.progressBar.setMaximum(1)
ui.progressBar.setValue(0)
ui.lbl_progress.setText("")



quickFormat = QuickFormat()
diskTools = DiskTools()
formatter = Formatter(fileSystems)

QtCore.QObject.connect(ui.btn_format, QtCore.SIGNAL("clicked()"), formatter.start)
QtCore.QObject.connect(ui.btn_cancel, QtCore.SIGNAL("clicked()"), _MainWindow.close)
QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatStarted()"), quickFormat.formatStarted)
QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatSuccessful()"), quickFormat.formatSuccessful)
QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatFailed()"), quickFormat.formatFailed)

_MainWindow.show()

app.exec_()
#sys.exit(app.exec_())




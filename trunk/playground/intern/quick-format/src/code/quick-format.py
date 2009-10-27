#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from PyKDE4.kdecore import i18n
from PyKDE4.solid import Solid

from subprocess import Popen, PIPE, STDOUT, call
from time import time

from quickformat.ui_quickformat import Ui_MainWindow
from quickformat.diskTools import DiskTools

import sys, os

# volumeList = {listIndex:'VolumePath', ..}

volumeList = {'':''}

fileSystems = { "Ext4":"ext4",
                "Ext3":"ext3",
                "Ext2":"ext2",
                "FAT 16/32":"vfat",
                "NTFS":"ntfs"}

class QuickFormat():
    def __init__(self):
        self.generateVolumeList()
        self.generateFileSystemList()

    def generateFileSystemList(self):
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


    def generateVolumeList(self):
        selectedIndex = 0
        currentIndex = 0

        volumeList.clear()

        volumes = Solid.Device.listFromType(Solid.StorageDrive.StorageVolume)

        for volume in volumes:
            volumeName = volume.product()
            volumePath = volume.asDeviceInterface(Solid.Block.Block).device()
            volumeFsType = volume.asDeviceInterface(Solid.StorageVolume.StorageVolume).fsType()

            if volumeFsType!="" and not str(volumeFsType).startswith("iso")and not str(volumeFsType).startswith("swap"):
                comboboxItem = volumeName + " (" + volumePath + ") " + volumeFsType
                ui.cmb_deviceName.addItem(comboboxItem)

                if volumePath == volumePathArg:
                    selectedIndex = currentIndex

                # append volumeList
                volumeList[currentIndex] = volumePath

                currentIndex += 1

        # select the appropriate volume from list
        ui.cmb_deviceName.setCurrentIndex(selectedIndex)


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
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        self.volumeToFormat = str(volumeList[ui.cmb_deviceName.currentIndex()])

        self.fs = fileSystems[str(ui.cmb_fileSystem.currentText())]

        self.emit(SIGNAL("formatStarted()"))

        self.formatted = self.formatDisk()

        try:
            diskTools.refreshPartitionTable(self.volumeToFormat[:8])
        except:
            print "ERROR: Cannot refresh partition"

        if self.formatted==False:
            self.emit(SIGNAL("formatFailed()"))
        else:
            self.emit(SIGNAL("formatSuccessful()"))


    def isDeviceMounted(self, volumePath):
        for mountPoint in diskTools.mountList():
            if self.volumeToFormat == mountPoint[0]:
                return True

    def formatDisk(self):
        # If device is mounted then unmount
        if self.isDeviceMounted(self.volumeToFormat) == True:
            try:
                diskTools.umount(str(self.volumeToFormat))
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
        command = "mkfs -t " + self.fs + self.quickOption + " " + self.labelingCommand + " '" + self.volumeLabel + "' " + self.volumeToFormat
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
MainWindow = QtGui.QMainWindow()

volumePathArg = ""

if len(sys.argv) == 2:
    volumePathArg = sys.argv[1]

print "-" + volumePathArg + "-"

ui = Ui_MainWindow()
ui.setupUi(MainWindow)

ui.progressBar.setMaximum(1)
ui.progressBar.setValue(0)
ui.lbl_progress.setText("")

quickFormat = QuickFormat()
diskTools = DiskTools()
formatter = Formatter()

QtCore.QObject.connect(ui.btn_format, QtCore.SIGNAL("clicked()"), formatter.start)
QtCore.QObject.connect(ui.btn_cancel, QtCore.SIGNAL("clicked()"), MainWindow.close)
QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatStarted()"), quickFormat.formatStarted)
QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatSuccessful()"), quickFormat.formatSuccessful)
QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatFailed()"), quickFormat.formatFailed)

MainWindow.show()

app.exec_()




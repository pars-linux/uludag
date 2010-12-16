#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

from PyKDE4.kdecore import i18n
from PyKDE4.solid import Solid

from subprocess import Popen, PIPE, STDOUT, call
from time import time

from quickformat.ui_quickformat import Ui_QuickFormat
from quickformat.diskTools import DiskTools

from quickformat.ui_item import Ui_Form

import sys, os

# volumeList = {listIndex:'VolumePath', ..}

volumeList = {'':''}

fileSystems = { "Ext4":"ext4",
                "Ext3":"ext3",
                "Ext2":"ext2",
                "FAT 16/32":"vfat",
                "NTFS":"ntfs"}

class QuickFormatItem(Ui_Form, QtGui.QWidget):
    def __init__(self, name, path, label, format, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.name.setText(name)
        self.label.setText(label)
        self.path.setText(path)
        self.format.setText(format)

class QuickFormat(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.volumePathArg = ""

        if len(sys.argv) == 2:
            self.volumePathArg = sys.argv[1]

        self.ui = Ui_QuickFormat()
        self.ui.setupUi(self)

        self.initSignals()

        self.ui.deviceName.setModel(self.ui.listWidget.model())
        self.ui.deviceName.setView(self.ui.listWidget)

        self.generateVolumeList()
        self.generateFileSystemList()

    def setInfo(self):
        self.ui.volumeLabel.setText(self.ui.deviceName.currentText())
        #self.ui.icon.setIcon(self.ui.deviceName)


    def initSignals(self):
        QtCore.QObject.connect(self.ui.deviceName, QtCore.SIGNAL("currentIndexChanged(QString)"), self.setInfo)
        """
        QtCore.QObject.connect(self.ui.btn_format, QtCore.SIGNAL("clicked()"), formatter.start)
        QtCore.QObject.connect(self.ui.btn_cancel, QtCore.SIGNAL("clicked()"), self.exit)
        QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatStarted()"), self.formatStarted)
        QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatSuccessful()"), self.formatSuccessful)
        QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatFailed()"), self.formatFailed)
        """

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
            self.ui.fileSystem.addItem(fs)


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

                widget = QuickFormatItem(volume.parent().product(), volumePath, volumeName, volumeFsType, self.ui.listWidget)
                item = QtGui.QListWidgetItem(volumePath , self.ui.listWidget)
                self.ui.listWidget.setItemWidget(item, widget)

                #icon = "/images/images/" + str(volume.icon()) + ".png"
                #self.ui.icon.setPixmap(QtGui.QPixmap(icon))

                #print icon
                item.setSizeHint(QSize(200,70))

                if volumePath == self.volumePathArg:
                    selectedIndex = currentIndex

                # append volumeList
                volumeList[currentIndex] = volumePath

                currentIndex += 1

        # select the appropriate volume from list
        self.ui.deviceName.setCurrentIndex(selectedIndex)


    def formatStarted(self):
        self.ui.btn_format.setDisabled(True)
        """
        self.ui.progressBar.setMaximum(0)
        self.ui.lbl_progress.setText(i18n("Please wait while formatting..."))
        """

    def formatSuccessful(self):
        """
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(1)
        self.ui.lbl_progress.setText("Format completed successfully")
        """
        self.ui.btn_format.setDisabled(False)
        self.ui.btn_cancel.setText("Close")

    def formatFailed(self):
        """
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(0)
        self.ui.lbl_progress.setText("Device is in use. Please try again")
        """
        self.ui.btn_format.setDisabled(False)
        self.ui.btn_cancel.setText("Close")


class Formatter(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        self.volumeToFormat = str(volumeList[self.ui.deviceName.currentIndex()])

        self.fs = fileSystems[str(self.ui.fileSystem.currentText())]

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

        self.volumeLabel = str(self.ui.txt_volumeLabel.text())

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
quick_format = QuickFormat()
quick_format.show()


#self.ui.progressBar.setMaximum(1)
#self.ui.progressBar.setValue(0)
#self.ui.lbl_progress.setText("")

#quickFormat = QuickFormat()
#diskTools = DiskTools()
#formatter = Formatter()
#MainWindow.show()

app.exec_()




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

from quickformat.ui_volumeitem import Ui_VolumeItem

import sys, os

# volumeList = {listIndex:'VolumePath', ..}

volumeList = {'':''}

fileSystems = { "ext4":"ext4",
                "ext3":"ext3",
                "ext2":"ext2",
                "FAT32":"vfat",
                "NTFS":"ntfs"}

class VolumeItem(Ui_VolumeItem, QtGui.QWidget):
    def __init__(self, name, path, label, format, icon, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.name.setText(name)
        self.label.setText(label)
        self.path.setText(path)
        self.format.setText("(" + format + ")")
        self.icon.setPixmap(icon)

class QuickFormat(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_QuickFormat()
        self.ui.setupUi(self)

        self.__initSignals__()
        self.__setCustomWidgets__()
        self.__processArgs__()

        self.generateVolumeList()
        self.generateFileSystemList()

    def __setCustomWidgets__(self):
        self.ui.volumeName.setModel(self.ui.listWidget.model())
        self.ui.volumeName.setView(self.ui.listWidget)

    def __processArgs__(self):
        self.volumePathArg = ""

        if len(sys.argv) == 2:
            self.volumePathArg = sys.argv[1]

    def __initSignals__(self):
        self.connect(self.ui.volumeName, QtCore.SIGNAL("currentIndexChanged(QString)"), self.setInfo)
        """
        QtCore.QObject.connect(self.ui.btn_format, QtCore.SIGNAL("clicked()"), formatter.start)
        QtCore.QObject.connect(self.ui.btn_cancel, QtCore.SIGNAL("clicked()"), self.exit)
        QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatStarted()"), self.formatStarted)
        QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatSuccessful()"), self.formatSuccessful)
        QtCore.QObject.connect(formatter, QtCore.SIGNAL("formatFailed()"), self.formatFailed)
        """

    def setInfo(self, num):
        self.ui.volumeLabel.setText(self.ui.volumeName.currentText())
        #self.ui.icon.setIcon(self.ui.volumeName)

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

    def filterFileSystem(self, fileSystem):
        if fileSystem!="" \
                and not str(fileSystem).startswith("iso") \
                and not str(fileSystem).startswith("swap"):
            return True

    def getVolumes(self):
        volumes = []

        # Get volumes
        for volume in Solid.Device.listFromType(Solid.StorageDrive.StorageVolume):
            # Apply filter
            if self.filterFileSystem(self.getVolumeFileSystem(volume)):
                volumes.append(volume)
        return volumes

    def getVolumeIcon(self, icon):
        iconPath = ":/images/images/" + str(icon) + ".png"
        return QtGui.QPixmap(iconPath)

    def getVolumeName(self, volume):
        return volume.product()

    def getVolumePath(self, volume):
        return volume.asDeviceInterface(Solid.Block.Block).device()

    def getVolumeFileSystem(self, volume):
        return volume.asDeviceInterface(Solid.StorageVolume.StorageVolume).fsType()

    def getDiskName(self, volume):
        """ returns the disk name that the volume resides on """
        return volume.parent().product()

    def addVolumeToList(self, volume):
        diskName = self.getDiskName(volume)
        volumeName = self.getVolumeName(volume)
        volumePath = self.getVolumePath(volume)
        volumeFileSystem = self.getVolumeFileSystem(volume)
        volumeIcon = self.getVolumeIcon(volume.icon())

        # Create custom widget
        widget = VolumeItem(diskName, volumePath, volumeName, volumeFileSystem, volumeIcon, self.ui.listWidget)

        # Create list widget item
        item = QtGui.QListWidgetItem(volumePath , self.ui.listWidget)

        # Set the list widget item's interior to our custom widget and append to list
        # list widget item <-> custom widget
        self.ui.listWidget.setItemWidget(item, widget)

        item.setSizeHint(QSize(200,70))


    def generateVolumeList(self):
        selectedIndex = 0
        currentIndex = 0

        volumeList.clear()

        volumes = self.getVolumes()

        for volume in volumes:
            self.addVolumeToList(volume)

            """
            if volumePath == self.volumePathArg:
                selectedIndex = currentIndex

            # append volumeList
            volumeList[currentIndex] = volumePath
            currentIndex += 1
            """


        # select the appropriate volume from list
        self.ui.volumeName.setCurrentIndex(selectedIndex)


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
        self.volumeToFormat = str(volumeList[self.ui.volumeName.currentIndex()])

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




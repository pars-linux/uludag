#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSize, SIGNAL, QThread

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

        self.generate_volume_list()
        self.generate_file_system_list()

    def __setCustomWidgets__(self):
        self.ui.volumeName.setModel(self.ui.listWidget.model())
        self.ui.volumeName.setView(self.ui.listWidget)

    def __processArgs__(self):
        self.volumePathArg = ""

        if len(sys.argv) == 2:
            self.volumePathArg = sys.argv[1]

    def __initSignals__(self):
        self.connect(self.ui.volumeName, SIGNAL("currentIndexChanged(QString)"), self.set_info)
        """
        QObject.connect(self.ui.btn_format, SIGNAL("clicked()"), formatter.start)
        QObject.connect(self.ui.btn_cancel, SIGNAL("clicked()"), self.exit)
        QObject.connect(formatter, SIGNAL("format_started()"), self.format_started)
        QObject.connect(formatter, SIGNAL("format_successful()"), self.format_successful)
        QObject.connect(formatter, SIGNAL("format_failed()"), self.format_failed)
        """

    def set_info(self, num):
        self.ui.volumeLabel.setText(self.ui.volumeName.currentText())
        #self.ui.icon.setIcon(self.ui.volumeName)

    def generate_file_system_list(self):
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

    def filter_file_system(self, fileSystem):
        if fileSystem!="" \
                and not str(fileSystem).startswith("iso") \
                and not str(fileSystem).startswith("swap"):
            return True

    def get_volumes(self):
        volumes = []

        # Get volumes
        for volume in Solid.Device.listFromType(Solid.StorageDrive.StorageVolume):
            # Apply filter
            if self.filter_file_system(self.get_volume_file_system(volume)):
                volumes.append(volume)
        return volumes

    def get_volume_icon(self, icon):
        iconPath = ":/images/images/" + str(icon) + ".png"
        return QtGui.QPixmap(iconPath)

    def get_volume_name(self, volume):
        return volume.product()

    def get_volume_path(self, volume):
        return volume.asDeviceInterface(Solid.Block.Block).device()

    def get_volume_file_system(self, volume):
        return volume.asDeviceInterface(Solid.StorageVolume.StorageVolume).fsType()

    def get_disk_name(self, volume):
        """ returns the disk name that the volume resides on """
        return volume.parent().product()

    def add_volume_to_list(self, volume):
        diskName = self.get_disk_name(volume)
        volumeName = self.get_volume_name(volume)
        volumePath = self.get_volume_path(volume)
        volumeFileSystem = self.get_volume_file_system(volume)
        volumeIcon = self.get_volume_icon(volume.icon())

        # Create custom widget
        widget = VolumeItem(diskName, volumePath, volumeName, volumeFileSystem, volumeIcon, self.ui.listWidget)

        # Create list widget item
        item = QtGui.QListWidgetItem(volumePath , self.ui.listWidget)

        # Set the list widget item's interior to our custom widget and append to list
        # list widget item <-> custom widget
        self.ui.listWidget.setItemWidget(item, widget)

        item.setSizeHint(QSize(200,70))


    def generate_volume_list(self):
        selectedIndex = 0
        currentIndex = 0

        volumeList.clear()

        volumes = self.get_volumes()

        for volume in volumes:
            self.add_volume_to_list(volume)

            """
            if volumePath == self.volumePathArg:
                selectedIndex = currentIndex

            # append volumeList
            volumeList[currentIndex] = volumePath
            currentIndex += 1
            """


        # select the appropriate volume from list
        self.ui.volumeName.setCurrentIndex(selectedIndex)


    def format_started(self):
        self.ui.btn_format.setDisabled(True)
        """
        self.ui.progressBar.setMaximum(0)
        self.ui.lbl_progress.setText(i18n("Please wait while formatting..."))
        """

    def format_successful(self):
        """
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(1)
        self.ui.lbl_progress.setText("Format completed successfully")
        """
        self.ui.btn_format.setDisabled(False)
        self.ui.btn_cancel.setText("Close")

    def format_failed(self):
        """
        self.ui.progressBar.setMaximum(1)
        self.ui.progressBar.setValue(0)
        self.ui.lbl_progress.setText("Device is in use. Please try again")
        """
        self.ui.btn_format.setDisabled(False)
        self.ui.btn_cancel.setText("Close")


class Formatter(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.volumeToFormat = str(volumeList[self.ui.volumeName.currentIndex()])

        self.fs = fileSystems[str(self.ui.fileSystem.currentText())]

        self.emit(SIGNAL("format_started()"))

        self.formatted = self.format_disk()

        try:
            diskTools.refreshPartitionTable(self.volumeToFormat[:8])
        except:
            print "ERROR: Cannot refresh partition"

        if self.formatted==False:
            self.emit(SIGNAL("format_failed()"))
        else:
            self.emit(SIGNAL("format_successful()"))


    def is_device_mounted(self, volumePath):
        for mountPoint in diskTools.mountList():
            if self.volumeToFormat == mountPoint[0]:
                return True

    def format_disk(self):
        # If device is mounted then unmount
        if self.is_device_mounted(self.volumeToFormat) == True:
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




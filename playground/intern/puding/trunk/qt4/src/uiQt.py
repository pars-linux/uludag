#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import glob
import os
import shutil
import sys
import tempfile

from common import getDiskInfo
from common import getIsoSize
from common import getFileSize
from common import getMounted
from common import createSyslinux
from common import createUSBDirs
from common import runCommand
from common import PartitionUtils

from constants import CORE_DEVELOPER
from constants import CORE_EMAIL
from constants import LICENSE_NAME
from constants import NAME
from constants import SHARE
from constants import URL
from constants import VERSION
from constants import YEAR
from constants import ART_CONTRIBUTOR
from constants import TRANSLATORS

from puding import qtAbout
from puding import qtConfirmDialog
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
        self.iso_dir = tempfile.mkdtemp(suffix="_isoPuding")

        super(Create, self).__init__(parent)
        self.setupUi(self)

        self.connect(self.button_quit, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
        self.connect(self.actionQuit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))

    @QtCore.pyqtSignature("bool")
    def on_button_browse_image_clicked(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, self.tr("Select CD Image"),
                os.environ["HOME"], "%s (*.iso *.img)" % self.tr("Images"))

        self.line_image.setText(filename)

    @QtCore.pyqtSignature("bool")
    def on_button_browse_disk_clicked(self):
        self.browse_disk = SelectDisk()
        if self.browse_disk.exec_() == QtGui.QDialog.Accepted:
            dirname = self.browse_disk.getSelectedDirectory()

            if not dirname:
                self.warningDialog(self.tr("Warning"), self.tr("You should select a valid directory."))

            else:
                self.line_disk.setText(QtCore.QString(dirname))

    @QtCore.pyqtSignature("bool")
    def on_actionAbout_triggered(self):
        about_puding = About()
        about_puding.exec_()

    @QtCore.pyqtSignature("bool")
    def on_button_create_clicked(self):
        # FIXED issue: #1
        src = unicode(str(self.line_image.displayText()))
        dst = str(self.line_disk.displayText())

        if dst.startswith("/dev/"):
            device = dst
            dst = tempfile.mkdtemp(suffix="_usbPuding")

            from puding.pardusTools import Authorization

            auth = Authorization()
            auth.mount(device, dst)

        if not self.__checkDestination(dst):
            self.warningDialog(self.tr("Directory is Invalid"), self.tr("Please check the USB disk path."))

            return False

        try:
            (name, md5, url) = self.__getSourceInfo(src)

        except TypeError: # 'bool' object is not iterable
            # It's not true way, you should warn to the users with WarningDialog.
            return False

        mount_point = getMounted(dst)
        (capacity, available, used) = getDiskInfo(dst)

        # Mount iso
        if not os.path.ismount(self.iso_dir):
            cmd = "fuseiso %s %s" % (src, self.iso_dir)
            if runCommand(cmd):
                # FIX ME: Should use warning dialog.
                return False

        # FIX ME: Now Puding supports only Pardus.
        from pardusTools import Main

        self.tools = Main(self.iso_dir, dst)
        total_size = self.tools.getTotalSize()

        if available < total_size:
            self.warningDialog("Warning", "There is not enough space left on your USB stick for the image.")

        else:
            self.confirm_infos = ConfirmDialog(src, dst, mount_point, name, total_size, capacity, available, used)

            if self.confirm_infos.exec_() == QtGui.QDialog.Accepted:
                createUSBDirs(dst)
                self.__createImage(src, dst)

                if dst.endswith("Puding"):
                    auth.umount(dst)

        runCommand("fusermount -u %s" % self.iso_dir)

    def warningDialog(self, title, message,):
        QtGui.QMessageBox.warning(self, title, message, QtGui.QMessageBox.Ok)

    def questionDialog(self, title, message):
        return QtGui.QMessageBox.question(self, title, message,
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)

    def __getSourceInfo(self, src):
        if QtCore.QString(src).isEmpty():
            self.warningDialog(self.tr("CD Image is Invalid"), self.tr("Please set an CD image path."))

            return False

        if not os.path.isfile(src):
            self.warningDialog(self.tr("CD Image is Invalid"), self.tr("Please check the CD image path."))

            return False

        iso_size = getIsoSize(src)
        iso_size_progress = iso_size / increment_value

        check_iso = ProgressBar(title = self.tr("Verify Checksum"),
                                message = self.tr("The checksum of the source is checking now..."),
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
            message = """The checksum of the source cannot be validated.
Please specify a correct source or be sure that
you have downloaded the source correctly."""

            self.warningDialog(self.tr("Checksum invalid"), self.tr(message))

            return False

        return pi.checksum()

    def __checkDestination(self, dst):
        if QtCore.QString(dst).isEmpty():
            return False

        return os.path.ismount(str(dst))

    def __createImage(self, src, dst):
        file_list = self.tools.file_list
        max_value = self.tools.getNumberOfFiles()
        create_image = ProgressBar(title = self.tr("Creating Image"), message = self.tr("Creating image..."), max_value = max_value)
        pi = ProgressIncrementCopy(create_image, self.iso_dir, dst)

        def closeDialog():
            pi.quit()
            create_image.close()

        QtCore.QObject.connect(pi, QtCore.SIGNAL("incrementProgress()"), create_image.incrementProgress)
        QtCore.QObject.connect(pi, QtCore.SIGNAL("updateLabel"), pi.updateLabel)
        QtCore.QObject.connect(pi, QtCore.SIGNAL("closeProgressDialog()"), closeDialog)

        pi.start()
        create_image.exec_()

        self.warningDialog(self.tr("USB Image is Ready"), self.tr("Your USB image is ready. Now you can install or run Pardus from USB storage."))

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
            label = QtGui.QListWidgetItem(QtCore.QString(self.drives[drive]["label"]))
            label.setIcon(QtGui.QIcon(":/icons/images/usb.png"))
            self.listWidget.addItem(label)

    @QtCore.pyqtSignature("bool")
    def on_button_browse_clicked(self):
        dirname = QtGui.QFileDialog.getExistingDirectory(self, self.tr("Choose Mount Disk Path"))

        if not dirname:
            self.line_directory.setText(dirname)

    def on_listWidget_itemClicked(self):
        item = self.listWidget.currentItem()
        label = item.text()

        for drive in self.drives:
            if self.drives[drive]["label"] == label:
                device = self.drives[drive]["mount"]
                if not device:
                    device = drive
                break

        self.line_directory.setText(device)

    def getSelectedDirectory(self):
        if self.line_directory.displayText() == "":
            return False

        return self.line_directory.displayText()

class ConfirmDialog(QtGui.QDialog, qtConfirmDialog.Ui_Dialog):
    def __init__(self, src, dst, mount_point, name, total_size, capacity, available, used, parent = None):
        super(ConfirmDialog, self).__init__(parent)
        self.setupUi(self)
        dst_info = "%s (%s)" % (dst, mount_point)

        self.label_name.setText(name)
        self.label_src.setText(src)
        self.label_src_size.setText("%dMB" % total_size)
        self.label_dst.setText(dst_info)

        self.label_capacity.setText("%dMB" % capacity)
        self.label_available.setText("%dMB" % available)
        self.label_used.setText("%dMB" % used)

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

class About(QtGui.QDialog, qtAbout.Ui_Dialog):
    def __init__(self, parent = None):
        super(About, self).__init__(parent)
        self.setupUi(self)

        description = self.tr("Puding is an USB image creator for Pardus Linux.")
        copyright = self.tr("Copyright (c) %s TUBITAK / UEKAE" % YEAR)

        about_text = "<b>puding</b> - %s<br>%s<br>%s<br><br><a href=\"%s\">%s</a><br>" % (VERSION, description, copyright, URL, URL)
        self.label_description.setText(about_text)

        authors = "%s, %s" % (CORE_DEVELOPER, CORE_EMAIL)
        translators = TRANSLATORS
        art_contributor = ART_CONTRIBUTOR
        self.plaintext_authors.setPlainText(authors)
        self.plaintext_translators.setPlainText(translators)
        self.plaintext_artwork.setPlainText(art_contributor)

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
        self.progressBar.setValue(0)
        self.label = dialog.label
        self.src = source
        self.dst = destination
        self.file_list = ["%s/pardus.img" % self.src]
        for file in glob.glob("%s/boot/*" % self.src):
            if os.path.isfile(file):
                self.file_list.append(file)
        self.file_list.extend(glob.glob("%s/repo/*" % self.src))

    def run(self):
        # Create config file
        createSyslinux(self.dst)

        for file in self.file_list:
            size = getFileSize(file)
            file_name = os.path.split(file)[1]
            self.message = self.tr("Copying %s (%0.2fMB)" % (file_name, size))
            self.emit(QtCore.SIGNAL("updateLabel"), self.message)
            shutil.copyfile(file, "%s/%s" % (self.dst, file.split(self.src)[-1]))
            self.emit(QtCore.SIGNAL("incrementProgress()"))

        self.emit(QtCore.SIGNAL("closeProgressDialog()"))

    def updateLabel(self, message):
        self.label.setText(message)

# And last..
def main():
    app = QtGui.QApplication(sys.argv)
    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    translator.load("%s/qm/puding_%s.qm" % (SHARE, locale))
    app.installTranslator(translator)
    form = Create()
    form.show()
    sys.exit(app.exec_())

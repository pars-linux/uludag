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
from PyQt4 import QtCore
from PyQt4 import QtGui

from puding.common import get_disk_info
from puding.common import get_iso_size
from puding.common import get_file_size
from puding.common import get_mounted
from puding.common import create_syslinux
from puding.common import create_USB_dirs
from puding.common import run_command
from puding.common import PartitionUtils
from puding.constants import AUTHORS
from puding.constants import LICENSE_NAME
from puding.constants import URL
from puding.constants import VERSION
from puding.constants import YEAR
from puding.constants import ART_CONTRIBUTOR
from puding.constants import TRANSLATORS
from puding.releases import releases
from puding.ui.qt import about_dialog_ui
from puding.ui.qt import confirm_dialog_ui
from puding.ui.qt import main_window_ui
from puding.ui.qt import progressbar_ui
from puding.ui.qt import select_disk_ui


# General variables
increment_value = 1024**2

class MainWindow(QtGui.QMainWindow, main_window_ui.Ui_MainWindow):
    def __init__(self, parent = None):
        self.iso_dir = tempfile.mkdtemp(suffix="_isoPuding")

        super(MainWindow, self).__init__(parent)
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
            dirname = self.browse_disk.get_selected_directory()

            if not dirname:
                self.warning_dialog(self.tr("Warning"), self.tr("You should select a valid directory."))

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

        if not self.__check_destination(dst):
            self.warning_dialog(self.tr("Directory is Invalid"), self.tr("Please check the USB disk path."))

            return False

        try:
            (name, md5, url) = self.__get_source_info(src)

        except TypeError: # 'bool' object is not iterable
            # It's not true way, you should warn to the users with WarningDialog.
            return False

        mount_point = get_mounted(dst)
        (capacity, available, used) = get_disk_info(dst)

        # Mount iso
        if not os.path.ismount(self.iso_dir):
            cmd = "fuseiso %s %s" % (src, self.iso_dir)
            if run_command(cmd):
                # FIX ME: Should use warning dialog.
                return False

        # FIX ME: Now Puding supports only Pardus.
        from pardusTools import Main

        self.tools = Main(self.iso_dir, dst)
        total_size = self.tools.get_total_size()

        if available < total_size:
            self.warning_dialog("Warning", "There is not enough space left on your USB stick for the image.")

        else:
            self.confirm_infos = ConfirmDialog(src, dst, mount_point, name, total_size, capacity, available, used)

            if self.confirm_infos.exec_() == QtGui.QDialog.Accepted:
                create_USB_dirs(dst)
                self.__create_image(src, dst)

                if dst.endswith("Puding"):
                    auth.umount(dst)

        run_command("fusermount -u %s" % self.iso_dir)

    def warning_dialog(self, title, message,):
        QtGui.QMessageBox.warning(self, title, message, QtGui.QMessageBox.Ok)

    def question_dialog(self, title, message):
        return QtGui.QMessageBox.question(self, title, message,
                QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)

    def __get_source_info(self, src):
        if QtCore.QString(src).isEmpty():
            self.warning_dialog(self.tr("CD Image is Invalid"), self.tr("Please set an CD image path."))

            return False

        if not os.path.isfile(src):
            self.warning_dialog(self.tr("CD Image is Invalid"), self.tr("Please check the CD image path."))

            return False

        iso_size = get_iso_size(src)
        iso_size_progress = iso_size / increment_value

        check_iso = ProgressBar(title = self.tr("Verify Checksum"),
                                message = self.tr("The checksum of the source is checking now..."),
                                max_value = iso_size_progress)
        pi = ProgressIncrementChecksum(check_iso, src)

        # FIX ME: Why is it in here?
        def close_dialog():
            pi.quit()
            check_iso.close()

        QtCore.QObject.connect(pi, QtCore.SIGNAL("increment_progress()"), check_iso.increment_progress)
        QtCore.QObject.connect(pi, QtCore.SIGNAL("closeProgressDialog()"), close_dialog)

        pi.start()
        check_iso.exec_()

        if not pi.checksum():
            message = """The checksum of the source cannot be validated.
Please specify a correct source or be sure that
you have downloaded the source correctly."""

            self.warning_dialog(self.tr("Checksum invalid"), self.tr(message))

            return False

        return pi.checksum()

    def __check_destination(self, dst):
        if QtCore.QString(dst).isEmpty():
            return False

        return os.path.ismount(str(dst))

    def __create_image(self, src, dst):
        file_list = self.tools.file_list
        max_value = self.tools.get_number_of_files()
        create_image = ProgressBar(title = self.tr("Creating Image"), message = self.tr("Creating image..."), max_value = max_value)
        pi = ProgressIncrementCopy(create_image, self.iso_dir, dst)

        def close_dialog():
            pi.quit()
            create_image.close()

        QtCore.QObject.connect(pi, QtCore.SIGNAL("increment_progress()"), create_image.increment_progress)
        QtCore.QObject.connect(pi, QtCore.SIGNAL("update_label"), pi.update_label)
        QtCore.QObject.connect(pi, QtCore.SIGNAL("closeProgressDialog()"), close_dialog)

        pi.start()
        create_image.exec_()

        self.warning_dialog(self.tr("USB Image is Ready"), self.tr("Your USB image is ready. Now you can install or run Pardus from USB storage."))

        return True

class SelectDisk(QtGui.QDialog, select_disk_ui.Ui_Dialog):
    def __init__(self, parent = None):
        self.partutils = PartitionUtils()
        self.partutils.detect_removable_drives()
        self.drives = self.partutils.return_drives()

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

    def get_selected_directory(self):
        if self.line_directory.displayText() == "":
            return False

        return self.line_directory.displayText()

class ConfirmDialog(QtGui.QDialog, confirm_dialog_ui.Ui_Dialog):
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

class ProgressBar(QtGui.QDialog, progressbar_ui.Ui_Dialog):
    def __init__(self, title, message, max_value, parent = None):
        super(ProgressBar, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle(title)
        self.label.setText(message)

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(max_value)

    def increment_progress(self):
        current_value = self.progressBar.value()
        self.progressBar.setValue(current_value + 1)

class About(QtGui.QDialog, about_dialog_ui.Ui_Dialog):
    def __init__(self, parent = None):
        super(About, self).__init__(parent)
        self.setupUi(self)

        description = self.tr("Puding is an USB image creator for Pardus Linux.")
        copyright = self.tr("Copyright (c) %s TUBITAK / UEKAE" % YEAR)

        about_text = "<b>puding</b> - %s<br>%s<br>%s<br><br><a href=\"%s\">%s</a><br>" % (VERSION, description, copyright, URL, URL)
        self.label_description.setText(about_text)

        translators = TRANSLATORS
        art_contributor = ART_CONTRIBUTOR
        self.plaintext_authors.setPlainText(AUTHORS)
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
            self.emit(QtCore.SIGNAL("increment_progress()"))

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
        create_syslinux(self.dst)

        for file in self.file_list:
            size = get_file_size(file)
            file_name = os.path.split(file)[1]
            self.message = self.tr("Copying %s (%0.2fMB)" % (file_name, size))
            self.emit(QtCore.SIGNAL("update_label"), self.message)
            shutil.copyfile(file, "%s/%s" % (self.dst, file.split(self.src)[-1]))
            self.emit(QtCore.SIGNAL("increment_progress()"))

        self.emit(QtCore.SIGNAL("closeProgressDialog()"))

    def update_label(self, message):
        self.label.setText(message)


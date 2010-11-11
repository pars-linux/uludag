#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Connection dialog
"""

# Standard modules
import os
import urllib2

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_repository import Ui_dialogRepository

# Helper modules
from lider.helpers import wrappers


class DialogRepository(QtGui.QDialog, Ui_dialogRepository):
    """
        Dialog for connections.

        Usage:
            dialog = DialogRepository(form)
            dialog.set_url("http://..")
            if dialog.exec_():
                print dialog.get_name()
    """

    def __init__(self, parent=None):
        """
            Constructor for dialog.

            Arguments:
                parent: Parent object
        """
        QtGui.QDialog.__init__(self, parent)

        # Attach generated UI
        self.setupUi(self)

        # Fine tune UI
        regex = QtCore.QRegExp("^[a-zA-Z0-9\-_]*$")
        validator = QtGui.QRegExpValidator(regex, self.editName)
        self.editName.setValidator(validator)

        # UI events
        self.connect(self.editURL, QtCore.SIGNAL("editingFinished()"), self.__check_fields)
        self.connect(self.editName, QtCore.SIGNAL("editingFinished()"), self.__check_fields)
        self.connect(self.pushCheck, QtCore.SIGNAL("clicked()"), self.__slot_check)

        # Update check button
        self.__update_urlcheck()

    def __slot_check(self):
        """
            Fetches URL and checks for errors.
        """
        if len(self.editURL.text()):
            repo_url = str(self.editURL.text())

            progress = wrappers.Progress(self)
            progress.started("Fetching...")

            try:
                connection = urllib2.urlopen(repo_url)
            except ValueError:
                progress.finished()
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to download %s" % repo_url)
                return

            output = os.tmpfile()
            total_size = int(connection.info()['Content-Length'])
            size = 0
            while size < total_size:
                data = connection.read(4096)
                output.write(data)
                size += len(data)
                progress.progress("%d / %d" % (size, total_size), 100 * size / total_size)
            output.seek(0)
            data = output.read()
            output.close()
            connection.close()
            progress.finished()

            if repo_url.endswith(".bz2"):
                import bz2
                data = bz2.decompress(data)

            import piksemel
            try:
                tag = piksemel.parseString(data).getTag("Distribution")
                name = "%s-%s" % (tag.getTagData("SourceName"), tag.getTagData("Version"))
            except:
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to download %s" % repo_url)
                name = ""

            if not len(self.editName.text()):
                name = name.replace(" ", "-")
                self.editName.setText(name)

    def get_url(self):
        """
            Returns URL.
        """
        return str(self.editURL.text())

    def get_name(self):
        """
            Returns name.
        """
        return str(self.editName.text())

    def set_url(self, url):
        """
            Sets URL.
        """
        self.editURL.setText(url)
        self.__update_urlcheck()

    def set_name(self, name):
        """
            Sets name.
        """
        self.editName.setText(name)

    def __update_urlcheck(self):
        """
            Enables URL check button when necessary.
        """
        try:
            import pisi
        except ImportError:
            self.pushCheck.hide()
            return
        if len(self.editURL.text()):
            self.pushCheck.setEnabled(True)
        else:
            self.pushCheck.setEnabled(False)

    def __check_fields(self, set_focus=False):
        """
            Checks fields for errors:

            Returns: True if valid, else False
        """
        self.__update_urlcheck()
        if self.editURL.isModified() and not len(self.editURL.text()):
            self.labelWarning.setText("URL is required.")
            if set_focus:
                self.editURL.setFocus(QtCore.Qt.OtherFocusReason)
            return False
        if self.editName.isModified() and not len(self.editName.text()):
            self.labelWarning.setText("Name is required.")
            if set_focus:
                self.editName.setFocus(QtCore.Qt.OtherFocusReason)
            return False
        self.labelWarning.setText("")
        return True

    def accept(self):
        if self.__check_fields(set_focus=True):
            QtGui.QDialog.accept(self)

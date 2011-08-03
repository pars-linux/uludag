#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Connection dialog
"""

# Standard modules
import socket

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.ui_connection import Ui_dialogConnection

# Helper modules
from lider.helpers import profile
from lider.helpers import profilereader
from lider.helpers import profilewriter

class DialogConnection(QtGui.QDialog, Ui_dialogConnection):
    """
        Dialog for connections.

        Usage:
            dialog = DialogConnection(form)
            dialog.set_domain("example.com")
            if dialog.exec_():
                print dialog.get_domain()
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

        # UI events
        #self.connect(self.comboDomain, QtCore.SIGNAL("editingFinished()"), self.__slot_find_host)
        #self.connect(self.comboDomain, QtCore.SIGNAL("editingFinished()"), self.__check_fields)
        self.connect(self.editHost, QtCore.SIGNAL("editingFinished()"), self.__check_fields)
        self.connect(self.editUser, QtCore.SIGNAL("editingFinished()"), self.__check_fields)
        self.connect(self.comboDomain, QtCore.SIGNAL("currentIndexChanged(int)"), self.__set_profile)

        # Create Profile Reader to list of profiles
        reader = profilereader.ProfileReader()
        self.profiles = []
        if reader.is_file_exists():
            self.profiles = reader.read()

            # Fill the profiles
            self.__fill_profiles()

            # Set last profile which is 0th place of profile list
            self.__set_profile(0)

    def __set_profile(self, index):
        """
            Sets connection details with index of combo box

            Arguments:
                index: Last changed index of combo box
        """
        if len(self.profiles)>=0 and len(self.profiles)>=index and index>=0:
            self.set_domain(self.profiles[index].get_domain())
            self.set_host(self.profiles[index].get_address())
            self.set_user(self.profiles[index].get_username())
            self.editPassword.setFocus()

    def __fill_profiles(self):
        """
            Adds profile names into combo box
        """
        if len(self.profiles):
            for index in range(0, len(self.profiles)):
                self.comboDomain.addItem(self.profiles[index].get_domain())
        pass

    def __slot_find_host(self):
        """
            When user finishes editing "domain" field, tries to fill
            host field if possible.
        """
        if len(self.comboDomain.currentText()) and not self.editHost.isModified():
            try:
                host = socket.gethostbyname(str(self.comboDomain.currentText()))
            except socket.error:
                return
            self.editHost.setText(host)

    def get_host(self):
        """
            Returns hostname.
        """
        return str(self.editHost.text())

    def get_domain(self):
        """
            Returns domain name.
        """
        return str(self.comboDomain.currentText())

    def get_user(self):
        """
            Returns user name.
        """
        return str(self.editUser.text())

    def get_password(self):
        """
            Returns user password.
        """
        return str(self.editPassword.text())

    def set_host(self, host):
        """
            Sets hostname.
        """
        self.editHost.setText(host)

    def set_domain(self, domain):
        """
            Sets domain name.
        """
        self.comboDomain.setEditText(domain)

    def set_user(self, user):
        """
            Sets user name.
        """
        self.editUser.setText(user)

    def set_password(self, password):
        """
            Sets user password.
        """
        self.editPassword.setText(password)

    def __check_fields(self, set_focus=False):
        """
            Checks fields for errors:

            Returns: True if valid, else False
        """
        # if self.editDomain.isModified() and not len(self.editDomain.text()):
        if not len(self.comboDomain.currentText()):
            self.labelWarning.setText("Domain name is required.")
            if set_focus:
                self.comboDomain.setFocus(QtCore.Qt.OtherFocusReason)
            return False
        if self.editHost.isModified() and not len(self.editHost.text()):
            self.labelWarning.setText("Server address is required.")
            if set_focus:
                self.editHost.setFocus(QtCore.Qt.OtherFocusReason)
            return False
        if self.editUser.isModified() and not len(self.editUser.text()):
            self.labelWarning.setText("User name is required.")
            if set_focus:
                self.editUser.setFocus(QtCore.Qt.OtherFocusReason)
            return False
        self.labelWarning.setText("")
        return True

    def accept(self):
        last_profile = profile.Profile(self.comboDomain.currentText(),
                self.editHost.text(),
                self.editUser.text())

        # Create Profile Writer to save last connected profile to the top of recent profiles
        writer = profilewriter.ProfileWriter()
        writer.save_as_last_profile(last_profile)


        if self.__check_fields(set_focus=True):
            QtGui.QDialog.accept(self)

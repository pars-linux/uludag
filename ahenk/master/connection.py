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
from ui_connection import Ui_dialogConnection


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
        self.connect(self.editDomain, QtCore.SIGNAL("editingFinished()"), self.__slot_find_host)

    def __slot_find_host(self):
        """
            When user finishes editing "domain" field, tries to fill
            host field if possible.
        """
        if len(self.editDomain.text()) and not self.editHost.isModified():
            try:
                host = socket.gethostbyname(str(self.editDomain.text()))
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
        return str(self.editDomain.text())

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
        self.editDomain.setText(domain)

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

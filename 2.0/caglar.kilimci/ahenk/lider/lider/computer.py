#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Computer dialog
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.ui_computer import Ui_dialogComputer


class DialogComputer(QtGui.QDialog, Ui_dialogComputer):
    """
        Dialog for computers.

        Usage:
            dialog = DialogComputer(form)
            dialog.set_name("test1)
            if dialog.exec_():
                print dialog.get_password()
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

    def get_name(self):
        """
            Returns name.
        """
        return str(self.editName.text())

    def get_password(self):
        """
            Returns password.
        """
        from lider.helpers.directory import Directory
        password = str(self.editPassword.text())
        salted = Directory.make_password(password)
        return salted

    def set_name(self, user):
        """
            Sets computer name.
        """
        self.editName.setText(user)

    def set_password(self, password):
        """
            Sets password.
        """
        self.editPassword.setText(password)

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
        # Signals for password matching control
        self.connect(self.editPassword, QtCore.SIGNAL("textChanged(QString)"), self.__slotPasswordTextChanged)
        self.connect(self.editConfirmPassword, QtCore.SIGNAL("textChanged(QString)"), self.__slotPasswordTextChanged)

        self.labelWarning.hide()


    def __slotPasswordTextChanged(self):
        """
            If password confirmation field is not empty, compare password and its confirmation field whether same or not.
            If they are not same, show warning label.
        """
        if len(str(self.editConfirmPassword.text())):
            if self.editPassword.text() == self.editConfirmPassword.text():
                self.labelWarning.hide()
            else:
                self.labelWarning.show()

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

    def get_description(self):
        """
            Returns LDAP attribute name.
        """
        return str(self.editDescription.text())


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

    def set_description(self, password):
        """
            Sets LDAP attribute name.
        """
        self.editDescription.setText(password)

    def accept(self):
        """
            Checks written passwords are same or not. If not, warn user.
        """
        if not (self.editPassword.text() == self.editConfirmPassword.text()):
            QtGui.QMessageBox.warning(self, "Computer Adding..", "Passwords do not match.")
        else:
            QtGui.QDialog.accept(self)

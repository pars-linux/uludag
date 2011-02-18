#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    User dialog
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.ui_user import Ui_dialogUser


class DialogUser(QtGui.QDialog, Ui_dialogUser):
    """
        Dialog for users.

        Usage:
            dialog = DialogUser(form)
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

        self.connect(self.editName, QtCore.SIGNAL("textChanged(QString)"), self.__slotNameTextChanged)
        self.connect(self.editPassword, QtCore.SIGNAL("textChanged(QString)"), self.__slotPasswordTextChanged)
        self.connect(self.editConfirmPassword, QtCore.SIGNAL("textChanged(QString)"), self.__slotPasswordTextChanged)

        self.labelWarning.hide()

    def __slotNameTextChanged(self):
        if not (self.editHomeDir.isModified()):
            self.editHomeDir.setText(self.editName.text())

    def __slotPasswordTextChanged(self):
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

    def get_uid(self):
        """
            Returns user ID.
        """
        return str(self.spinUID.value())

    def get_gid(self):
        """
            Returns group ID.
        """
        return str(self.spinGID.value())

    def set_name(self, user):
        """
            Sets user name.
        """
        self.editName.setText(user)

    def set_password(self, password):
        """
            Sets password.
        """
        self.editPassword.setText(password)

    def set_uid(self, uid):
        """
            Sets user id.
        """
        self.spinUID.setValue(uid)

    def set_gid(self, gid):
        """
            Sets group id.
        """
        self.spinGID.setValue(uid)

    def accept(self):
        if not (self.editPassword.text() == self.editConfirmPassword.text()):
            print "Passwords do not match."
            QtGui.QMessageBox.warning(self, "User Adding..", "Passwords do not match.")
            return
        else:
            QtGui.QDialog.accept(self)

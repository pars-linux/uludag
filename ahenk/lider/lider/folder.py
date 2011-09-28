#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Folder dialog
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.ui_folder import Ui_dialogFolder
from lider.helpers import i18n

i18n = i18n.i18n

class DialogFolder(QtGui.QDialog, Ui_dialogFolder):
    """
        Dialog for folders.

        Usage:
            dialog = DialogFolder(form)
            dialog.set_name("test1)
            if dialog.exec_():
                print dialog.get_label()
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

        # Name must be alphanumeric only
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('^[a-zA-Z0-9_-]+$'), self)
        self.editName.setValidator(validator)

    def get_name(self):
        """
            Returns name.
        """
        return str(self.editName.text())

    def get_label(self):
        """
            Returns label.
        """
        return str(self.editLabel.text())

    def get_description(self):
        """
            Returns LDAP attribute name.
        """
        return str(self.editDescription.text())

    def set_name(self, user):
        """
            Sets name.
        """
        self.editName.setText(user)
        self.editName.setEnabled(False)

    def set_label(self, label):
        """
            Sets label.
        """
        self.editLabel.setText(unicode(label))

    def set_description(self, description):
        """
            Sets description.
        """
        self.editDescription.setText(unicode(description))

    def accept(self):
        if not len(self.editName.text()):
            QtGui.QMessageBox.warning(self, i18n("Folder"), i18n("Folder name is missing"))
        elif not len(self.editLabel.text()):
            QtGui.QMessageBox.warning(self, i18n("Folder"), i18n("Folder label is missing"))
        else:
            QtGui.QDialog.accept(self)

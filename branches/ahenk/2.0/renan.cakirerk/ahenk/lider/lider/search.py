#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Search dialog
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.ui_search import Ui_dialogSearch


class DialogSearch(QtGui.QDialog, Ui_dialogSearch):
    """
        Dialog for search items in network.

        Usage:
            dialog = DialogSearch(form)
            if dialog.exec_():
                print dialog.get_query()
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

    def get_query(self):
        """
            Returns query string.
        """
        return str(self.editQuery.text())

    def set_query(self, user):
        """
            Sets query string.
        """
        self.editQuery.setText(user)

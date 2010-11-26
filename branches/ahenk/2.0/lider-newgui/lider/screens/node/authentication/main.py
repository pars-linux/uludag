#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Authentication
"""

# Standard modules
#

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_authentication import Ui_widgetAuthentication

# Helper modules
#


class WidgetModule(QtGui.QWidget, Ui_widgetAuthentication):
    """
        Authentication UI.
    """
    def __init__(self, parent=None):
        """
            Constructor for main window.

            Arguments:
                parent: Parent object
        """
        QtGui.QWidget.__init__(self, parent)

        # Attach generated UI
        self.setupUi(self)

        # UI events
        #

        # UI initialization
        #

    def showEvent(self, event):
        """
            Things to do before widget is shown.
        """
        pass

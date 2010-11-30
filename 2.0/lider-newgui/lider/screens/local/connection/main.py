#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Connection
"""

# Standard modules
#

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_connection import Ui_widgetConnection

# Helper modules
#


class WidgetModule(QtGui.QWidget, Ui_widgetConnection):
    """
        Connection UI.
    """

    connected = QtCore.pyqtSignal()

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
        self.connect(self.pushConnect, QtCore.SIGNAL("clicked()"), self.__slot_connect)

        # UI initialization
        #

    def showEvent(self, event):
        """
            Things to do before widget is shown.
        """
        pass

    def __slot_connect(self):
        """
            Triggered when user clicks "Connect" button
        """
        self.connected.emit()

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Search
"""

# Standard modules
#

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_search import Ui_widgetSearch

# Helper modules
#


class WidgetModule(QtGui.QWidget, Ui_widgetSearch):
    """
        Search UI
    """

    selectedItem = QtCore.pyqtSignal()

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
        self.connect(self.listNetwork, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.__slot_item_clicked)

        # UI initialization
        #

    def showEvent(self, event):
        """
            Things to do before widget is shown.
        """
        pass

    def get_mini(self, parent):
        """
            Generates mini version on the fly for embedding into Node screen.
        """
        widget = QtGui.QListWidget(parent)

        item_0 = QtGui.QListWidgetItem(widget)
        item_0.setText("Item 0")
        item_1 = QtGui.QListWidgetItem(widget)
        item_1.setText("Item 1")

        return widget

    def __slot_item_clicked(self, item):
        """
            Triggered when user clicks an item.
        """
        self.selectedItem.emit()

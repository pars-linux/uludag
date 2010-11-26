#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Network tree
"""

# Standard modules
#

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_tree import Ui_widgetTree

# Helper modules
#


class WidgetModule(QtGui.QWidget, Ui_widgetTree):
    """
        Network tree UI
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

    def get_mini(self, parent):
        """
            Generates mini version on the fly for embedding into Node screen.
        """
        from minitree import WidgetMiniTree
        widget = WidgetMiniTree(parent)
        return widget

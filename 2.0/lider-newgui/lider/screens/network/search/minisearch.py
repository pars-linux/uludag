#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Network mini search
"""

# Standard modules
#

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_minisearch import Ui_widgetSearch

# Helper modules
#


class WidgetMiniSearch(QtGui.QWidget, Ui_widgetSearch):
    """
        Network mini search UI
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

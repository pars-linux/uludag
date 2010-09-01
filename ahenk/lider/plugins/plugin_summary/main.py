#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    System summary module
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from plugins.plugin_summary.ui_summary import Ui_widgetSummary

# Helper modules
from helpers import plugins


class WidgetModule(QtGui.QWidget, Ui_widgetSummary):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

    def get_type(self):
        return plugins.TYPE_GLOBAL

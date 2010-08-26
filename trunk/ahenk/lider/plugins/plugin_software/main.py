#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from plugins.plugin_software.ui_software import Ui_widgetSoftware


WidgetLabel = "Software Update"


class WidgetModule(QtGui.QWidget, Ui_widgetSoftware):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

    def load_policy(self, policy):
        pass

    def dump_policy(self):
        return {"x": [1], "pisiAutoUpdateMode": ["security"]}

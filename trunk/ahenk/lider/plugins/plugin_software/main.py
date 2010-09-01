#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Software magement module
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from plugins.plugin_software.ui_software import Ui_widgetSoftware

# Helper modules
from helpers import plugins


class WidgetModule(QtGui.QWidget, Ui_widgetSoftware):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

    def get_type(self):
        return plugins.TYPE_SINGLE

    def load_policy(self, policy):
        text = [
            "softwareRepositories = %s" % policy.get("softwareRepositories", ""),
            "softwareUpdateSchedule = %s" % policy.get("softwareUpdateSchedule", ""),
            "softwareUpdateMode = %s" % policy.get("softwareUpdateMode", "off"),
        ]
        text = "\n".join(text)
        self.textPolicy.setPlainText(text)

    def dump_policy(self):
        return {}

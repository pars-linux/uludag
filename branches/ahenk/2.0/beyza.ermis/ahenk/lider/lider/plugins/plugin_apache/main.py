#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Software magement module
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_apache import Ui_widgetApache

# Helper modules
from lider.helpers import plugins
from lider.helpers import wrappers

import pisi

class WidgetModule(QtGui.QWidget, Ui_widgetApache, plugins.PluginWidget):
    """
        Software management UI.
    """
    def __init__(self, parent=None):
        """
            Constructor for main window.

            Arguments:
                parent: Parent object
        """
        plugins.PluginWidget.__init__(self)
        QtGui.QWidget.__init__(self, parent)

        # Attach generated UI
        self.setupUi(self)

    def get_type(self):
        """
            Widget type.

            Should return TYPE_GLOBAL or TYPE_SINGLE
        """
        return plugins.TYPE_SINGLE

    def get_classes(self):
        """
            Returns a list of policy class names.
        """
        return ["apachePolicy"]

    def is_installed(self, package):
        return package in pisi.api.list_installed()

    def load_policy(self, policy):
        """
            Main window calls this method when policy is fetched from directory.
            Not required for global widgets.
        """
        if (self.is_installed("apache")):
            apacheDomains = policy.get("apacheDomains", [])
            domains = "\n".join(apacheDomains)
            self.textDomains.setPlainText(domains)
        else:
            self.warningLabel.setEnabled(True)
            self.domainLabel.setEnabled(False)
            self.textDomains.setEnabled(False)

    def dump_policy(self):
        """
            Main window calls this method to get policy generated by UI.
            Not required for global widgets.
        """
        apacheDomains = str(self.textDomains.toPlainText()).split("\n")
        # New policy
        policy = {
               "apacheDomains": apacheDomains
               }
        return policy



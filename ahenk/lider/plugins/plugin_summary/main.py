#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    System summary module
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.plugins.plugin_summary.ui_summary import Ui_widgetSummary

# Helper modules
from lider.helpers import plugins


class WidgetModule(QtGui.QWidget, Ui_widgetSummary, plugins.PluginWidget):
    """
        System summary UI.
    """
    def __init__(self, parent=None):
        """
            Constructor for plugin widget.

            Arguments:
                parent: Parent object
        """
        plugins.PluginWidget.__init__(self)
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

    def showEvent(self, event):
        """
            Things to do before widget is shown.
        """
        pass

    def get_type(self):
        """
            Widget type.

            Should return TYPE_GLOBAL or TYPE_SINGLE
        """
        return plugins.TYPE_GLOBAL


    def load_policy(self, policy):
        """
            Main window calls this method when policy is fetched from directory.
            Not required for global widgets.
        """
        pass

    def dump_policy(self):
        """
            Main window calls this method to get policy generated by UI.
            Not required for global widgets.
        """
        return {}

    def talk_message(self, sender, message):
        """
            Main window calls this method when an XMPP message is received.
        """
        pass

    def talk_status(self, sender, status):
        """
            Main window calls this method when an XMPP status is changed.
        """
        pass

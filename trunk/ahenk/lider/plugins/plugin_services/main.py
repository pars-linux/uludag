#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Software magement module
"""

# Standard modules
import simplejson

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.plugins.plugin_services.ui_services import Ui_widgetServices

# Helper modules
from lider.helpers import plugins
from lider.helpers import wrappers


class WidgetModule(QtGui.QWidget, Ui_widgetServices, plugins.PluginWidget):
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

        # UI events

    def showEvent(self, event):
        """
            Things to do before widget is shown.
        """
        jid = "%s@%s" % (self.item.name, self.talk.domain)
        self.talk.send_command(jid, "service.info")

    def get_type(self):
        """
            Widget type.

            Should return TYPE_GLOBAL or TYPE_SINGLE
        """
        return plugins.TYPE_SINGLE

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
        policy = {
        }
        return policy

    def talk_message(self, sender, command, arguments=None):
        """
            Main window calls this method when an XMPP message is received.
        """
        print command, arguments
        if command == "service.info":
            self.listServices.clear()
            for name, desc, status in arguments:
                item = QtGui.QListWidgetItem(self.listServices)
                item.setText("%s - %s" % (name, status))

    def talk_status(self, sender, status):
        """
            Main window calls this method when an XMPP status is changed.
        """
        pass

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Web browser module
"""

# Standard modules
import simplejson

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from plugins.plugin_web.ui_web import Ui_widgetWeb

# Helper modules
from helpers import plugins
from helpers import talk


class WidgetModule(QtGui.QWidget, Ui_widgetWeb, plugins.PluginWidget):
    """
        Web browser UI.
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

        self.connect(self.pushRefresh, QtCore.SIGNAL("clicked()"), self.__slot_refresh)
        self.connect(self.comboComputers, QtCore.SIGNAL("activated(int)"), self.__slot_select)

    def showEvent(self, event):
        """
            Things to do before widget is shown.
        """
        self.comboComputers.clear()
        self.comboComputers.addItem("Select...")
        for username in self.talk.online:
            self.comboComputers.addItem(username)

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
        try:
            command, reply = message.split(":", 1)
            reply = simplejson.loads(reply)
        except (ValueError, simplejson.JSONDecodeError):
            return
        if command == "apache info":
            if reply == False:
                self.webView.setHtml("Web server is not installed.")
            elif reply == True:
                self.webView.setHtml("Web server is installed but not running.")
            else:
                self.webView.setUrl(QtCore.QUrl(reply))

    def talk_status(self, sender, status):
        """
            Main window calls this method when an XMPP status is changed.
        """
        if status == talk.Online:
            for i in range(1, self.comboComputers.count()):
                if sender == str(self.comboComputers.itemText(i)):
                    return
            self.comboComputers.addItem(sender)
        elif status == talk.Offline:
            for i in range(1, self.comboComputers.count()):
                if sender == str(self.comboComputers.itemText(i)):
                    self.comboComputers.removeItem(i)
                    return

    def __slot_refresh(self):
        """
            Triggered when users clicks refresh button.
        """
        self.webView.reload()

    def __slot_select(self, index):
        """
            Triggered when users selects a computer.
        """
        if index == 0:
            self.webView.setHtml("")
        else:
            name = str(self.comboComputers.itemText(index))
            jid = "%s@%s" % (name, self.talk.domain)
            self.talk.send_message(jid, "apache info")

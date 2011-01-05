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
from ui_web import Ui_widgetWeb

# Helper modules
from lider.helpers import plugins
from lider.helpers import talk


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

        # Attach generated UI
        self.setupUi(self)

        # Fine tune UI
        self.pushBack.setEnabled(False)
        self.pushForward.setEnabled(False)
        self.pushReload.setEnabled(False)
        self.pushPrint.setEnabled(False)

        # UI events
        self.connect(self.pushRefresh, QtCore.SIGNAL("clicked()"), self.__slot_refresh)
        self.connect(self.comboComputers, QtCore.SIGNAL("activated(int)"), self.__slot_select)
        self.connect(self.comboServices, QtCore.SIGNAL("activated(int)"), self.__slot_select2)
        self.connect(self.webView, QtCore.SIGNAL("loadFinished(bool)"), self.__slot_web_loaded)
        self.connect(self.pushBack, QtCore.SIGNAL("clicked()"), self.__slot_web_back)
        self.connect(self.pushForward, QtCore.SIGNAL("clicked()"), self.__slot_web_forward)
        self.connect(self.pushReload, QtCore.SIGNAL("clicked()"), self.__slot_web_reload)
        self.connect(self.pushPrint, QtCore.SIGNAL("clicked()"), self.__slot_web_print)

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

    def talk_message(self, sender, message, arguments=None):
        """
            Main window calls this method when an XMPP message is received.
        """
        if message == "apache.info":
            self.comboServices.clear()
            self.comboServices.addItem("Select...")
            for name, url in arguments.iteritems():
                self.comboServices.addItem(name, QtCore.QVariant(url))

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
        index = self.comboComputers.currentIndex()
        self.__slot_select(index)

    def __slot_select(self, index):
        """
            Triggered when users selects a computer.
        """
        if index == 0:
            self.webView.setHtml("")
            self.comboServices.clear()
            self.comboServices.addItem("Select...")
        else:
            name = str(self.comboComputers.itemText(index))
            jid = "%s@%s" % (name, self.talk.domain)
            self.talk.send_command(jid, "apache.info")

    def __slot_select2(self, index):
        """
            Triggered when users selects a computer.
        """
        if index == 0:
            self.webView.setHtml("")
        else:
            url = self.comboServices.itemData(index).toString()
            self.webView.setUrl(QtCore.QUrl(url))

    def __slot_web_loaded(self, ok):
        """
            Triggered when web browser finishes loading.
        """
        history = self.webView.history()
        self.pushBack.setEnabled(history.canGoBack())
        self.pushForward.setEnabled(history.canGoForward())
        self.pushReload.setEnabled(True)
        self.pushPrint.setEnabled(True)

    def __slot_web_back(self):
        """
            Triggered when user clicks "Back" button.
        """
        self.webView.back()

    def __slot_web_forward(self):
        """
            Triggered when user clicks "Forward" button.
        """
        self.webView.forward()

    def __slot_web_reload(self):
        """
            Triggered when user clicks "Reload" button.
        """
        self.webView.stop()
        self.webView.reload()

    def __slot_web_print(self):
        """
            Triggered when user clicks "Print" button.
        """
        dialog = QtGui.QPrintDialog(self)
        dialog.exec_()
        printer = dialog.printer()
        self.webView.print_(printer)
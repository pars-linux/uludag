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
from ui_services import Ui_widgetServices

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
        self.connect(self.pushStart, QtCore.SIGNAL("clicked()"), self.__slot_start_service)
        self.connect(self.pushStop, QtCore.SIGNAL("clicked()"), self.__slot_stop_service)

        # Package index
        self.package_index = {}

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
        if command == "service.info":
            self.tableWidget.setRowCount(len(arguments))

            index = 0

            for name, desc, status in arguments:
                item_description = QtGui.QTableWidgetItem(str(desc))
                self.tableWidget.setItem(index, 0, item_description)

                item_name = QtGui.QTableWidgetItem(str(name))
                self.tableWidget.setItem(index, 3, item_name)

                if status in ['started', 'on', 'conditional_started']:
                    item_status = QtGui.QTableWidgetItem("Running")
                else:
                    item_status = QtGui.QTableWidgetItem("Stopped")
                self.tableWidget.setItem(index, 1, item_status)

                if status in ['stopped', 'on']:
                    item_autostart = QtGui.QTableWidgetItem("Yes")
                elif status in ['conditional_started', 'conditional_stopped']:
                    item_autostart = QtGui.QTableWidgetItem("Conditional")
                else:
                    item_autostart = QtGui.QTableWidgetItem("No")
                self.tableWidget.setItem(index, 2, item_autostart)

                index += 1

    def talk_status(self, sender, status):
        """
            Main window calls this method when an XMPP status is changed.
        """
        pass

    def __slot_start_service(self):
        """
            This method is called when the start button clicked to start the selected service
        """
        item = self.tableWidget.selectedItems()
        item_name = str(item[3].text())

        jid = "%s@%s" % (self.item.name, self.talk.domain)
        self.talk.send_command(jid, "service.start", [item_name])

    def __slot_stop_service(self):
        """
            This method is called when the stop button clicked to stop the selected service
        """
        item = self.tableWidget.selectedItems()
        item_name = str(item[3].text())

        jid = "%s@%s" % (self.item.name, self.talk.domain)
        self.talk.send_command(jid, "service.stop", [item_name])

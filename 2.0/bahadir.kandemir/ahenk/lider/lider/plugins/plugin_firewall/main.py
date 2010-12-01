#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Firewall magement module
"""

# Standard library
import base64
import bz2
import os
import re
import signal
import subprocess
import tempfile

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_firewall import Ui_widgetFirewall

# Helper modules
from lider.helpers import plugins
from lider.helpers import wrappers


class WidgetModule(QtGui.QWidget, Ui_widgetFirewall, plugins.PluginWidget):
    """
        Firewall management UI.
    """
    def __init__(self, parent=None):
        """
            Constructor for main window.

            Arguments:
                parent: Parent object
        """
        plugins.PluginWidget.__init__(self)
        QtGui.QWidget.__init__(self, parent)

        # Rules
        self.rules_xml = ""
        self.rules_compiled = ""

        # Attach generated UI
        self.setupUi(self)

        # UI events
        self.connect(self.pushEdit, QtCore.SIGNAL("clicked()"), self.__slot_edit)
        self.connect(self.pushReset, QtCore.SIGNAL("clicked()"), self.__slot_reset)

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
        return plugins.TYPE_SINGLE

    def get_classes(self):
        """
            Returns a list of policy class names.
        """
        return ["firewallPolicy"]

    def load_policy(self, policy):
        """
            Main window calls this method when policy is fetched from directory.
            Not required for global widgets.
        """
        firewallState = policy.get("firewallState", ["off"])[0]
        self.groupFirewall.setChecked(firewallState == "on")

        firewallRules = policy.get("firewallRules", [""])[0]

        rules_xml = ""
        rules_compiled = ""

        if len(firewallRules):
            try:
                rules_xml, rules_compiled = firewallRules.split(":")

                rules_xml = base64.decodestring(rules_xml)
                rules_xml = bz2.decompress(rules_xml)

                rules_compiled = base64.decodestring(rules_compiled)
                rules_compiled = bz2.decompress(rules_compiled)
            except Exception:
                pass

        self.rules_xml = rules_xml
        self.rules_compiled = rules_compiled

    def dump_policy(self):
        """
            Main window calls this method to get policy generated by UI.
            Not required for global widgets.
        """
        firewallState = "off"
        if self.groupFirewall.isChecked():
            firewallState = "on"

        rules_xml = bz2.compress(self.rules_xml)
        rules_xml = base64.encodestring(rules_xml)

        rules_compiled = bz2.compress(self.rules_compiled)
        rules_compiled = base64.encodestring(rules_compiled)

        firewallRules = rules_xml + ":" + rules_compiled

        policy = {
            "firewallState": [firewallState],
            "firewallRules": [firewallRules],
        }
        return policy

    def talk_message(self, sender, command, arguments=None):
        """
            Main window calls this method when an XMPP message is received.
        """
        pass

    def talk_status(self, sender, status):
        """
            Main window calls this method when an XMPP status is changed.
        """
        pass

    def __slot_edit(self):
        """
            Triggered when user clicks 'Edit Rules' button.
        """
        fp = tempfile.NamedTemporaryFile(delete=False)
        name = fp.name
        if len(self.rules_xml):
            fp.write(self.rules_xml)
        else:
            fp.write(file("/usr/share/ahenk-lider/firewall.fwb").read())
        fp.close()

        self.labelFirewall.setText("")

        process = subprocess.Popen(["/usr/bin/fwbuilder", "-d", name], stderr=subprocess.PIPE)
        while True:
            if "delayedQuit" in process.stderr.readline():
                os.kill(process.pid, signal.SIGINT)
                break

        fw_name = re.findall('Firewall.*iptables.*name="([a-zA-Z0-9\-_]+)"', file(name).read())[0]

        ret = os.system("/usr/bin/fwb_ipt -q -f %s -o %s.sh %s" % (name, name, fw_name))
        if ret != 0:
            self.labelFirewall.setText("Unable to compile firewall rules.")
            return

        self.rules_xml = file(name).read()
        self.rules_compiled = file(name + ".sh").read()

    def __slot_reset(self):
        """
            Triggered when user clicks 'Reset Rules' button.
        """
        fp = tempfile.NamedTemporaryFile(delete=False)
        name = fp.name
        fp.write(file("/usr/share/ahenk-lider/firewall.fwb").read())
        fp.close()

        self.labelFirewall.setText("")

        fw_name = re.findall('Firewall.*iptables.*name="([a-zA-Z0-9\-_]+)"', file(name).read())[0]

        ret = os.system("/usr/bin/fwb_ipt -q -f %s -o %s.sh %s" % (name, name, fw_name))
        if ret != 0:
            return

        self.rules_xml = file(name).read()
        self.rules_compiled = file(name + ".sh").read()

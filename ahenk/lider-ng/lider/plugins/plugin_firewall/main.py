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
from lider import wrappers


class ThreadFW(QtCore.QThread):
    def __init__(self, group_name= None, rules_xml=None):
        QtCore.QThread.__init__(self)

        self.status = None
        self.error = ""

        if group_name:
            self.group_name = group_name
        else:
            self.group_name = "Firewall"

        if len(rules_xml):
            self.rules_xml = rules_xml
        else:
            self.rules_xml = file("/usr/share/ahenk-lider/firewall.fwb").read()

        self.rules_compiled = ""

    def run(self):
        fp = tempfile.NamedTemporaryFile(delete=False)
        name = fp.name
        fp.write(self.rules_xml)
        fp.close()

        process = subprocess.Popen(["/usr/bin/fwbuilder", "-d", name], stderr=subprocess.PIPE)
        while True:
            if "delayedQuit" in process.stderr.readline():
                os.kill(process.pid, signal.SIGINT)
                break

        self.rules_xml = file(name).read()
        fw_name = re.findall('Firewall.*iptables.*name="([a-zA-Z0-9\-_]+)"', self.rules_xml)[0]

        process = subprocess.Popen(["/usr/bin/fwb_ipt", "-q", "-f", name, "-o", "%s.sh" % name, fw_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.wait() != 0:
            self.status = False
            self.error = process.stderr.read()
            return

        self.status = True

        data = file(name + ".sh").read()

        # Disable "start" method clearing whole rule set
        data = re.sub('(reset_all )', '#\\1', data)

        # Add NAT log rules
        data = re.sub('    echo \"Rule ([0-9]+) \(NAT\)\"\n    # \n    \$IPTABLES \-t nat (.*) \-j DNAT (.*)',
                      '    echo "Rule \\1 (NAT)"\n    # \n    $IPTABLES -t nat \\2 -j DNAT \\3\n    $IPTABLES -t nat \\2 -j LOG  --log-level info --log-prefix "RULE \\1 -- TRANSLATE " \\3',
                      data,
                      re.MULTILINE)

        # Add log prefixes
        data = re.sub('RULE_', '%s_RULE_' % self.group_name, data)
        data = re.sub('"RULE ', '"%s RULE ' % self.group_name, data)

        self.rules_compiled = data


class WidgetModule(QtGui.QWidget, Ui_widgetFirewall):
    """
        Firewall management UI.
    """
    def __init__(self, parent=None):
        """
            Constructor for main window.

            Arguments:
                parent: Parent object
        """
        QtGui.QWidget.__init__(self, parent)

        # Rules
        self.rules_xml = ""
        self.rules_compiled = ""

        # Attach generated UI
        self.setupUi(self)

        # FW Builder thread
        self.thread = None

        # UI events
        self.connect(self.radioEnable, QtCore.SIGNAL("clicked()"), self.__slot_status)
        self.connect(self.radioDisable, QtCore.SIGNAL("clicked()"), self.__slot_status)
        self.connect(self.pushEdit, QtCore.SIGNAL("clicked()"), self.__slot_edit)
        self.connect(self.pushReset, QtCore.SIGNAL("clicked()"), self.__slot_reset)

    def load_policy(self, policy):
        firewallState = policy.get("firewallState", ["off"])[0]
        if firewallState == "on":
            self.radioEnable.setChecked(True)
        else:
            self.radioDisable.setChecked(True)
        self.__slot_status()

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
        firewallState = "off"
        if self.radioEnable.isChecked():
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

    def __slot_thread(self):
        if self.thread.isFinished():
            self.rules_xml = self.thread.rules_xml
            self.rules_compiled = self.thread.rules_compiled
            if self.thread.status:
                self.plainTextEdit.setPlainText("")
            else:
                self.plainTextEdit.setPlainText(self.thread.error)
        self.pushEdit.setEnabled(True)
        self.pushReset.setEnabled(True)

    def __slot_edit(self):
        """
            Triggered when user clicks 'Edit Rules' button.
        """
        if self.item:
            name = self.item.name
            name = name.upper()
        else:
            name = "Group"

        self.pushEdit.setEnabled(False)
        self.pushReset.setEnabled(False)
        self.thread = ThreadFW(name, self.rules_xml)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.__slot_thread)
        self.thread.start()

    def __slot_reset(self):
        """
            Triggered when user clicks 'Reset Rules' button.
        """
        fp = tempfile.NamedTemporaryFile(delete=False)
        name = fp.name
        fp.write(file("/usr/share/ahenk-lider/firewall.fwb").read())
        fp.close()

        self.plainTextEdit.setPlainText("")

        fw_name = re.findall('Firewall.*iptables.*name="([a-zA-Z0-9\-_]+)"', file(name).read())[0]

        process = subprocess.Popen(["/usr/bin/fwb_ipt", "-q", "-f", name, "-o", "%s.sh" % name, fw_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.wait() != 0:
            return

        self.rules_xml = file(name).read()
        self.rules_compiled = file(name + ".sh").read()

    def __slot_status(self):
        """
            Triggered when user changes firewall status.
        """
        if self.radioEnable.isChecked():
            icon = wrappers.Icon("secure64", 64)
        else:
            icon = wrappers.Icon("insecure64", 64)

        pixmap = icon.pixmap(64, 64)
        self.pixmapStatus.setPixmap(pixmap)

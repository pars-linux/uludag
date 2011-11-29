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
from lider.helpers import i18n

i18n = i18n.i18n

class ThreadFW(QtCore.QThread):
    def __init__(self, group_name= None, rules_xml=None):
        QtCore.QThread.__init__(self)

        self.status = None
        self.out = ""
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

        process = subprocess.Popen(["/usr/bin/fwbuilder", "-d", name], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
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
        self.out = process.stdout.read()

        data = file(name + ".sh").read()

        # Disable "start" method clearing whole rule set
        data = re.sub('(reset_all )', '#\\1', data)

        # Add NAT log rules
        data = re.sub('    echo \"Rule ([0-9]+) \(NAT\)\"\n    # \n    \$IPTABLES \-t nat (.*) \-j DNAT (.*)',
                      '    echo "Rule \\1 (NAT)"\n    # \n    $IPTABLES -t nat \\2 -j DNAT \\3\n    $IPTABLES -t nat \\2 -j ULOG --ulog-nlgroup 1 --ulog-prefix "RULE \\1 -- TRANSLATE " --ulog-qthreshold 1 \\3',
                      data,
                      re.MULTILINE)

        # Add log prefixes
        data = re.sub('RULE_', '%s_RULE_' % self.group_name, data)
        data = re.sub('"RULE ', '"%s RULE ' % self.group_name, data)

        # Add log rules for established and related connections
        data = re.sub('    \$IPTABLES \-A INPUT   \-m state \-\-state ESTABLISHED,RELATED \-j ACCEPT ',
                      '    $IPTABLES -A INPUT   -m state --state ESTABLISHED,RELATED -m limit --limit 1/minute -j ULOG --ulog-nlgroup 1 --ulog-prefix "ESTABLISHED or RELATED" --ulog-qthreshold 1\n    $IPTABLES -A INPUT   -m state --state ESTABLISHED,RELATED -j ACCEPT ',
                      data)

        data = re.sub('    \$IPTABLES \-A OUTPUT  \-m state \-\-state ESTABLISHED,RELATED \-j ACCEPT ',
                      '    $IPTABLES -A OUTPUT  -m state --state ESTABLISHED,RELATED -m limit --limit 1/minute -j ULOG --ulog-nlgroup 1 --ulog-prefix "ESTABLISHED or RELATED" --ulog-qthreshold 1\n    $IPTABLES -A OUTPUT  -m state --state ESTABLISHED,RELATED -j ACCEPT ',
                      data)

        data = re.sub('    \$IPTABLES \-A FORWARD \-m state \-\-state ESTABLISHED,RELATED \-j ACCEPT',
                      '    $IPTABLES -A FORWARD -m state --state ESTABLISHED,RELATED -m limit --limit 1/minute -j ULOG --ulog-nlgroup 1 --ulog-prefix "ESTABLISHED or RELATED" --ulog-qthreshold 1\n    $IPTABLES -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT ',
                      data)

        self.rules_compiled = data

    #def __slot_modify_default_rules(self):
        # Save changes to default firewall settings file
        #f = open('/usr/share/ahenk-lider/firewall.fwb', 'w+')
        #f.write(self.rules_xml)
        #f.close()
         

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

        # FW Builder thread
        self.thread = None

        # UI events
        #self.connect(self.radioEnable, QtCore.SIGNAL("clicked()"), self.__slot_status)
        #self.connect(self.radioDisable, QtCore.SIGNAL("clicked()"), self.__slot_status)
        self.connect(self.pushEdit, QtCore.SIGNAL("clicked()"), self.__slot_edit)
        self.connect(self.pushReset, QtCore.SIGNAL("clicked()"), self.__slot_reset)
        self.connect(self.pushFailsafe, QtCore.SIGNAL("clicked()"), self.__slot_load_failsafe_rules)

    def set_item(self, item):
        """
            Sets directory item that is being worked on.
            Not required for global widgets.
        """
        pass

    # def showEvent(self, event):
    def showEvent(self):
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

        """
        firewallState = policy.get("firewallState", ["off"])[0]
        if firewallState == "on":
            self.radioEnable.setChecked(True)
        else:
            self.radioDisable.setChecked(True)
        self.__slot_status()
        """
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

        """
        firewallState = "off"
        if self.radioEnable.isChecked():
            firewallState = "on"
        """

        rules_xml = bz2.compress(self.rules_xml)
        rules_xml = base64.encodestring(rules_xml)

        rules_compiled = bz2.compress(self.rules_compiled)
        rules_compiled = base64.encodestring(rules_compiled)

        firewallRules = rules_xml + ":" + rules_compiled

        # Disable firewall state for now
        policy = {
            #"firewallState": [firewallState],
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

    def __slot_thread(self):
        if self.thread.isFinished():
            self.rules_xml = self.thread.rules_xml
            self.rules_compiled = self.thread.rules_compiled
            if self.thread.status:
                self.plainTextEdit.setPlainText(self.thread.out)
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

        self.plainTextEdit.setPlainText("")

        self.pushEdit.setEnabled(False)
        self.pushReset.setEnabled(False)
        self.thread = ThreadFW(name, self.rules_xml)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.__slot_thread)
        self.thread.start()

    def __slot_reset(self):
        """
            Triggered when user clicks 'Reset Rules' button.
        """
        msg = QtGui.QMessageBox(self)
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setText(i18n("Default firewall rules will be loaded."))
        msg.setInformativeText(i18n("Do you want to continue?"))
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msg.setDefaultButton(QtGui.QMessageBox.No)

        if msg.exec_() != QtGui.QMessageBox.Yes:
            return

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

        self.plainTextEdit.setPlainText(i18n("Default rules were loaded"))

    def __slot_load_failsafe_rules(self):
        """
            Triggered when user clicks 'Load Failsafe Rules' button.
        """
        msg = QtGui.QMessageBox(self)
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setText(i18n("Failsafe firewall rules will be loaded."))
        msg.setInformativeText(i18n("Do you want to continue?"))
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msg.setDefaultButton(QtGui.QMessageBox.No)

        if msg.exec_() != QtGui.QMessageBox.Yes:
            return

        fp = tempfile.NamedTemporaryFile(delete=False)
        name = fp.name
        fp.write(file("/usr/share/ahenk-lider/firewall-failsafe.fwb").read())
        fp.close()

        self.plainTextEdit.setPlainText("")

        fw_name = re.findall('Firewall.*iptables.*name="([a-zA-Z0-9\-_]+)"', file(name).read())[0]

        process = subprocess.Popen(["/usr/bin/fwb_ipt", "-q", "-f", name, "-o", "%s.sh" % name, fw_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.wait() != 0:
            return

        self.rules_xml = file(name).read()
        self.rules_compiled = file(name + ".sh").read()

        self.plainTextEdit.setPlainText(i18n("Failsafe rules were loaded"))

    """
    def __slot_status(self):

            #Triggered when user changes firewall status.

        if self.radioEnable.isChecked():
            icon = wrappers.Icon("secure64", 64)
        else:
            icon = wrappers.Icon("insecure64", 64)

        pixmap = icon.pixmap(64, 64)
        self.pixmapStatus.setPixmap(pixmap)
    """

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Software magement module
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_authentication import Ui_widgetAuthentication

# Helper modules
from lider.helpers import plugins
from lider.helpers import wrappers


class WidgetModule(QtGui.QWidget, Ui_widgetAuthentication, plugins.PluginWidget):
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
        self.connect(self.radioUnix, QtCore.SIGNAL("clicked()"), self.__update_boxes)
        self.connect(self.radioLDAP, QtCore.SIGNAL("clicked()"), self.__update_boxes)
        self.connect(self.radioAD, QtCore.SIGNAL("clicked()"), self.__update_boxes)

        # Reset UI
        self.__update_boxes()


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
        return ["authenticationPolicy"]

    def load_policy(self, policy):
        """
            Main window calls this method when policy is fetched from directory.
            Not required for global widgets.
        """
        # Authentication type
        authenticationType = policy.get("authenticationType", ["unix"])[0]
        if authenticationType == "ldap":
            self.radioLDAP.setChecked(True)
        elif authenticationType == "ad":
            self.radioAD.setChecked(True)
        else:
            self.radioUnix.setChecked(True)
        self.__update_boxes()
        # LDAP Domain & Host
        authenticationDomainLDAP = policy.get("authenticationDomainLDAP", [""])[0]
        authenticationHostLDAP = policy.get("authenticationHostLDAP", [""])[0]
        self.lineLDAPServer.setText(authenticationHostLDAP)
        self.lineLDAPDomain.setText(authenticationDomainLDAP)
        # Active Directory Domain & Host
        authenticationDomainAD = policy.get("authenticationDomainAD", [""])[0]
        authenticationHostAD = policy.get("authenticationHostAD", [""])[0]
        self.lineADServer.setText(authenticationHostAD)
        self.lineADDomain.setText(authenticationDomainAD)

    def dump_policy(self):
        """
            Main window calls this method to get policy generated by UI.
            Not required for global widgets.
        """
        # Authentication type
        authenticationType = "unix"
        if self.radioLDAP.isChecked():
            authenticationType = "ldap"
        elif self.radioAD.isChecked():
            authenticationType = "ad"
        # LDAP Domain & Host
        authenticationDomainLDAP = str(self.lineLDAPDomain.text())
        authenticationHostLDAP = str(self.lineLDAPServer.text())
        # Active Directory Domain & Host
        authenticationDomainAD = str(self.lineADDomain.text())
        authenticationHostAD = str(self.lineADServer.text())
        # New policy
        policy = {
            "authenticationType": [authenticationType],
            "authenticationDomainLDAP": [authenticationDomainLDAP],
            "authenticationHostLDAP": [authenticationHostLDAP],
            "authenticationDomainAD": [authenticationDomainAD],
            "authenticationHostAD": [authenticationHostAD],
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

    def __update_boxes(self):
        """
            Changes visibilities of group boxes according to authentication
            source selection.
        """
        if self.radioUnix.isChecked():
            self.groupLDAP.hide()
            self.labelGroupLDAP.hide()
            self.groupAD.hide()
            self.labelGroupAD.hide()
        elif self.radioLDAP.isChecked():
            self.groupLDAP.show()
            self.labelGroupLDAP.show()
            self.groupAD.hide()
            self.labelGroupAD.hide()
        elif self.radioAD.isChecked():
            self.groupLDAP.hide()
            self.labelGroupLDAP.hide()
            self.groupAD.show()
            self.labelGroupAD.show()

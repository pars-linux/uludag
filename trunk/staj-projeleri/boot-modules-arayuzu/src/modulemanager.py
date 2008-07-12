#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from gui.ui_mainwindow import Ui_moduleManagerDlg


import dbus
from handler import CallHandler

class ModuleManagerDlg(QtGui.QDialog, Ui_moduleManagerDlg):

    def __init__(self,parent=None):

        if not self.setupBusses():
            sys.exit(1)

        QtGui.QDialog.__init__(self,parent) 
        self.setupUi(self)

        # Populate list
        self.populateList()

    def setupBusses(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException:
            KMessageBox.error(self, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def callHandler(self, script, model, method, action):
        ch = CallHandler(script, model, method, action, 0, self.busSys, self.busSes)
        ch.registerError(self.comarError)
        ch.registerDBusError(self.busError)
        ch.registerAuthError(self.busError)
        ch.registerCancel(self.cancelError)
        return ch

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        KMessageBox.sorry(None, message, i18n("Error"))

    def call(self, script, model, method, *args):
        try:
            obj = self.busSys.get_object("tr.org.pardus.comar", "/package/%s" % script)
            iface = dbus.Interface(obj, dbus_interface="tr.org.pardus.comar.%s" % model)
        except dbus.DBusException, exception:
            self.errorDBus(exception)
        try:
            func = getattr(iface, method)
            return func(*args)
        except dbus.DBusException, exception:
            self.error(exception)

    def callSys(self, method, *args):
        try:
            obj = self.busSys.get_object("tr.org.pardus.comar", "/")
            iface = dbus.Interface(obj, dbus_interface="tr.org.pardus.comar")
        except dbus.DBusException, exception:
            self.errorDBus(exception)
            return
        try:
            func = getattr(iface, method)
            return func(*args)
        except dbus.DBusException, exception:
            self.error(exception)

    def busError(self, exception):
        KMessageBox.error(self, str(exception), i18n("D-Bus Error"))
        self.setupBusses()

    def comarError(self, exception):
        if "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(self, message, i18n("Error"))
        else:
            KMessageBox.error(self, str(exception), i18n("COMAR Error"))

    def populateList(self):
        """loadedModules = self.callSys("listLoaded", "Boot.Modules")
        if loadedModules:
            for i,j in loadedModules.iteritems():
                dosya = open("/home/ozirus/Desktop/test.txt","w")
                dosya.write(i+ "-->" + j)
                dosya.close()
        """    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ModuleManagerDlg()
    form.show()
    app.exec_()

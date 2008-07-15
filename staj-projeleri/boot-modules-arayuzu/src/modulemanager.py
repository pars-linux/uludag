#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from gui.ui_mainwindow import Ui_moduleManagerDlg

import dbus
import dbus.mainloop.qt

from handler import * 

class ModuleManagerDlg(QtGui.QDialog, Ui_moduleManagerDlg):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent) 
        self.setupUi(self)

        if not dbus.get_default_main_loop():
            dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)

        if not self.openBus():
            sys.exit(1)

        self.loadedModules=[]
        self.availableModules={}

        #self.connect(self.btnSearch, QtCore.SIGNAL("clicked()"), self.populateList)
        self.populateList()
    
    def callMethod(self, method, action):
        ch = CallHandler("module_init_tools", "Boot.Modules", method,
                         action,
                         self.winId(),
                         self.busSys, self.busSes)
        ch.registerError(self.comarError)
        ch.registerAuthError(self.comarError)
        ch.registerDBusError(self.busError)
        ch.registerCancel(self.cancelError)
        return ch
    
    def callHandler(self, script, model, method, action):
        ch = CallHandler(script, model, method, action, self.winID, self.busSys, self.busSes)
        ch.registerError(self.error)
        ch.registerDBusError(self.errorDBus)
        ch.registerAuthError(self.errorDBus)
        return ch


    def comarError(self, exception):
        if "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            QtGui.QMessageBox.warning(self, i18n("Error"), message)
        else:
            QtGui.QMessageBox.warning(self, i18n("COMAR Error"), str(exception))

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        QtGui.QMessageBox.warning(self, i18n("Error"), message)


    def busError(self, exception):
        QtGui.QMessageBox.warning(self, i18n("Comar Error"), i18n("Cannot connect to the DBus! If it is not running you should start it with the 'service dbus start' command in a root console."))
        sys.exit()

    def openBus(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException:
            QtGui.QMessageBox.warning(self, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def populateList(self):
        def handler(modules):
            for key in modules:
                self.loadedModules.append(str(key))

            self.listModules.addItems(self.loadedModules)

        ch = self.callMethod("listLoaded", "tr.org.pardus.comar.boot.modules.get")
        ch.registerDone(handler)
        ch.call()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ModuleManagerDlg()
    form.show()
    app.exec_()

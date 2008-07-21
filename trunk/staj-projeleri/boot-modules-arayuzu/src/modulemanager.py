#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from gui.ui_mainwindow import Ui_moduleManagerDlg
from gui.ui_availablemodules import Ui_availableModulesDlg


import dbus
import dbus.mainloop.qt

from handler import * 

class ComarLink:

    def __init__(self, winId):

        self.winId = winId

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

class AvailableModulesDlg(QtGui.QDialog, Ui_availableModulesDlg):
   
    def __init__(self, comarLink, parent=None) :
        QtGui.QDialog.__init__(self, parent) 
        self.setupUi(self)
        self.comarLink = comarLink
        self.populateAllModules()
        self.connect(self.cmbListType, QtCore.SIGNAL("activated(const QString &)"), self.listViaSelectedType)

        self.connect(self.addBlacklistAction, QtCore.SIGNAL("triggered()"), self.addModuleToBlacklist)
        self.connect(self.removeBlacklistAction, QtCore.SIGNAL("triggered()"), self.removeModuleFromBlacklist)
        self.connect(self.addAutoloadAction, QtCore.SIGNAL("triggered()"), self.addModuleToAutoload)
        self.connect(self.removeAutoloadAction, QtCore.SIGNAL("triggered()"), self.removeModuleFromAutoload)
        self.connect(self.loadAction, QtCore.SIGNAL("triggered()"), self.loadModule)

    def addModuleToBlacklist(self):
        ch = self.comarLink.callMethod("addBlacklist","tr.org.pardus.comar.boot.modules.editblacklist") 
        selectedModule = self.listModules.currentItem()
        ch.call(str(selectedModule.text()))

    def removeModuleFromBlacklist(self): 
        ch = self.comarLink.callMethod("removeBlacklist","tr.org.pardus.comar.boot.modules.editblacklist") 
        selectedModule = self.listModules.currentItem()
        ch.call(str(selectedModule.text()))

    def addModuleToAutoload(self):
        pass

    def removeModuleFromAutoload(self):
        pass

    def loadModule(self):
        ch = self.comarLink.callMethod("unload","tr.org.pardus.comar.boot.modules.editblacklist") 
        selectedModule = self.listModules.currentItem()
        ch.call(str(selectedModule.text()))

    def listViaSelectedType(self, listingType):
        if listingType == "All available":
            self.populateAllModules()
        elif listingType == "Blacklisted":
            self.populateBlacklistedModules()
        elif listingType == "Autoloading":
            self.populateAutoloadingModules()
        else:
            pass

    def populateAllModules(self):

        self.listAllModules.clear()

        def handler(modules):
            self.allModules=[]

            for key in modules:
                self.allModules.append(key)

            colorIndex = 0
            sayac=0
            for i in self.allModules:
                color = (255,230)   # This and colorIndex are used for background changing. One blue, one white, one blue, one white and so on.
                item = QtGui.QListWidgetItem(i)
                item.setBackgroundColor(QtGui.QColor(color[colorIndex], color[colorIndex], 255))
                self.listAllModules.addItem(item)

                if colorIndex == 0:
                    colorIndex = 1
                elif colorIndex == 1:
                    colorIndex = 0

        ch = self.comarLink.callMethod("listAvailable","tr.org.pardus.comar.boot.modules.get") 
        ch.registerDone(handler)
        ch.call()
    
    def populateAutoloadingModules(self):

        self.listAllModules.clear()

        def handler(modules):
            self.allModules=[]

            for key in modules:
                self.allModules.append(key)

            colorIndex = 0
            sayac=0
            for i in self.allModules:
                color = (255,230)  # This and colorIndex are used for background changing. One blue, one white, one blue, one white and so on..
                item = QtGui.QListWidgetItem(i)
                item.setBackgroundColor(QtGui.QColor(color[colorIndex], color[colorIndex], 255))
                self.listAllModules.addItem(item)

                if colorIndex == 0:
                    colorIndex = 1
                elif colorIndex == 1:
                    colorIndex = 0

        ch = self.comarLink.callMethod("listAutoload","tr.org.pardus.comar.boot.modules.get") 
        ch.registerDone(handler)
        ch.call()
    

    def populateBlacklistedModules(self):
        
        self.listAllModules.clear()

        def handler(modules):
            self.allModules=[]

            for key in modules:
                self.allModules.append(key)

            colorIndex = 0
            sayac=0
            for i in self.allModules:
                color = (255,230) # This and colorIndex are used for background changing. One blue, one white, one blue, one white and so on..
                item = QtGui.QListWidgetItem(i)
                item.setBackgroundColor(QtGui.QColor(color[colorIndex], color[colorIndex], 255))
                self.listAllModules.addItem(item)

                if colorIndex == 0:
                    colorIndex = 1
                elif colorIndex == 1:
                    colorIndex = 0

        ch = self.comarLink.callMethod("listBlacklist","tr.org.pardus.comar.boot.modules.get") 
        ch.registerDone(handler)
        ch.call()


class ModuleManagerDlg(QtGui.QDialog, Ui_moduleManagerDlg):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent) 
        self.setupUi(self)

        if not dbus.get_default_main_loop():
            dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)

        self.comarLink = ComarLink(self.winId)

        if not self.comarLink.openBus():
            sys.exit(1)


        # Action connectings
        self.connect(self.unloadAction, QtCore.SIGNAL("triggered()"), self.unloadModule)
        self.connect(self.addblacklistAction, QtCore.SIGNAL("triggered()"), self.addModuleToBlacklist)

        self.populateLoadedModules()

    
    # Slots for actions 
    def unloadModule(self):
        ch = self.comarLink.callMethod("unload","tr.org.pardus.comar.boot.modules.unload")
        selectedModule = self.listModules.currentItem()
        ch.call(str(selectedModule.text()))
    
    def addModuleToBlacklist(self):
        ch = self.comarLink.callMethod("addBlacklist","tr.org.pardus.comar.boot.modules.editblacklist") 
        selectedModule = self.listModules.currentItem()
        ch.call(str(selectedModule.text()))

    def populateLoadedModules(self):

        def handler(modules):
            self.loadedModules=[]

            for key in modules:
                self.loadedModules.append(key)
            
            for i in self.loadedModules:
                item = QtGui.QListWidgetItem(i)
                self.listModules.addItem(item)


        ch = self.comarLink.callMethod("listLoaded", "tr.org.pardus.comar.boot.modules.get")
        ch.registerDone(handler)
        ch.call()

    def on_btnNewModule_pressed(self):
        dialog = AvailableModulesDlg(self.comarLink, self)
        if dialog.exec_():
            pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ModuleManagerDlg()
    form.show()
    app.exec_()

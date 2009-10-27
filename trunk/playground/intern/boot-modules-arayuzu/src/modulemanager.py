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

import gettext
__trans = gettext.translation('bootmodulesgui', fallback=True)
_ = __trans.ugettext


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
            message = _("You are not authorized for this operation.")
            QtGui.QMessageBox.warning(None, "Error", message, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
        else:
            QtGui.QMessageBox.warning(None, "COMAR Error", str(exception), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)

    def cancelError(self):
        message = _("You are not authorized for this operation.")
        QtGui.QMessageBox.warning(None, "Error", message, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)


    def busError(self, exception):
        QtGui.QMessageBox.warning(None, _("Comar Error"), _("Cannot connect to the DBus! If it is not running you should start it with the 'service dbus start' command in a root console."), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
        sys.exit()

    def openBus(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException:
            QtGui.QMessageBox.warning(None, _("Unable to connect to DBus."), _("DBus Error"), QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
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
        self.connect(self.editSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.searchOnList)

    def searchOnList(self, item):
        
        self.listAllModules.clear()

        searchResults = []

        for i in range(len(self.allModules)):
            nextModule=str(self.allModules[i])
            if nextModule.startswith(item):
                searchResults.append(nextModule)

        if len(searchResults) == 0 and self.editSearch.text() == "":
            self.listAllModules.addItems(self.loadedModules)
        elif len(searchResults) == 0:
            pass
        else:
            self.listAllModules.addItems(searchResults)


    def loadModule(self):
        ch = self.comarLink.callMethod("load","tr.org.pardus.comar.boot.modules.load") 
        selectedModule = str(self.listAllModules.currentItem().text())

        ch.call(selectedModule)

    def addModuleToBlacklist(self):
        ch = self.comarLink.callMethod("addBlacklist","tr.org.pardus.comar.boot.modules.editblacklist") 
        selectedModule = str(self.listAllModules.currentItem().text())
        ch.call(selectedModule)

    def removeModuleFromBlacklist(self): 
        ch = self.comarLink.callMethod("removeBlacklist","tr.org.pardus.comar.boot.modules.editblacklist") 
        selectedModule = str(self.listAllModules.currentItem().text())
        ch.call(selectedModule)

    def addModuleToAutoload(self):
        ch = self.comarLink.callMethod("addAutoload","tr.org.pardus.comar.boot.modules.addautoload")
        selectedModule = str(self.listAllModules.currentItem().text())
        ch.call(selectedModule, "2.6") # FIXME:  This kernel version number is hard-coded but should not be

    def removeModuleFromAutoload(self):
        ch = self.comarLink.callMethod("removeAutoload","tr.org.pardus.comar.boot.modules.editautoload")
        selectedModule = str(self.listAllModules.currentItem().text())
        ch.call(selectedModule, "2.6") # FIXME:  This kernel version number is hard-coded but should not be

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
        self.listAllModules.addItem(_("Loading..."))

        def handler(modules):

            self.listAllModules.clear()
            self.allModules=[]

            for key in modules:
                self.allModules.append(key)

            colorIndex = 0
            rowIndex = 1
            for i in self.allModules:
                color = (255,230)   # This and colorIndex are used for background changing. One blue, one white, one blue, one white and so on.
                item = QtGui.QListWidgetItem(i)
                item.setBackgroundColor(QtGui.QColor(color[colorIndex], color[colorIndex], 255))
                self.listAllModules.insertItem(rowIndex, item)
                rowIndex = rowIndex + 1
                if colorIndex == 0:
                    colorIndex = 1
                elif colorIndex == 1:
                    colorIndex = 0

        ch = self.comarLink.callMethod("listAvailable","tr.org.pardus.comar.boot.modules.get") 
        ch.registerDone(handler)
        ch.call()
    
    def populateAutoloadingModules(self):

        self.listAllModules.clear()
        self.listAllModules.addItem(_("Loading..."))

        def handler(modules):
            self.listAllModules.clear()
            self.allModules=[]

            for key in modules:
                self.allModules.append(key)

            colorIndex = 0
            rowIndex = 1
            for i in self.allModules:
                color = (255,230)  # This and colorIndex are used for background changing. One blue, one white, one blue, one white and so on..
                item = QtGui.QListWidgetItem(i)
                item.setBackgroundColor(QtGui.QColor(color[colorIndex], color[colorIndex], 255))
                self.listAllModules.addItem(rowIndex, item)
                rowIndex = rowIndex + 1

                if colorIndex == 0:
                    colorIndex = 1
                elif colorIndex == 1:
                    colorIndex = 0

        ch = self.comarLink.callMethod("listAutoload","tr.org.pardus.comar.boot.modules.get") 
        ch.registerDone(handler)
        ch.call("2.6")

    def populateBlacklistedModules(self):
        
        self.listAllModules.clear()
        self.listAllModules.addItem(_("Loading..."))

        def handler(modules):
            self.listAllModules.clear()
            self.allModules=[]

            for key in modules:
                self.allModules.append(key)

            colorIndex = 0
            self.listAllModules.setCurrentRow(0)
            for i in self.allModules:
                color = (255,230) # This and colorIndex are used for background changing. One blue, one white, one blue, one white and so on..
                item = QtGui.QListWidgetItem(i)
                item.setBackgroundColor(QtGui.QColor(color[colorIndex], color[colorIndex], 255))
                row = self.listAllModules.currentRow()
                self.listAllModules.insertItem(row, item)

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
        self.connect(self.editSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.searchOnList)

        self.populateLoadedModules()

    
    # Slots for actions 
    def unloadModule(self):
        ch = self.comarLink.callMethod("unload","tr.org.pardus.comar.boot.modules.unload")
        selectedModule = str(self.listModules.currentItem().text())

        def handler():
            self.populateLoadedModules()

        ch.registerDone(handler)
        ch.call(selectedModule)

    
    def addModuleToBlacklist(self):
        ch = self.comarLink.callMethod("addBlacklist","tr.org.pardus.comar.boot.modules.editblacklist") 
        selectedModule = str(self.listModules.currentItem().text())
        ch.call(selectedModule)

    def searchOnList(self, item):
        
        self.listModules.clear()

        searchResults = []

        for i in range(len(self.loadedModules)):
            nextModule=str(self.loadedModules[i])
            if nextModule.startswith(item):
                searchResults.append(nextModule)

        if len(searchResults) == 0 and self.editSearch.text() == "":
            self.listModules.addItems(self.loadedModules)
        elif len(searchResults) == 0:
            pass
        else:
            self.listModules.addItems(searchResults)

    def populateLoadedModules(self):

        self.listModules.clear()
        self.listModules.addItem(_("Loading..."))

        def handler(modules):

            self.listModules.clear()
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
        self.connect(dialog.loadAction, QtCore.SIGNAL("triggered()"), self.populateLoadedModules)
        dialog.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ModuleManagerDlg()
    form.show()
    app.exec_()

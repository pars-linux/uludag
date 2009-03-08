#!/usr/bin/python
# -*- coding: utf-8 -*-

# Qt stuff
from PyQt4 import QtCore
from PyQt4 import QtGui

# App specific stuff
from gui.ui_mainwindow import Ui_moduleManagerDlg
from gui.ui_availablemodules import Ui_availableModulesDlg

#System
import comar
import sys

# DBUS-QT
import dbus.mainloop.qt

class AvailableModulesDlg(QtGui.QDialog, Ui_availableModulesDlg):
    
    def __init__(self, comarLinkRef, parent=None):
        QtGui.QDialog.__init__(self, parent) 
        self.setupUi(self)
        self.comarLink = comarLinkRef
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
        selectedModule = str(self.listAllModules.currentItem().text())
        self.comarLink.Boot.Modules["module_init_tools"].load(selectedModule)

    def addModuleToBlacklist(self):
        selectedModule = str(self.listAllModules.currentItem().text())
        self.comarLink.Boot.Modules["module_init_tools"].addBlackList(selectedModule)

    def removeModuleFromBlacklist(self): 
        selectedModule = str(self.listAllModules.currentItem().text())
        self.comarLink.Boot.Modules["module_init_tools"].removeBlackList(selectedModule)

    def addModuleToAutoload(self):
        selectedModule = str(self.listAllModules.currentItem().text())
        self.comarLink.Boot.Modules["module_init_tools"].addAutoload(selectedModule,"2.6") # FIXME: kernel_version shouldn't be hard-coded

    def removeModuleFromAutoload(self):
        selectedModule = str(self.listAllModules.currentItem().text())
        self.comarLink.Boot.Modules["module_init_tools"].removeAutoload(selectedModule, "2.6") # FIXME: kernel_version shouldn't be hard-coded


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
        
        def putToList(package, exception, results):

            if not exception:

                self.listAllModules.clear()
                self.allModules=[]

                for set in results:
                    for module in set:
                        self.allModules.append(module)

                for element in self.allModules:
                    item = QtGui.QListWidgetItem(str(element))
                    self.listAllModules.addItem(item)
        
        self.listAllModules.clear()
        self.listAllModules.addItem("Loading...")

        self.comarLink.Boot.Modules.listAvailable(async = putToList)

    def populateAutoloadingModules(self):
        
        def putToList(package, exception, results):

            if not exception:

                self.listAllModules.clear()
                self.allModules=[]

                for set in results:
                    for module in set:
                        self.allModules.append(module)

                for element in self.allModules:
                    item = QtGui.QListWidgetItem(str(element))
                    self.listAllModules.addItem(item)

        self.listAllModules.clear()
        self.listAllModules.addItem("Loading")
        self.comarLink.Boot.Modules["module_init_tools"].listAutoload("2.6", async=putToList)

    def populateBlacklistedModules(self):

        def putToList(package, exception, results):
            
            if not exception:
                self.listAllModules.clear()
                self.allModules=[]

            for set in results:
                for module in set:
                    self.allModules.append(module)

            for element in self.allModules:
                item = QtGui.QListWidgetItem(str(element))
                self.listAllModules.addItem(item)

        self.listAllModules.clear()
        self.listAllModules.addItem("Loading...")

        self.comarLink.Boot.Modules.listBlacklist(async = putToList)

class ModuleManagerDlg(QtGui.QWidget, Ui_moduleManagerDlg):
#class ModuleManagerDlg(QtGui.QDialog, Ui_moduleManagerDlg):

    def __init__(self, parent=None):

        QtGui.QDialog.__init__(self, parent) 
        self.setupUi(self)

        self.comarLink = comar.Link()

        # Action connectings
        self.connect(self.unloadAction, QtCore.SIGNAL("triggered()"), self.unloadModule)
        self.connect(self.addblacklistAction, QtCore.SIGNAL("triggered()"), self.addModuleToBlacklist)
        self.connect(self.editSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.searchOnList)

        self.populateLoadedModules()


    # Slots for actions 
    def unloadModule(self):

        selectedModule = str(self.listModules.currentItem().text())

        def updateList(package, exception, results):
            self.populateLoadedModules()
        
        self.comarLink.Boot.Modules["module_init_tools"].unload(selectedModule, async=updateList)


        
    def addModuleToBlacklist(self):
        selectedModule = str(self.listModules.currentItem().text())
        self.comarLink.Boot.Modules["module_init_tools"].addBlacklist(selectedModule)

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
    
    def clearList(self):
        self.listModules.clear()
        self.loadedModules = []

    def populateLoadedModules(self):

        def putToList(package, exception, results):

            if not exception:

                self.listModules.clear()
                self.loadedModules = []

                for set in results: #FIXME: Hacky code
                    for module in set:
                        self.loadedModules.append(module)
                
                for element in self.loadedModules:
                    item = QtGui.QListWidgetItem(str(element))
                    self.listModules.addItem(item)
        
        self.listModules.clear()
        self.listModules.addItem("Loading...")

        self.comarLink.Boot.Modules.listLoaded(async = putToList)

    def on_btnNewModule_pressed(self):
        dialog = AvailableModulesDlg(self.comarLink, self)
        self.connect(dialog.loadAction, QtCore.SIGNAL("triggered()"), self.populateLoadedModules)
        dialog.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ModuleManagerDlg()
    form.show()
    app.exec_()

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
        	self.comarLink.Boot.Modules.load(module=selectedModule)

	def addModuleToBlacklist(self):
        	selectedModule = str(self.listAllModules.currentItem().text())
        	self.comarLink.Boot.Modules.addBlackList(module=selectedModule)

    	def removeModuleFromBlacklist(self): 
        	selectedModule = str(self.listAllModules.currentItem().text())
        	self.comarLink.Boot.Modules.removeBlacklist(module=selectedModule)

    	def addModuleToAutoload(self):
        	selectedModule = str(self.listAllModules.currentItem().text())
        	self.comarLink.Boot.Modules.addAutoload(module=selectedModule, kernel_version='2.6') # FIXME: kernel_version shouldn't be hard-coded

	def removeModuleFromAutoload(self):
        	selectedModule = str(self.listAllModules.currentItem().text())
        	self.comarLink.Boot.Modules.removeAutoload(module=selectedModule, kernel_version='2.6') # FIXME: kernel_version shouldn't be hard-coded


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
        	self.listAllModules.addItem("Loading...")
		
        	def handler(modules):

			self.listAllModules.clear()
			self.allModules=[]
	
			for key in modules:
				self.allModules.append(key)
	
			colorIndex = 0
			rowIndex = 1
	
			for i in self.allModules:
				color = (255,230)
				item = QtGui.QListWidgetItem(i)
				item.setBackgroundColor(QtGui.QColor(color[colorIndex], color[colorIndex], 255))
				self.listAllModules.insertItem(rowIndex, item)
				rowIndex = rowIndex + 1
	
				if colorIndex == 0:
					colorIndex = 1
				elif colorIndex == 1:
					colorIndex = 0

		self.comarLink.callMethod("listAvailable","tr.org.pardus.comar.boot.modules.get") 
		ch.registerDone(handler)
		ch.call()
    
	def populateAutoloadingModules(self):

        	self.listAllModules.clear()
        	self.listAllModules.addItem("Loading...")

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
		# FIXME
		ch = self.comarLink.callMethod("listAutoload","tr.org.pardus.comar.boot.modules.get") 
		ch.registerDone(handler)
		ch.call("2.6")

	def populateBlacklistedModules(self):
        
        	self.listAllModules.clear()
        	self.listAllModules.addItem("Loading...")

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

        # FIXME
        	self.comarLink.callMethod("listBlacklist","tr.org.pardus.comar.boot.modules.get") 
        	ch.registerDone(handler)
        	ch.call()

class ModuleManagerDlg(QtGui.QDialog, Ui_moduleManagerDlg):

	def __init__(self, parent=None):

        	QtGui.QDialog.__init__(self, parent) 
        	self.setupUi(self)

        	if not dbus.get_default_main_loop():
            		dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)

        	self.comarLink = comar.Link()

		# Action connectings
		self.connect(self.unloadAction, QtCore.SIGNAL("triggered()"), self.unloadModule)
		self.connect(self.addblacklistAction, QtCore.SIGNAL("triggered()"), self.addModuleToBlacklist)
		self.connect(self.editSearch, QtCore.SIGNAL("textChanged(const QString &)"), self.searchOnList)
	
		self.populateLoadedModules()

    
    	# Slots for actions 
	def unloadModule(self):
        	selectedModule = str(self.listModules.currentItem().text())
        	self.comarLink.Boot.Modules.unload(module=selectedModule)
        
	# FIXME: Handler ilişkisini kur. Bitince listeyi yenileteceğiz.

        	def handler():
            		self.populateLoadedModules()

        	ch.registerDone(handler)
    
	def addModuleToBlacklist(self):
        	selectedModule = str(self.listModules.currentItem().text())
        	self.comarLink.Boot.Modules.addBlacklist(module=selectedModule)

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
	
		def putToList(package, exception, results):
		
			self.listModules.clear()
			self.listModules.addItem("Loading...")
			
			if not exception:
		
					self.listModules.clear()
					self.loadedModules = []
		
					for set in results: #FIXME: Hacky code
						for module in set:
							self.loadedModules.append(module)
				
					for element in self.loadedModules:
						item = QtGui.QListWidgetItem(str(element))
						self.listModules.addItem(item)
							
					
		
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

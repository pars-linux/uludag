# -*- coding: utf-8 -*-
#necessary modules
import os
import sys
from operations import *

#Qt modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#PyKDE4 modules
from PyKDE4.kdeui import *

#KonfigTracker Modules
from monitor import Monitor
from about import *

#KonfigTracker Gui
from ui_mainwindow import Ui_MainWindow

class KonfigTracker(KXmlGuiWindow, Ui_MainWindow):

	def __init__(self,app):
		KXmlGuiWindow.__init__(self)
		
		#Backend Initializations
		self.app = app
		self.InitApplication()
		self.monitor = Monitor(app)
		self.monitor.start()
		
		# UI Initializations
		self.setupUi(self)
		self.setFixedSize(self.width(), self.height())
		self.setMainMenuBar()
		self.connectMainSignals()

		#System Tray Settings
		self.trayItem = KStatusNotifierItem("konfigtracker",self)
		self.trayItem.setStandardActionsEnabled(True)
		self.trayItem.setIconByPixmap(QIcon(":/data/tray.png"))
		self.trayItem.setToolTip(QIcon(":/data/tray.png"), "KonfigTracker", "Snapshot and monitoring tool for kde4 settings")
		
		#update the list for setting up the backupList widget
		self.commitMap = {}
		self.pathMap = {}
                self.slotUpdateView()
		self.treeView.setHeaderLabel("No snapshots selected")

	def InitApplication(self):
		if not os.access(db_path,os.F_OK):
			os.mkdir(db_path)
			createDatabase(db_path)
			performBackup()
		else:
			performBackup()

	def setMainMenuBar(self):
		self.appMenuBar = self.menuBar()
		
		#Adding File Menu
		self.fileMenu = KActionMenu("File", self)
		self.quitAction = KStandardAction.quit(self.app.quit, self.actionCollection())
		self.importAction = KAction("Import Configurations", self)
		self.exportAction = KAction("Export Configurations", self)
		self.exportAction.setEnabled(False)
		self.fileMenu.addAction(self.importAction)
		self.fileMenu.addAction(self.exportAction)
		self.separator1 = self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.quitAction)
		self.appMenuBar.addMenu(self.fileMenu.menu())
		
		#Backup Menu
		self.backupMenu = KActionMenu("Backup", self)
		self.tagSelection = KAction("Tag Selected", self)
		self.tagSelection.setEnabled(False)
		self.initConfig = KAction("Initialize", self)
		self.backupMenu.addAction(self.initConfig)
		self.backupMenu.addAction(self.tagSelection)
		self.appMenuBar.addMenu(self.backupMenu.menu())

		#Restore Menu
		self.restoreMenu = KActionMenu("Restore", self)
		self.restoreSelection = KAction("To Selected Snapshot", self)
		self.restoreSelection.setEnabled(False)
		self.restoreMenu.addAction(self.restoreSelection)
		self.appMenuBar.addMenu(self.restoreMenu.menu())
		
		#Help Menu
		self.helpMenu = KHelpMenu(self, aboutData)
		self.appMenuBar.addMenu(self.helpMenu.menu())

	def connectMainSignals(self):
		#SIGNALS for pushbuttons
		self.connect(self.archiveButton, SIGNAL("clicked(bool)"), self.slotExportDatabase)
		self.connect(self.restoreButton, SIGNAL("clicked(bool)"), self.slotPerformRestore)
		self.connect(self.importButton, SIGNAL("clicked(bool)"), self.slotImportArchive)
		
		#SIGNALS for view items
		self.connect(self.monitor, SIGNAL("backupDone"), self.slotUpdateView)
                self.connect(self.backupList, SIGNAL("itemClicked(QListWidgetItem*)"), self.slotUpdateTreeView)
		self.connect(self.backupList, SIGNAL("itemClicked(QListWidgetItem*)"), self.slotEnableItems)
                self.connect(self.treeView, SIGNAL("itemSelectionChanged()"), self.slotShowLog)

		#SIGNALS for menu items
		self.connect(self.restoreSelection, SIGNAL("triggered(bool)"), self.slotPerformRestore)
		self.connect(self.exportAction, SIGNAL("triggered(bool)"), self.slotExportDatabase)
		self.connect(self.tagSelection, SIGNAL("triggered(bool)"), self.slotTagCommit)

	def slotEnableItems(self):
		self.tagSelection.setEnabled(True)
		self.exportAction.setEnabled(True)
		self.restoreSelection.setEnabled(True)
		self.archiveButton.setEnabled(True)
		self.restoreButton.setEnabled(True)

	def slotImportArchive(self):
		pass

	def slotUpdateTreeView(self):
		#this will update the treeView, which will show the list of files changed.
		#pathMap will be a dictionary as <path,git.Diff>
		selected = self.backupList.selectedItems()
		self.pathMap.clear()
		for i in selected:
			selectedCommit = self.commitMap[str(i.text())]
			self.pathMap = getPathMap(selectedCommit)
			#adding the commitId as toplevel item of treeView
			self.treeView.clear()
			self.treeView.setHeaderLabel("id: " + selectedCommit)
			for j in self.pathMap.keys():
				item = QTreeWidgetItem(self.treeView)
				item.setText(0,j)

	def slotUpdateView(self):
		#update the backupList view
                self.commitMap.clear()
		self.commitMap = getCommitMap()
                backup_list = QStringList()
                for i in self.commitMap:
                	backup_list.append(QString(i))
                #showing the list in view
                self.backupList.clear()
                self.backupList.insertItems(0, backup_list)
                self.backupList.sortItems(Qt.DescendingOrder)

		#showing a message in tray
		self.trayItem.showMessage("KonfigTracker",backup_list.first(),self.trayItem.iconName())
      
        def slotShowLog(self):
                diffLog = QString()
                selected = self.treeView.selectedItems()
                for i in selected:
			selectedDiff = self.pathMap[str(i.text(0))]
			#commitLog = getDiff(selectedDiff)
			diffLog = QString(selectedDiff.diff)
		colorList = diffLog.split('\n')
		self.backupLog.clear()
                # a loop for coloring the text browser
		for i in colorList:
			if i.startsWith('-'):
				self.backupLog.setTextBackgroundColor(Qt.darkRed)
				self.backupLog.setTextColor(Qt.white)
				self.backupLog.append(i)
			elif i.startsWith('+'):
				self.backupLog.setTextBackgroundColor(Qt.darkGreen)
				self.backupLog.append(i)
			else:
				self.backupLog.setTextColor(Qt.black)
				self.backupLog.setTextBackgroundColor(Qt.white)
				self.backupLog.append(i)

	def slotPerformRestore(self):
		selectionList = self.backupList.selectedItems()
		#extract the commit id and call restore function
		for i in selectionList:
			selection = self.commitMap[str(i.text())]
			restore(str(selection))
		self.showRestoreDone()
                    
	def showRestoreDone(self):
		msgBox = QMessageBox()
		msgBox.setWindowTitle("Restore Complete")
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Your configuration files have been restored to selected snapshot.\nPlease restart your session")
		ret = msgBox.exec_()
                
	def slotExportDatabase(self):
		selectionList = self.backupList.selectedItems()
		#show a QFileDialog for saving
		fileName = QFileDialog.getSaveFileName(self,"Save archive", QDir.homePath() + "/untitled.tar.gz", "Archives (*.tar.gz)")
		if not fileName.isEmpty():
			for i in selectionList:
				selection = self.commitMap[str(i.text())]
				exportDatabase(selection,fileName)
	
	def slotTagCommit(self):
		pass

# -*- coding: utf-8 -*-
#necessary modules
import os
from operations import *

#Qt modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#PyKDE4 modules
from PyKDE4.kdeui import *

#KonfigTracker Modules
from monitor import Monitor

#KonfigTracker Gui
from gui.ui_mainwindow import Ui_MainWindow

class KonfigTracker(KXmlGuiWindow, Ui_MainWindow):

	def __init__(self,app):
		KXmlGuiWindow.__init__(self)
		#Backend Initializations
		self.InitApplication()
		self.monitor = Monitor(app)
		self.monitor.start()
		# UI Initializations
		self.setupUi(self)
		self.setFixedSize(self.width(), self.height())
		self.app = app
		self.connectMainSignals()
		#update the list for setting up the backupList widget
		self.commitMap = {}
                self.slotUpdateView()

	def InitApplication(self):
		""" 
		If there exist no database in this path, this function will create
		one, and initialize a git repository there.
		"""
		if not os.access(db_path,os.F_OK):
			os.mkdir(db_path)
			createDatabase(db_path)
			performBackup()
		else:
			performBackup()

	def connectMainSignals(self):
		self.connect(self.archiveButton, SIGNAL("clicked(bool)"), self.slotExportDatabase)
		self.connect(self.restoreButton, SIGNAL("clicked(bool)"), self.slotPerformRestore)
		self.connect(self.monitor, SIGNAL("backupDone"), self.slotUpdateView)
                self.connect(self.backupList, SIGNAL("itemClicked(QListWidgetItem*)"), self.slotShowLog)
                self.connect(self.backupList, SIGNAL("itemSelectionChanged()"), self.slotShowLog)
                self.connect(self.actionAbout_Qt, SIGNAL("triggered(bool)"),self.slotAboutQt)

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
            
        def slotShowLog(self):
                commitLog = QString()
                selected = self.backupList.selectedItems()
                for i in selected:
			selectedCommit = self.commitMap[str(i.text())]
			commitLog = getCommitLog(selectedCommit)
		colorList = commitLog.split('\n')
		self.backupLog.clear()
                # a loop for coloring the text browser
		for i in colorList:
			if i.startsWith('-'):
				self.backupLog.setTextColor(Qt.darkRed)
				self.backupLog.append(i)
			elif i.startsWith('+'):
				self.backupLog.setTextColor(Qt.darkGreen)
				self.backupLog.append(i)
			else:
				self.backupLog.setTextColor(Qt.black)
				self.backupLog.append(i)

	def slotPerformRestore(self):
		selectionList = self.backupList.selectedItems()
		if selectionList == []:
			self.showError()
		else:
			#extract the commit id and call restore function
			for i in selectionList:
				selection = self.commitMap[str(i.text())]
				restore(str(selection))
			self.showRestoreDone()
                    
	def showError(self):
		msgBox = QMessageBox()
		msgBox.setWindowTitle("KonfigTracker Error")
		msgBox.setIcon(QMessageBox.Critical)
		msgBox.setText("Please select a snapshot from the list!")
		ret = msgBox.exec_()
                
	def showRestoreDone(self):
		msgBox = QMessageBox()
		msgBox.setWindowTitle("Restore Complete")
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Your configuration files have been restored to selected backup.\nPlease restart your session")
		ret = msgBox.exec_()
                
	def slotAboutQt(self):
		about = QMessageBox.aboutQt(self)
                
	def slotExportDatabase(self):
		selectionList = self.backupList.selectedItems()
		if selectionList == []:
			self.showError()
		else:
			#show a QFileDialog for saving
			fileName = QFileDialog.getSaveFileName(self,"Save archive", QDir.homePath() + "/untitled.tar.gz", "Archives (*.tar.gz)")
			for i in selectionList:
				selection = self.commitMap[str(i.text())]
				exportDatabase(selection,fileName)
	
	def slotTagCommit(self):
		selectionList = self.backupList.selectedItems()
		if selectionList == []:
			self.showError()
		else:
			pass

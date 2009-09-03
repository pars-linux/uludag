# -*- coding: utf-8 -*-

# Author: Renan Cakirerk <pardus@cakirerk.org>

from PyQt4 import QtCore, QtGui
import sys,os
from subprocess import Popen, PIPE, STDOUT, call
from time import time
from PyQt4.QtCore import *

fileSystems = {"Extended 4":"ext4", 
			   "Extended 3":"ext3",
			   "Extended 2":"ext2",
			   "FAT 16/32":"vfat",
			   "NTFS":"ntfs",
			   "XFS":"xfs"}

class Ui_MainWindow(object):
	
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(270, 278)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
		MainWindow.setSizePolicy(sizePolicy)
		MainWindow.setMinimumSize(QtCore.QSize(270, 278))
		MainWindow.setMaximumSize(QtCore.QSize(270, 278))
		MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
		MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setEnabled(True)
		self.centralwidget.setObjectName("centralwidget")
		self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
		self.verticalLayout.setObjectName("verticalLayout")
		self.grpBoxDeviceName = QtGui.QGroupBox(self.centralwidget)
		self.grpBoxDeviceName.setMinimumSize(QtCore.QSize(0, 150))
		self.grpBoxDeviceName.setMaximumSize(QtCore.QSize(16777215, 150))
		font = QtGui.QFont()
		font.setWeight(75)
		font.setBold(True)
		self.grpBoxDeviceName.setFont(font)
		self.grpBoxDeviceName.setObjectName("grpBoxDeviceName")
		self.verticalLayoutWidget = QtGui.QWidget(self.grpBoxDeviceName)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 25, 241, 106))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
		self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.lbl_fileSystem = QtGui.QLabel(self.verticalLayoutWidget)
		font = QtGui.QFont()
		font.setWeight(50)
		font.setBold(False)
		self.lbl_fileSystem.setFont(font)
		self.lbl_fileSystem.setObjectName("lbl_fileSystem")
		self.verticalLayout_2.addWidget(self.lbl_fileSystem)
		self.cmb_fileSystem = QtGui.QComboBox(self.verticalLayoutWidget)
		font = QtGui.QFont()
		font.setWeight(50)
		font.setBold(False)
		self.cmb_fileSystem.setFont(font)
		self.cmb_fileSystem.setObjectName("cmb_fileSystem")
		self.verticalLayout_2.addWidget(self.cmb_fileSystem)
		self.lbl_volumeLabel = QtGui.QLabel(self.verticalLayoutWidget)
		font = QtGui.QFont()
		font.setWeight(50)
		font.setBold(False)
		self.lbl_volumeLabel.setFont(font)
		self.lbl_volumeLabel.setObjectName("lbl_volumeLabel")
		self.verticalLayout_2.addWidget(self.lbl_volumeLabel)
		self.txt_volumeLabel = QtGui.QLineEdit(self.verticalLayoutWidget)
		self.txt_volumeLabel.setMinimumSize(QtCore.QSize(0, 25))
		font = QtGui.QFont()
		font.setWeight(50)
		font.setBold(False)
		self.txt_volumeLabel.setFont(font)
		self.txt_volumeLabel.setObjectName("txt_volumeLabel")
		self.verticalLayout_2.addWidget(self.txt_volumeLabel)
		self.verticalLayout.addWidget(self.grpBoxDeviceName)
		

		self.lbl_progress = QtGui.QLabel(self.centralwidget)
		font = QtGui.QFont()
		font.setWeight(50)
		font.setBold(False)
		self.lbl_progress.setFont(font)
		
		self.lbl_progress.setMaximumSize(QtCore.QSize(16777215, 20))
		self.lbl_progress.setAlignment(QtCore.Qt.AlignCenter)
		self.lbl_progress.setObjectName("lbl_progress")
		self.verticalLayout.addWidget(self.lbl_progress)
		
		self.progressBar = QtGui.QProgressBar(self.centralwidget)
		self.progressBar.setMinimumSize(QtCore.QSize(0, 0))
		self.progressBar.setMaximumSize(QtCore.QSize(16777215, 20))
		self.progressBar.setAutoFillBackground(False)
		self.progressBar.setMaximum(1)
		self.progressBar.setProperty("value", QtCore.QVariant(55973))
		self.progressBar.setTextVisible(False)
		self.progressBar.setOrientation(QtCore.Qt.Horizontal)
		self.progressBar.setInvertedAppearance(False)
		self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
		self.progressBar.setObjectName("progressBar")
		self.verticalLayout.addWidget(self.progressBar)
		spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		self.verticalLayout.addItem(spacerItem)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem1)
		self.btn_format = QtGui.QPushButton(self.centralwidget)
		self.btn_format.setObjectName("btn_format")
		self.horizontalLayout.addWidget(self.btn_format)
		self.btn_cancel = QtGui.QPushButton(self.centralwidget)
		self.btn_cancel.setObjectName("btn_cancel")
		self.horizontalLayout.addWidget(self.btn_cancel)
		self.verticalLayout.addLayout(self.horizontalLayout)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 270, 23))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)

		self.retranslateUi(MainWindow)
		QtCore.QObject.connect(self.btn_format, QtCore.SIGNAL("clicked()"), quickFormat.start)
		QtCore.QObject.connect(self.btn_cancel, QtCore.SIGNAL("clicked()"), MainWindow.close)
		QtCore.QObject.connect(quickFormat,SIGNAL("formatStarted()"),formatStarted)
		QtCore.QObject.connect(quickFormat,SIGNAL("formatSuccessful()"),formatSuccessful)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Disk Formatting Utility", None, QtGui.QApplication.UnicodeUTF8))
		self.grpBoxDeviceName.setTitle(QtGui.QApplication.translate("MainWindow", "Kingston USB 2.0 4GB", None, QtGui.QApplication.UnicodeUTF8))
		self.lbl_fileSystem.setText(QtGui.QApplication.translate("MainWindow", "File System", None, QtGui.QApplication.UnicodeUTF8))
		self.lbl_volumeLabel.setText(QtGui.QApplication.translate("MainWindow", "Volume Label", None, QtGui.QApplication.UnicodeUTF8))
		self.lbl_progress.setText(QtGui.QApplication.translate("MainWindow", "Progress", None, QtGui.QApplication.UnicodeUTF8))
		self.btn_format.setText(QtGui.QApplication.translate("MainWindow", "Format", None, QtGui.QApplication.UnicodeUTF8))
		self.btn_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


class QuickFormat(QtCore.QThread):

	def __init__(self):
		QtCore.QThread.__init__(self)


	def addFileSystems(self):
		
		# temporary space for file systems
		tempFileSystems = []
		
		# get file systems
		for fs in fileSystems:
			tempFileSystems.append(fs)
		
		# sort file systems	
		tempFileSystems.sort()
		sortedFileSystems = tempFileSystems
		
		# display file systems in combobox
		for fs in sortedFileSystems:
			ui.cmb_fileSystem.addItem(fs)	
			
			
	def formatDisk(self): 
  
		self.fs = fileSystems[str(ui.cmb_fileSystem.itemText(ui.cmb_fileSystem.currentIndex()))]
		if self.fs == "ntfs":
			option = "-Q"
		else:
			option = ""
		
		volumeLabel = str(ui.txt_volumeLabel.text())
#		volumeLabel = "Deneme"
		if volumeLabel=="":
			volumeLabel="MyDisk"

		if self.fs == "vfat":
			proc = Popen("mkfs -t " + self.fs + " -n " + volumeLabel + " " + option + " " + deviceName, shell=True, stdout=PIPE,)
		
		else:
			proc = Popen("mkfs -t " + self.fs + " -L " + volumeLabel + " " + option + " " + deviceName, shell=True, stdout=PIPE,)
			
		print proc.communicate()[0]
	
	def run(self):
		self.emit(SIGNAL("formatStarted()"))
		self.formatDisk()
		self.emit(SIGNAL("formatSuccessful()"))




def formatStarted():
	ui.btn_format.setDisabled(True)
	ui.progressBar.setMaximum(0)
	ui.lbl_progress.setText("Please wait while formatting...") 

def formatSuccessful():
	ui.progressBar.setMaximum(1)
	ui.progressBar.setValue(1)
	ui.lbl_progress.setText("Format Completed Successfully")
	ui.btn_format.setDisabled(False)
	ui.btn_cancel.setText("Close")
	
def formatFailed():
	ui.progressBar.setMaximum(1)
	ui.progressBar.setValue(0)
	ui.lbl_progress.setText("Device is in use. Unmount it and try again.") 


if __name__ == "__main__":
	
	
	deviceName = "/dev/sdb1" #sys.argv[1]
	
	quickFormat = QuickFormat()

	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	
	quickFormat.addFileSystems()
	ui.txt_volumeLabel.setText("MyDisk")
	
	
	MainWindow.show()
	
	sys.exit(app.exec_())
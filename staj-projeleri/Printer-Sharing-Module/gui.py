# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Sal Ağu 19 09:50:20 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!
from qt import *
from kdeui import *
from kdecore import *
from pardus import netutils
import sys
import printerwidget2, events, cupsdialog, helpdialog


class MainWindow(QMainWindow):
	def __init__(self,parent = None,name = None,fl = 0):
		QMainWindow.__init__(self,parent,name,fl)
		self.statusBar()
		
		if not name:
			self.setName("MainWindow")
		
		#Essential properties
		self.Events = events.Events()
		self.printerName = ""
		self.activePrinter = QPushButton(None)
		
		self.setCentralWidget(QWidget(self,"qt_central_widget"))
		
		self.propertiesbox = QGroupBox(self.centralWidget(),"propertiesbox")
		self.propertiesbox.setGeometry(QRect(10,280,590,130))
		
		self.namel = QLabel(self.propertiesbox,"namel")
		self.namel.setGeometry(QRect(10,20,110,21))
		
		self.statusl = QLabel(self.propertiesbox,"statusl")
		self.statusl.setGeometry(QRect(10,42,110,21))
		
		self.locationl = QLabel(self.propertiesbox,"locationl")
		self.locationl.setGeometry(QRect(10,64,110,21))
		
		self.uril = QLabel(self.propertiesbox,"uril")
		self.uril.setGeometry(QRect(10,86,110,21))
		
		self.namel2 = QLabel(self.propertiesbox,"namel2")
		self.namel2.setGeometry(QRect(130,20,440,21))
		
		self.statusl2 = QLabel(self.propertiesbox,"statusl2")
		self.statusl2.setGeometry(QRect(130,42,440,21))
		
		self.locationl2 = QLabel(self.propertiesbox,"locationl2")
		self.locationl2.setGeometry(QRect(130,64,440,21))
		
		self.uril2 = QLabel(self.propertiesbox,"uril2")
		self.uril2.setGeometry(QRect(130,86,440,21))
		
		self.printerframe = printerwidget2.PrinterWidget2(self.centralWidget(),"printerframe",self)
		self.printerframe.setGeometry(QRect(10,10,390,260))
		self.printerframe.setFrameShape(QFrame.StyledPanel)
		self.printerframe.setFrameShadow(QFrame.Raised)
		
		self.helpbutton = KPushButton(self.centralWidget(),"helpbutton")
		#self.helpbutton = QPushButton(self.centralWidget(),"helpbutton")
		self.helpbutton.setGeometry(QRect(540,250,60,21))
		self.helpbutton.setFocusPolicy(QPushButton.NoFocus)
		
		self.advanceButton = QPushButton(self.centralWidget(),"advanceButton")
		self.advanceButton.setGeometry(QRect(410,240,110,30))
		self.advanceButton.setFocusPolicy(QPushButton.NoFocus)
		
		self.sharebutton = QPushButton(self.centralWidget(),"sharebutton")
		self.sharebutton.setGeometry(QRect(430,15,150,40))
		self.sharebutton.setFocusPolicy(QPushButton.NoFocus)
		
		self.windowsbox = QGroupBox(self.centralWidget(),"windowsbox")
		self.windowsbox.setGeometry(QRect(410,60,190,170))
		
		self.iplabel = QLabel(self.windowsbox,"iplabel")
		self.iplabel.setGeometry(QRect(10,110,150,21))
		
		self.customedit = QLineEdit(self.windowsbox,"customedit")
		self.customedit.setGeometry(QRect(10,131,150,30))
		self.customedit.setEnabled(False)
		
		self.allowbox = QCheckBox(self.windowsbox,"allowbox")
		self.allowbox.setGeometry(QRect(10,26,170,20))
		self.allowbox.setFocusPolicy(QCheckBox.NoFocus)
		
		self.allowcombo = QComboBox(0,self.windowsbox,"allowcombo")
		self.allowcombo.setGeometry(QRect(10,70,151,30))
		self.allowcombo.setFocusPolicy(QComboBox.NoFocus)
		
		self.allowlabel = QLabel(self.windowsbox,"allowlabel")
		self.allowlabel.setGeometry(QRect(10,48,170,21))
		
		self.languageChange()
		self.insertItems()
		
		self.resize(QSize(616,442).expandedTo(self.minimumSizeHint()))
		self.clearWState(Qt.WState_Polished)
		
		#Connection adjustments
		self.connect(self.sharebutton,SIGNAL("clicked()"),self.sharefunction)
		self.connect(self.sharebutton,SIGNAL("clicked()"),self.replace)
		self.connect(self.allowcombo, SIGNAL("activated(const QString&)"),self.adjustedit)
		self.connect(self.advanceButton, SIGNAL("clicked()"), self.advanceFunction)
		self.connect(self.helpbutton, SIGNAL("clicked()"),self.helpDialog)
		
	def loadProperties(self,name=None,status=None,location=None,uri=None):
		if name==None:
			name = ""
		if status==None:
			status = ""
		if location ==None:
			location = ""
		if uri==None:
			uri = ""
		self.namel2.setText(name)
		self.statusl2.setText(status)
		self.locationl2.setText(location)
		self.uril2.setText(uri)
		
		if status == "shared":
			self.sharebutton.setText("Remove\nShare")
		else:
			self.sharebutton.setText("Share")
			
	def updateHostLabel(self):
		if self.sambabutton.isChecked():
			self.hostedit.setEnabled(True)
		else:
			self.hostedit.setEnabled(False)
		
	def sharefunction(self):
		self.Events.shareCups(self.sharebutton.text(),self.printerName,self)
		
	def setPrinter(self, name, printer):
		self.printerName = name
		self.activePrinter = printer
		
	def advanceFunction(self):
		dialog = cupsdialog.cupsDialog(self)
		dialog.exec_loop()
		
	def helpDialog(self):
		dialog = helpdialog.HelpDialog(self)
		dialog.exec_loop()
	
	def replace(self):
		if self.sender().text()=="Share":
			self.sender().setText("Remove\nShare")
			self.statusl2.setText("shared")
			self.printerframe.setPrinterShared(self.printerName,True,self.Events.getShared())
		else:
			self.sender().setText("Share")
			self.statusl2.setText("not shared")
			self.printerframe.setPrinterShared(self.printerName,False,self.Events.getShared())
		
			
	def refreshPrinterStatus(self, shared):
		self.printerframe.refreshPrinterStatus(shared=="1")

	def adjustedit(self):
		x = int(self.allowcombo.currentText()[0])
		customtext = ""
		if x>2:
			customtext = self.interfacelist[x-2].getAddress()[0]
			sp = customtext.split(".")
			customtext = sp[0] + "." + sp[1] + "." + sp[2] + ".*"
		else:
			customtext = "...*"
		
		self.customedit.setText(customtext)
		
		if self.allowcombo.currentText()[0] == "2":
			self.customedit.setEnabled(True)
		else:
			self.customedit.setEnabled(False)
			
	def insertItems(self):
		gen = netutils.interfaces()
		self.interfacelist = []
		for p in gen:
			self.interfacelist.append(p)
		
		for i in range(1,len(self.interfacelist)):
			if self.interfacelist[i].name == "eth0":
				self.allowcombo.insertItem(self.__tr("%s. ethernet"%(i+2)))
			elif self.interfacelist[i].name == "wlan":
				self.allowcombo.insertItem(self.__tr("%s. ethernet"%(i+2)))
			else:
				self.allowcombo.insertItem(self.__tr(self.interfacelist[i].name))

	def languageChange(self):
		self.setCaption(self.__tr("Printer Sharing Module"))
		self.propertiesbox.setTitle(self.__tr("Printer Properties"))
		self.namel.setText(self.__tr("<b>Name:</b>"))
		self.statusl.setText(self.__tr("<b>Status:</b>"))
		self.locationl.setText(self.__tr("<b>Location:</b>"))
		self.uril.setText(self.__tr("<b>Device URI:</b>"))
		self.namel2.setText(self.__tr("<b>...</b>"))
		self.statusl2.setText(self.__tr("<b>...</b>"))
		self.locationl2.setText(self.__tr("<b>...</b>"))
		self.uril2.setText(self.__tr("<b>...</b>"))
		self.helpbutton.setText(self.__tr("Help"))
		self.advanceButton.setText(self.__tr("Advance"))
		self.sharebutton.setText(self.__tr("Share"))
		self.windowsbox.setTitle(self.__tr("Windows Clients"))
		self.iplabel.setText(self.__tr("IP number:"))
		self.customedit.setText(self.__tr("...*"))
		self.allowbox.setText(self.__tr("Allow Windows Clients"))
		self.allowcombo.clear()
		self.allowcombo.insertItem(self.__tr("1. All"))
		self.allowcombo.insertItem(self.__tr("2. Custom"))
		self.allowlabel.setText(self.__tr("<u>Allowed Addresses:</u>"))


	def __tr(self,s,c = None):
		return qApp.translate("MainWindow",s,c)
    
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	app.connect(app,SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
	app.exec_loop()

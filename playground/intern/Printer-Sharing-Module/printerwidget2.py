# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printerwidget.ui'
#
# Created: Cum Ağu 15 09:33:03 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!



from qt import *
from kdeui import *
from kdecore import *
import sys, cups
import events



def getIconSet(name, group=KIcon.NoGroup):
    return KGlobal.iconLoader().loadIconSet(name, group)


def getIcon(name, group=KIcon.NoGroup):
    return KGlobal.iconLoader().loadIcon(name, group)

class IconButton(QPushButton):
	def __init__(self, parent, icon_name, uri,shared):
		QPushButton.__init__(self, parent)
		self.setPixmap(getIcon("print_printer"))
		layout = QVBoxLayout()
		
		self.urilabel = QLabel(self)
		self.urilabel.setPaletteBackgroundColor(QColor(225,225,225))
		self.urilabel.setGeometry(QRect(10,10,15,15))
		if uri[0:3] == "usb":
			self.urilabel.setPixmap(getIcon("usb",KIcon.Small))
		elif uri[0:4] == "wlan":
			self.urilabel.setPixmap(getIcon("irkickflash",KIcon.Small))
		elif uri[0:2] == "lp":
			self.urilabel.setPixmap(getIcon("input_devices_settings",KIcon.Small))
			
		self.sharedlabel = QLabel(self)
		self.sharedlabel.setPaletteBackgroundColor(QColor(225,225,225))
		self.sharedlabel.setGeometry(QRect(85,10,15,15))
		if shared:
			self.sharedlabel.setPixmap(getIcon("button_ok",KIcon.Small))
		else:
			self.sharedlabel.setPixmap(getIcon("button_cancel",KIcon.Small))
			
		self.label = QLabel(self,"Error")
		self.label.setGeometry(QRect(5,75,100,18))
		self.setFocusPolicy(QComboBox.NoFocus)
		self.label.setPaletteBackgroundColor(QColor(225,225,225))
		self.resize(110, 100)
		
	def changeStatus(self,shared):
		if shared:
			self.sharedlabel.setPixmap(getIcon("button_ok",KIcon.Small))
		else:
			self.sharedlabel.setPixmap(getIcon("button_cancel",KIcon.Small))
		
	def setText(self,text):
		self.label.setText(text)
	def getText(self):
		return self.label.text()

class PrinterWidget2(QFrame):
	def __init__(self,parent=None,name = None,grand = None):
		QFrame.__init__(self,parent)
		
		self.printer = PrinterWidget(self,name,grand)
		self.printer.setGeometry(0,0,373,256)
		
		self.scrollb = QScrollBar(self,"scrollb")
		self.scrollb.setGeometry(373,2,15,256)
		self.connect(self.scrollb,SIGNAL("valueChanged(int)"),self.set)
		
		self.increment = (self.printer.getHeight() - 130.0)/100
		
		self.resize(380,256)
		self.clearWState(Qt.WState_Polished)
	
	def set(self):
		y = self.scrollb.value()*self.increment
		self.printer.setGeometry(0,-y,373,256+y)
		
	def changePrinterStatus(self,printer, shared):
		self.printer.changePrinterStatus(printer, shared)
	def refreshPrinterStatus(self,shared):
		self.printer.refreshPrinterStatus(shared)
	def setPrinterShared(self,printer, pshared, shared):
		self.printer.setPrinterShared(printer, pshared, shared)
	def refreshPrinters(self):
		self.printer.refreshPrinters()
	def showProperties(self):
		self.printer.showProperties()
	

class PrinterWidget(QFrame):
	def __init__(self,parent = None,name = None,grand = None,fl = 0):
		QFrame.__init__(self,parent)
		self.grand = grand
		
		if not name:
			self.setName("PrinterWidget")
		
		self.setPaletteBackgroundColor(QColor(255,255,255))
		
		#This two lines are to get KIcons
		empty = KCModule(self,"empty")
		empty.setGeometry(-20,-20,5,5)
		
		
		self.p = QPainter(self)
		
		self.languageChange()
		self.Events = events.Events()
		self.connection = self.Events.connection
		
		
		self.buttonlist = []
		
		self.refreshPrinters()
		
		self.resize(QSize(380,self.height()).expandedTo(self.minimumSizeHint()))
		self.clearWState(Qt.WState_Polished)
		
	def changePrinterStatus(self,printer, shared):
		self.buttonlist[self.buttonlist.index(printer)].changeStatus(shared)
		
		
	def refreshPrinterStatus(self,shared):
		for p in self.buttonlist:
			param = self.printers[p.getText().__str__()]["printer-is-shared"]
			p.changeStatus(param and shared)
	
	def setPrinterShared(self,printer, pshared, shared):
		self.printers[printer]["printer-is-shared"] = pshared
		self.refreshPrinterStatus(shared=="1")
	
	def refreshPrinters(self):
		self.printers = self.connection.getPrinters()
		self.settings = self.connection.adminGetServerSettings()
			
		for printer in self.printers:
			uri = self.printers[printer]["device-uri"]
			shr = self.printers[printer]["printer-is-shared"]
			self.buttonlist.append(IconButton(self,"printer1",uri,shr))
			index = len(self.buttonlist)-1
			self.buttonlist[index].setText(printer)
			if self.settings["_share_printers"] == "0":
				self.buttonlist[index].changeStatus(False)
			self.connect(self.buttonlist[index],SIGNAL("clicked()"),self.showProperties)
		
			
		gridx = 0
		gridy = 0
		SPACE = 10
		for printer in self.buttonlist:
			x = SPACE + gridx*125
			y = SPACE + gridy*125
			printer.setGeometry(QRect(x,y,printer.width(), printer.height()))
			gridx = gridx + 1
			gridy = gridy + gridx/3
			gridx = gridx % 3
		self.h = gridy*125+20
		self.x = gridx
				
	def getHeight(self):
		if len(self.buttonlist)<7:
			return 130
		if self.x==0:
			return self.h -125
		else:
			return self.h
	
	def showProperties(self):
		printers = self.connection.getPrinters()
		printername = self.printers.keys()[self.buttonlist.index(self.sender())]
		
		if printers[printername]["printer-is-shared"]:
			status = "shared"
			self.grand.sharebutton.setText("Remove\nShare")
		else:
			status = "not shared"
			self.grand.sharebutton.setText("Share")
		
		set = self.connection.adminGetServerSettings()
		set["ServerName"] = "localhost"
		self.connection.adminSetServerSettings(set)
		
		self.grand.sharebutton.setEnabled(True)
		self.grand.loadProperties(self.printers[printername]["printer-info"],status,
					self.printers[printername]["printer-location"],
					self.printers[printername]["device-uri"])
		
		self.grand.setPrinter(printername,self.sender())
	
	
	def languageChange(self):
		self.setCaption(self.__tr("Form1"))
	
	
	def __tr(self,s,c = None):
		return qApp.translate("Form1",s,c)
    
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = PrinterWidget()
	win.show()
	app.connect(app,SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
	app.exec_loop()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cupsdialog.ui'
#
# Created: Sal Ağu 19 15:49:47 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
import events

class cupsDialog(QDialog):
	def __init__(self,grand,parent = None,name = None,modal = 0,fl = 0):
		QDialog.__init__(self,parent,name,modal,fl)
		
		if not name:
			self.setName("cupsDialog")
		
		self.Events = events.Events()
		self.grand = grand
		
		self.applybutton = QPushButton(self,"applybutton")
		self.applybutton.setGeometry(QRect(220,220,90,30))
		
		self.cancelbutton = QPushButton(self,"cancelbutton")
		self.cancelbutton.setGeometry(QRect(320,220,90,30))
		
		self.okbutton = QPushButton(self,"okbutton")
		self.okbutton.setGeometry(QRect(120,220,90,30))
		
		self.cupsbox = QGroupBox(self,"cupsbox")
		self.cupsbox.setGeometry(QRect(20,20,400,190))
		
		self.remoteany = QCheckBox(self.cupsbox,"remoteany")
		self.remoteany.setGeometry(QRect(20,20,371,31))
		
		self.shareprinters = QCheckBox(self.cupsbox,"shareprinters")
		self.shareprinters.setGeometry(QRect(20,50,371,31))
		
		self.remoteadmin = QCheckBox(self.cupsbox,"remoteadmin")
		self.remoteadmin.setGeometry(QRect(20,80,371,31))
		
		self.usercancel = QCheckBox(self.cupsbox,"usercancel")
		self.usercancel.setGeometry(QRect(20,110,371,31))
		
		self.debuglog = QCheckBox(self.cupsbox,"debuglog")
		self.debuglog.setGeometry(QRect(20,140,371,31))
		
		self.languageChange()
		self.loadServerSettings()
		
		self.resize(QSize(436,272).expandedTo(self.minimumSizeHint()))
		self.clearWState(Qt.WState_Polished)
		
		self.connect(self.applybutton, SIGNAL("clicked()"), self.applyServerSettings)
		self.connect(self.okbutton, SIGNAL("clicked()"), self.applyServerSettings)
		self.connect(self.okbutton, SIGNAL("clicked()"), self, SLOT("close()"))
		self.connect(self.cancelbutton, SIGNAL("clicked()"), self, SLOT("close()"))
    
    	def applyServerSettings(self):
		rmtad = "0"
		rmtan = "0"
		dbg = "0"
		shr = "0"
		cnc = "0"
		if self.remoteadmin.isChecked():
			rmtad = "1"
		if self.remoteany.isChecked():
			rmtan = "1"
		if self.debuglog.isChecked():
			dbg = "1"
		if self.shareprinters.isChecked():
			shr = "1"
		if self.usercancel.isChecked():
			cnc = "1"
		
		self.Events.applyServerSettings(rmtad,rmtan,dbg,shr,cnc)
		self.grand.refreshPrinterStatus(shr)
		
	def loadServerSettings (self):
		settings = self.Events.serversettings()
		self.remoteadmin.setChecked(settings[0])
		self.remoteany.setChecked(settings[1])
		self.debuglog.setChecked(settings[2])
		self.shareprinters.setChecked(settings[3])
		self.usercancel.setChecked(settings[4])


	def languageChange(self):
		self.setCaption(self.__tr("Form1"))
		self.applybutton.setText(self.__tr("Apply"))
		self.cancelbutton.setText(self.__tr("Cancel"))
		self.okbutton.setText(self.__tr("OK"))
		self.cupsbox.setTitle(self.__tr("CUPS Server Settings"))
		self.remoteany.setText(self.__tr("Show printers shared by other systems"))
		self.shareprinters.setText(self.__tr("Share published printers connected to this system"))
		self.remoteadmin.setText(self.__tr("Allow remote administration"))
		self.usercancel.setText(self.__tr("Allow users to cancel any job (not just their own)"))
		self.debuglog.setText(self.__tr("Save debugging information for troubleshooting"))
		
		
	def __tr(self,s,c = None):
		return qApp.translate("cupsDialog",s,c)
    
        
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = cupsDialog()
	win.show()
	app.connect(app,SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
	app.exec_loop()

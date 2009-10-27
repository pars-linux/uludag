# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mydialog.ui'
#
# Created: Çrş Ağu 20 15:56:09 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
import sys



class HelpDialog(QDialog):
	def __init__(self,parent = None,name = None,modal = 0,fl = 0):
			QDialog.__init__(self,parent,name,modal,fl)
		
			if not name:
				self.setName("Help")
		
			self.setSizeGripEnabled(1)
		
		
			self.ok = QPushButton(self,"ok")
			self.ok.setGeometry(QRect(230,405,91,31))
			
			self.label = QLabel(self,"label")
			self.label.setGeometry(QRect(245,10,250,30))
		
			self.textBrowser = QTextBrowser(self,"textLabel1")
			self.textBrowser.setGeometry(QRect(0,40,531,360))
			self.textBrowser.setPaletteBackgroundColor(QColor(239,239,239))
		
			self.languageChange()
			
			self.connect(self.ok,SIGNAL("clicked()"),self,SLOT("close()"))
		
			self.resize(QSize(531,452).expandedTo(self.minimumSizeHint()))
			self.clearWState(Qt.WState_Polished)
		
		
	def languageChange(self):
			self.setCaption(self.__tr("MyDialog"))
			self.ok.setText(self.__tr("OK"))
			self.label.setText(self.__tr("<b><u>HELP</u></b>"))
			self.textBrowser.setText(open("help_eng").read())
		
		
	def __tr(self,s,c = None):
			return qApp.translate("MyDialog",s,c)
	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = HelpDialog()
	win.show()
	app.connect(app,SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
	app.exec_loop()

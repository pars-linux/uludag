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
			self.textBrowser.setText(self.__tr("<blockquote><b><u>PRINTER SHARING MODULE</u></b>\n"
		"<p>Printer Sharing Module uses Common UNIX Printing System(CUPS) and Samba file sharing system together.\n"
		"This module provides an interface to simplify printer sharing over a local network.</p>\n"
		"<p><b>Utilities:</b><br>\n"
		"This module automatically collects the printers added in your system and shows as buttons on the big white part.\n"
		"This buttons show the name of printer, whether that printer shared or not (top-right of each button) and connection type of printer (top-left of each button)\n"
		"By clicking these buttons you can see the related properties (name, status, location, URI) of that printer at below the interface.</p>\n"
		"<p><b>Sharing:</b><br>\n"
		"After clicking a printer you can share it on local network just by clicking the share button. \n"
		"Using only this share button proviedes you to share printer to linux machines. \n"
		"If you want to share that printer also to windows machines you should choose \"Allow Windows Clients\" button.\n"
		"At \"Windows Clients\" part, you can decide the sharing policy over windows clients. \n"
		"Related to your network connection; you can choose a local network and only share that network.\n"
		"Also, you may allow only one ip for using your printer. Then you should choose \"Custom\" below the \"Allowed Addresses\"\n"
		"Otherwise, you can allow everyone, who can reach your computer, to attain your printer by selecting \"All\" option.</p> \n"
		"<p><b>Advance Settings:</b>\n"
		"If you are well informed about CUPS. You can modify the cups server settings by clicking \"Advance\" button.</p></blockquote>"))
		
		
	def __tr(self,s,c = None):
			return qApp.translate("MyDialog",s,c)
	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = HelpDialog()
	win.show()
	app.connect(app,SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
	app.exec_loop()

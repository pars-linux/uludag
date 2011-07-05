# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rootvesunucuayari.ui'
#
# Created: Thu Jul  3 14:49:52 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys, os
import piksemel

class RootVeSunucuEkrani(QtGui.QWidget):
	
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)
		self.resize(572,605)
		self.setGeometry(QtCore.QRect(0,0,572,582))
		self.label = QtGui.QLabel(self)
		self.label.setGeometry(QtCore.QRect(137,61,281,21))
		self.label.setObjectName("label")
		self.sunucuismi_line = QtGui.QLineEdit(self)
		self.sunucuismi_line.setGeometry(QtCore.QRect(260,235,110,21))
		self.sunucuismi_line.setObjectName("sunucuismi_line")
		self.sunucuismi_label = QtGui.QLabel(self)
		self.sunucuismi_label.setGeometry(QtCore.QRect(172,232,83,22))
		self.sunucuismi_label.setObjectName("sunucuismi_label")
		self.rootsifre2_line = QtGui.QLineEdit(self)
		self.rootsifre2_line.setGeometry(QtCore.QRect(260,201,110,24))
		self.rootsifre2_line.setObjectName("rootsifre2_line")
		self.rootsifre_line = QtGui.QLineEdit(self)
		self.rootsifre_line.setGeometry(QtCore.QRect(260,170,110,24))
		self.rootsifre_line.setObjectName("rootsifre_line")
		self.rootsifre2_label = QtGui.QLabel(self)
		self.rootsifre2_label.setGeometry(QtCore.QRect(117,201,138,22))
		self.rootsifre2_label.setObjectName("rootsifre2_label")
		self.rootsifre_label = QtGui.QLabel(self)
		self.rootsifre_label.setGeometry(QtCore.QRect(169,170,86,22))
		self.rootsifre_label.setObjectName("rootsifre_label")
		self.devamet_buton = QtGui.QPushButton(self)
		self.devamet_buton.setGeometry(QtCore.QRect(470,510,75,28))
		self.devamet_buton.setObjectName("devamet_buton")
		
		self.connect(self.devamet_buton, QtCore.SIGNAL("clicked()"), self.devamet)
		
		self.label.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
	"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
	"p, li { white-space: pre-wrap; }\n"
	"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
	"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">ROOT VE SUNUCU AYARLARI</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.sunucuismi_label.setText(QtGui.QApplication.translate("MainWindow", "SUNUCU İSMİ:", None, QtGui.QApplication.UnicodeUTF8))
		self.rootsifre2_label.setText(QtGui.QApplication.translate("MainWindow", "ROOT ŞİFRESİ(yeniden):", None, QtGui.QApplication.UnicodeUTF8))
		self.rootsifre_label.setText(QtGui.QApplication.translate("MainWindow", "ROOT ŞİFRESİ:", None, QtGui.QApplication.UnicodeUTF8))
		self.devamet_buton.setText(QtGui.QApplication.translate("MainWindow", "Devam Et", None, QtGui.QApplication.UnicodeUTF8))
	
	def devamet(self):
		self.devamedebilir = True
		
		if (self.rootsifre_line.text() == self.rootsifre2_line.text()) and self.rootsifre_line.text() != None:
			self.rootsifre = self.rootsifre_line.text()
		else:
			self.devamedebilir = False
		
		
		if self.sunucuismi_line.text() == None:
			self.devamedebilir = False
		else:
			self.sunucuismi = self.sunucuismi_line.text()
		
		
		if self.devamedebilir:
			
			
			self.close()
			
	
app = QtGui.QApplication(sys.argv)
kulll = RootVeSunucuEkrani()
kulll.show()
app.exec_()	
	

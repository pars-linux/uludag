#   Kullanici ayarlarini kullanici ismi , bagli oldugu gruplar sifre gibi bilgileri alan Kahya ekrani
#   RootveSunucuAyari.py ve genelayarlar.py gibi 2 ekranla birlestirilmesi dusunuldu ama henuz yapilmadi
#   
#



from PyQt4 import QtCore, QtGui

import sys, os
import piksemel
#import rootvesunucuayari

class Ui_MainWindow(QtGui.QWidget):	
	
	def __init__(self, parent = None):
        	QtGui.QWidget.__init__(self, parent)
		self.setGeometry(QtCore.QRect(0,30,519,563))
		self.resize(519,616)
		
		self.label = QtGui.QLabel(self)
		self.label.setGeometry(QtCore.QRect(150,40,201,41))
		self.label.setObjectName("label")
		self.power_check = QtGui.QCheckBox(self)
		self.power_check.setGeometry(QtCore.QRect(300,350,59,23))
		self.power_check.setObjectName("power_check")
		self.pnp_check = QtGui.QCheckBox(self)
		self.pnp_check.setGeometry(QtCore.QRect(170,350,46,23))
		self.pnp_check.setObjectName("pnp_check")
		self.gruplar_label = QtGui.QLabel(self)
		self.gruplar_label.setGeometry(QtCore.QRect(116,259,44,22))
		
		font = QtGui.QFont()
		font.setFamily("Sans Serif")
		font.setWeight(50)
		font.setBold(False)
		self.gruplar_label.setFont(font)
		self.gruplar_label.setObjectName("gruplar_label")
		self.video_check = QtGui.QCheckBox(self)
		self.video_check.setGeometry(QtCore.QRect(299,320,56,23))
		self.video_check.setObjectName("video_check")
		self.sifre_line = QtGui.QLineEdit(self)
		self.sifre_line.setGeometry(QtCore.QRect(170,200,201,24))
		self.sifre_line.setObjectName("sifre_line")
		self.kullaniciekle_buton = QtGui.QPushButton(self)
		self.kullaniciekle_buton.setGeometry(QtCore.QRect(170,420,131,28))
		self.kullaniciekle_buton.setObjectName("kullaniciekle_buton")
		self.wheel_check = QtGui.QCheckBox(self)
		self.wheel_check.setGeometry(QtCore.QRect(300,380,80,23))
		self.wheel_check.setObjectName("wheel_check")
		self.dialout_check = QtGui.QCheckBox(self)
		self.dialout_check.setGeometry(QtCore.QRect(170,290,68,23))
		self.dialout_check.setObjectName("dialout_check")
		self.kullaniciadi_label = QtGui.QLabel(self)
		self.kullaniciadi_label.setGeometry(QtCore.QRect(89,141,71,18))
		
		font = QtGui.QFont()
		font.setFamily("Sans Serif")
		font.setWeight(50)
		font.setBold(False)
		self.kullaniciadi_label.setFont(font)
		self.kullaniciadi_label.setObjectName("kullaniciadi_label")
		self.pnpadmin_check = QtGui.QCheckBox(self)
		self.pnpadmin_check.setGeometry(QtCore.QRect(170,380,84,23))
		self.pnpadmin_check.setObjectName("pnpadmin_check")
		self.sifre_label = QtGui.QLabel(self)
		self.sifre_label.setGeometry(QtCore.QRect(132,197,28,22))
		font = QtGui.QFont()
		font.setFamily("Sans Serif")
		font.setWeight(50)
		font.setBold(False)
		self.sifre_label.setFont(font)
		self.sifre_label.setObjectName("sifre_label")
		self.removable_check = QtGui.QCheckBox(self)
		self.removable_check.setGeometry(QtCore.QRect(299,291,87,23))
		self.removable_check.setObjectName("removable_check")
		self.users_check = QtGui.QCheckBox(self)
		self.users_check.setGeometry(QtCore.QRect(299,262,56,23))
		self.users_check.setObjectName("users_check")
		self.kullanicigercekadi_line = QtGui.QLineEdit(self)
		self.kullanicigercekadi_line.setGeometry(QtCore.QRect(170,170,201,24))
		self.kullanicigercekadi_line.setObjectName("kullanicigercekadi_line")
		self.sifre2_line = QtGui.QLineEdit(self)
		self.sifre2_line.setGeometry(QtCore.QRect(169,229,201,24))
		self.sifre2_line.setObjectName("sifre2_line")
		self.kullanicigercekadi_label = QtGui.QLabel(self)
		self.kullanicigercekadi_label.setGeometry(QtCore.QRect(47,166,113,22))
		font = QtGui.QFont()
		font.setFamily("Sans Serif")
		font.setWeight(50)
		font.setBold(False)
		self.kullanicigercekadi_label.setFont(font)
		self.kullanicigercekadi_label.setObjectName("kullanicigercekadi_label")
		self.sifre2_label = QtGui.QLabel(self)
		self.sifre2_label.setGeometry(QtCore.QRect(80,228,80,22))
		font = QtGui.QFont()
		font.setFamily("Sans Serif")
		font.setWeight(50)
		font.setBold(False)
		self.sifre2_label.setFont(font)
		self.sifre2_label.setObjectName("sifre2_label")
		self.kullanicieklendi_buton = QtGui.QLabel(self)
		self.kullanicieklendi_buton.setGeometry(QtCore.QRect(310,430,201,18))
		self.kullanicieklendi_buton.setObjectName("kullanicieklendi_buton")
		self.kullanicieklendi_buton.hide()	
		self.kullaniciadi_line = QtGui.QLineEdit(self)
		
		self.kullaniciadi_line.setGeometry(QtCore.QRect(170,140,201,24))
		self.kullaniciadi_line.setObjectName("kullaniciadi_line")
		self.audio_check = QtGui.QCheckBox(self)
		self.audio_check.setGeometry(QtCore.QRect(169,259,56,23))
		self.audio_check.setObjectName("audio_check")
		self.disk_check = QtGui.QCheckBox(self)
		self.disk_check.setGeometry(QtCore.QRect(170,320,48,23))
		self.disk_check.setObjectName("disk_check")
		self.devamet_buton = QtGui.QPushButton(self)
		self.devamet_buton.setGeometry(QtCore.QRect(390,500,75,28))
		self.devamet_buton.setObjectName("devamet_buton")
		self.baskakullaniciekle_buton = QtGui.QPushButton(self)
		self.baskakullaniciekle_buton.setGeometry(QtCore.QRect(170,460,131,28))
		self.baskakullaniciekle_buton.setObjectName("baskakullaniciekle_buton")
		self.baskakullaniciekle_buton.hide()	
		#MainWindow.setCentralWidget(self.centralwidget)
		
		self.connect(self.kullaniciekle_buton, QtCore.SIGNAL("clicked()"), self.kullanici_ekle)
		self.connect(self.devamet_buton, QtCore.SIGNAL("clicked()"), self.devamet)
		self.connect(self.baskakullaniciekle_buton, QtCore.SIGNAL("clicked()"), self.baskakullaniciekle)
		
		
		
		
		
		self.label.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
	"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
	"p, li { white-space: pre-wrap; }\n"
	"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
	"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">KULLANICI AYARLARI</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
		self.power_check.setText(QtGui.QApplication.translate("MainWindow", "Power", None, QtGui.QApplication.UnicodeUTF8))
		self.pnp_check.setText(QtGui.QApplication.translate("MainWindow", "Pnp", None, QtGui.QApplication.UnicodeUTF8))
		self.gruplar_label.setText(QtGui.QApplication.translate("MainWindow", "Gruplar:", None, QtGui.QApplication.UnicodeUTF8))
		self.video_check.setText(QtGui.QApplication.translate("MainWindow", "Video", None, QtGui.QApplication.UnicodeUTF8))
		self.kullaniciekle_buton.setText(QtGui.QApplication.translate("MainWindow", "EKLE", None, QtGui.QApplication.UnicodeUTF8))
		self.wheel_check.setText(QtGui.QApplication.translate("MainWindow", "Wheel", None, QtGui.QApplication.UnicodeUTF8))
		self.dialout_check.setText(QtGui.QApplication.translate("MainWindow", "Dial Out", None, QtGui.QApplication.UnicodeUTF8))
		self.kullaniciadi_label.setText(QtGui.QApplication.translate("MainWindow", "Kullanici adi:", None, QtGui.QApplication.UnicodeUTF8))
		self.pnpadmin_check.setText(QtGui.QApplication.translate("MainWindow", "Pnp Admin", None, QtGui.QApplication.UnicodeUTF8))
		self.sifre_label.setText(QtGui.QApplication.translate("MainWindow", "Sifre:", None, QtGui.QApplication.UnicodeUTF8))
		self.removable_check.setText(QtGui.QApplication.translate("MainWindow", "Removable", None, QtGui.QApplication.UnicodeUTF8))
		self.users_check.setText(QtGui.QApplication.translate("MainWindow", "Users", None, QtGui.QApplication.UnicodeUTF8))
		self.kullanicigercekadi_label.setText(QtGui.QApplication.translate("MainWindow", "Kullanici Gercek Adi:", None, QtGui.QApplication.UnicodeUTF8))
		self.sifre2_label.setText(QtGui.QApplication.translate("MainWindow", "Sifre(yeniden):", None, QtGui.QApplication.UnicodeUTF8))
		self.kullanicieklendi_buton.setText(QtGui.QApplication.translate("MainWindow", "Kullanici eklendi!", None, QtGui.QApplication.UnicodeUTF8))
		self.audio_check.setText(QtGui.QApplication.translate("MainWindow", "Audio", None, QtGui.QApplication.UnicodeUTF8))
		self.disk_check.setText(QtGui.QApplication.translate("MainWindow", "Disk", None, QtGui.QApplication.UnicodeUTF8))
		self.devamet_buton.setText(QtGui.QApplication.translate("MainWindow", "Devam Et", None, QtGui.QApplication.UnicodeUTF8))
		self.baskakullaniciekle_buton.setText(QtGui.QApplication.translate("MainWindow", "Baska Kullanici Ekle", None, QtGui.QApplication.UnicodeUTF8))
		
		
		
		
		
		self.userrecords_tag = piksemel.newDocument("yali")
		self.userrecords_tag.insertData("\n\t")
		self.users_tag = self.userrecords_tag.insertTag("users")
		
		
		#self.rootvesunucuekrani = RootVeSunucuEkrani()
		#self.rootvesunucuekrani.hide()
		
		
		
		
	def kullanici_ekle(self):
		
		
		
		self.UserCanBeAdded = True
		self.devamedebilir = False
		
		self.kullaniciadi = self.kullaniciadi_line.text()
		
		if self.kullaniciadi == None:
			self.UserCanBeAdded = False
		
		
		self.kullanicigercekadi = self.kullanicigercekadi_line.text()
		
		
		if self.kullanicigercekadi == None:
			self.UserCanBeAdded = False
				
		self.kullanicisifre=None
		if (self.sifre_line.text() == self.sifre2_line.text()) & (self.sifre_line.text() != None) & (self.sifre2_line.text() != None):
			self.kullanicisifre = self.sifre2_line.text()
		else:
			self.UserCanBeAdded = False
			
		if self.kullanicisifre == None:
			self.UserCanBeAdded = False
		
		self.gruplar = []
		if self.audio_check.checkState() :
			self.gruplar.append("audio")
			
		if self.dialout_check.checkState():
			self.gruplar.append("dial out")	
			
		if self.disk_check.checkState() :
			self.gruplar.append("disk")
			
		if self.pnp_check.checkState() :
			self.gruplar.append("pnp")
			
		if self.pnpadmin_check.checkState() :
			self.gruplar.append("pnp admin")
			
		if self.users_check.checkState() :
			self.gruplar.append("users")
		
		if self.removable_check.checkState() :
			self.gruplar.append("removable")
		
		if self.video_check.checkState() :
			self.gruplar.append("video")
		
		if self.power_check.checkState() :
			self.gruplar.append("power")
	
		if self.wheel_check.checkState() :
			self.gruplar.append("wheel")
		
			
		if self.gruplar == None:
			self.UserCanBeAdded = False
			
		
		
		
			
			
		
			
		if self.UserCanBeAdded :
			self.kullanicieklendi_buton.setText(QtGui.QApplication.translate("MainWindow", "kullanici eklendi", None, QtGui.QApplication.UnicodeUTF8))
			self.kullanicieklendi_buton.show()
			self.baskakullaniciekle_buton.show()
						
			
			self.users_tag.insertData("\n\t\t")
			self.user_tag = self.users_tag.insertTag("user")
			self.user_tag.insertData("\n\t\t\t")
			self.username_tag = self.user_tag.insertTag("username")
			self.username = str(self.kullaniciadi)
			self.realname = str(self.kullanicigercekadi)
			self.password = str(self.kullanicisifre)
		
		
			self.username_tag.insertData(self.username)
			self.user_tag.insertData("\n\t\t\t")
			self.realname_tag = self.user_tag.insertTag("realname")
			self.realname_tag.insertData(self.realname)
			self.user_tag.insertData("\n\t\t\t")
			self.password_tag = self.user_tag.insertTag("password")
			self.password_tag.insertData(self.password)
			self.user_tag.insertData("\n\t\t\t")
			self.groups_tag = self.user_tag.insertTag("groups")
			self.groups_tag.insertData(",".join(self.gruplar))
			
			print self.userrecords_tag.toString()
			self.devamedebilir = True
			
		else:
			self.kullanicieklendi_buton.setText(QtGui.QApplication.translate("MainWindow", "Eksik bilgileri tamamlayin!", None, QtGui.QApplication.UnicodeUTF8))
			self.kullanicieklendi_buton.show()
			self.kullanicieklendi_buton.repaint()
	
	
	def write_to_file(self, doc, name="/tmp/doc.xml"):
		file_object = open(name, "w")
		xml.dom.ext.PrettyPrint(doc, file_object)
		file_object.close()	

	def baskakullaniciekle(self):
		
		self.clearSpaces()
		
	
	def devamet(self):
		self.hide()
		
		self.rootvesunucuekrani.show()
		
		if self.rootvesunucuekrani.devamedebilir:
			self.userrecords_tag.insertData("\n\t")
			self.rootsifre_tag = self.userrecords_tag.insertTag("root_password")
			self.rootsifre_tag.insertData(self.rootvesunucuekrani.rootsifre)
			self.userrecords_tag.insertData("\n\t")
			self.hostname_tag = self.userrecords_tag.insertTag("hostname")
			self.hostname_tag.insertData(self.rootvesunucuekrani.sunucuismi)	
		
	
	
	def clearSpaces(self):
		self.sifre_line.clear()
		self.kullanicigercekadi_line.clear()
		self.sifre2_line.clear()
		self.kullanicieklendi_buton.hide()
		self.baskakullaniciekle_buton.hide()
		self.kullaniciadi_line.clear()

app = QtGui.QApplication(sys.argv)
kulll = Ui_MainWindow()
kulll.show()
app.exec_()	
	

	





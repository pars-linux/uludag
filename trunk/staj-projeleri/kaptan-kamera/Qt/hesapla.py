# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myFirst.ui'
#
# Created: Çrş Eyl 10 11:15:10 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class Makine:
    def __init__(self, ui):
        self.ui = ui

    def topla(self):
        son = int(self.ui.tbBir.text()) + int(self.ui.tbiki.text())
        self.ui.lblSonuc.setText(str(son))

    def cikar(self):
        son = int(self.ui.tbBir.text()) - int(self.ui.tbiki.text())
        self.ui.lblSonuc.setText(str(son))



class Form1(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form1")



        self.btnTopla = QPushButton(self,"btnTopla")
        self.btnTopla.setGeometry(QRect(170,20,161,61))

        self.btnCikar = QPushButton(self,"btnCikar")
        self.btnCikar.setGeometry(QRect(170,100,161,61))

        self.tbBir = QLineEdit(self,"tbBir")
        self.tbBir.setGeometry(QRect(60,20,80,41))

        self.tbiki = QLineEdit(self,"tbiki")
        self.tbiki.setGeometry(QRect(60,70,80,41))

        self.lblSonuc = QLabel(self,"lblSonuc")
        self.lblSonuc.setGeometry(QRect(60,130,80,31))

        self.languageChange()

        self.resize(QSize(403,216).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.makine = Makine(self)

        self.connect(self.btnTopla,SIGNAL("clicked()"),self.makine.topla)
        self.connect(self.btnCikar,SIGNAL("clicked()"),self.makine.cikar)


    def languageChange(self):
        self.setCaption(self.__tr("myFirst"))
        self.btnTopla.setText(self.__tr("Topla"))
        self.btnCikar.setText(self.__tr("Cikar"))
        self.lblSonuc.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    #QObject.connect(a.btnTopla, SIGNAL("clicked()"), a.makine.topla)
    #QObject.connect(a.btnCikar, SIGNAL("clicked()"), a.makine.cikar)
    w = Form1()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mtFirst.ui'
#
# Created: Çrş Eyl 10 10:43:57 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class Form1(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form1")



        self.tbGiris = QLineEdit(self,"tbGiris")
        self.tbGiris.setGeometry(QRect(50,40,330,41))

        self.lblOut = QLabel(self,"lblOut")
        self.lblOut.setGeometry(QRect(50,120,141,31))

        self.btnOk = QPushButton(self,"btnOk")
        self.btnOk.setGeometry(QRect(220,100,161,61))

        self.languageChange()

        self.resize(QSize(403,216).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("myFirst"))
        self.lblOut.setText(QString.null)
        self.btnOk.setText(self.__tr("OK"))


    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Form1()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()

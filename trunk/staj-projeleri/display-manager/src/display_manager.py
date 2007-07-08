# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'display_manager.ui'
#
# Created: Paz Tem 8 15:33:53 2007
#      by: The PyQt User Interface Compiler (pyuic) 3-snapshot-20070613
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class formMain(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("formMain")



        self.editTest = QLineEdit(self,"editTest")
        self.editTest.setGeometry(QRect(80,10,180,21))

        self.pushTest = QPushButton(self,"pushTest")
        self.pushTest.setGeometry(QRect(10,10,61,21))

        self.pushHelp = QPushButton(self,"pushHelp")
        self.pushHelp.setGeometry(QRect(10,40,61,21))

        self.languageChange()

        self.resize(QSize(371,257).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Form"))
        self.pushTest.setText(i18n("test"))
        self.pushHelp.setText(i18n("help"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profileDialog.ui'
#
# Created: Cum Haz 29 14:00:06 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class profileDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form1")


        Form1Layout = QGridLayout(self,1,1,11,6,"Form1Layout")

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.textLabel1 = QLabel(self,"textLabel1")
        layout3.addWidget(self.textLabel1)

        self.lineEdit2 = QLineEdit(self,"lineEdit2")
        layout3.addWidget(self.lineEdit2)

        Form1Layout.addLayout(layout3,0,0)

        self.buttonGroup2 = QButtonGroup(self,"buttonGroup2")
        self.buttonGroup2.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup2.layout().setSpacing(6)
        self.buttonGroup2.layout().setMargin(11)
        buttonGroup2Layout = QGridLayout(self.buttonGroup2.layout())
        buttonGroup2Layout.setAlignment(Qt.AlignTop)

        layout8 = QVBoxLayout(None,0,6,"layout8")

        self.textLabel5 = QLabel(self.buttonGroup2,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))
        layout8.addWidget(self.textLabel5)

        self.textLabel5_2 = QLabel(self.buttonGroup2,"textLabel5_2")
        self.textLabel5_2.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_2.sizePolicy().hasHeightForWidth()))
        layout8.addWidget(self.textLabel5_2)

        self.textLabel5_3 = QLabel(self.buttonGroup2,"textLabel5_3")
        self.textLabel5_3.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_3.sizePolicy().hasHeightForWidth()))
        layout8.addWidget(self.textLabel5_3)

        self.textLabel5_4 = QLabel(self.buttonGroup2,"textLabel5_4")
        self.textLabel5_4.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_4.sizePolicy().hasHeightForWidth()))
        layout8.addWidget(self.textLabel5_4)

        self.textLabel5_5 = QLabel(self.buttonGroup2,"textLabel5_5")
        self.textLabel5_5.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_5.sizePolicy().hasHeightForWidth()))
        layout8.addWidget(self.textLabel5_5)

        buttonGroup2Layout.addLayout(layout8,3,5)

        layout14 = QVBoxLayout(None,0,6,"layout14")

        self.lineEdit3_6 = QLineEdit(self.buttonGroup2,"lineEdit3_6")
        self.lineEdit3_6.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.lineEdit3_6.sizePolicy().hasHeightForWidth()))
        self.lineEdit3_6.setMaximumSize(QSize(60,32767))
        layout14.addWidget(self.lineEdit3_6)

        self.lineEdit3_3_2 = QLineEdit(self.buttonGroup2,"lineEdit3_3_2")
        self.lineEdit3_3_2.setMaximumSize(QSize(60,32767))
        layout14.addWidget(self.lineEdit3_3_2)

        self.lineEdit3_2_2 = QLineEdit(self.buttonGroup2,"lineEdit3_2_2")
        self.lineEdit3_2_2.setMaximumSize(QSize(60,32767))
        layout14.addWidget(self.lineEdit3_2_2)

        self.lineEdit3_4_2 = QLineEdit(self.buttonGroup2,"lineEdit3_4_2")
        self.lineEdit3_4_2.setMaximumSize(QSize(60,32767))
        layout14.addWidget(self.lineEdit3_4_2)

        self.lineEdit3_5_2 = QLineEdit(self.buttonGroup2,"lineEdit3_5_2")
        self.lineEdit3_5_2.setMaximumSize(QSize(60,32767))
        layout14.addWidget(self.lineEdit3_5_2)

        buttonGroup2Layout.addLayout(layout14,3,6)
        spacer1 = QSpacerItem(40,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addMultiCell(spacer1,3,3,0,1)
        spacer2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addItem(spacer2,2,0)
        spacer2_2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addItem(spacer2_2,5,0)

        self.lineEdit13 = QLineEdit(self.buttonGroup2,"lineEdit13")

        buttonGroup2Layout.addMultiCellWidget(self.lineEdit13,5,5,3,4)

        self.radioButton2 = QRadioButton(self.buttonGroup2,"radioButton2")

        buttonGroup2Layout.addMultiCellWidget(self.radioButton2,1,1,0,6)

        self.radioButton1 = QRadioButton(self.buttonGroup2,"radioButton1")

        buttonGroup2Layout.addMultiCellWidget(self.radioButton1,0,0,0,6)

        self.radioButton3 = QRadioButton(self.buttonGroup2,"radioButton3")

        buttonGroup2Layout.addMultiCellWidget(self.radioButton3,4,4,0,6)

        self.textLabel6 = QLabel(self.buttonGroup2,"textLabel6")

        buttonGroup2Layout.addMultiCellWidget(self.textLabel6,5,5,1,2)

        self.checkBox1 = QCheckBox(self.buttonGroup2,"checkBox1")

        buttonGroup2Layout.addMultiCellWidget(self.checkBox1,2,2,1,6)

        layout5 = QVBoxLayout(None,0,6,"layout5")

        self.checkBox4 = QCheckBox(self.buttonGroup2,"checkBox4")
        self.checkBox4.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.checkBox4.sizePolicy().hasHeightForWidth()))
        layout5.addWidget(self.checkBox4)

        self.checkBox4_2 = QCheckBox(self.buttonGroup2,"checkBox4_2")
        self.checkBox4_2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.checkBox4_2.sizePolicy().hasHeightForWidth()))
        layout5.addWidget(self.checkBox4_2)

        self.checkBox4_3 = QCheckBox(self.buttonGroup2,"checkBox4_3")
        self.checkBox4_3.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.checkBox4_3.sizePolicy().hasHeightForWidth()))
        layout5.addWidget(self.checkBox4_3)

        self.checkBox4_4 = QCheckBox(self.buttonGroup2,"checkBox4_4")
        self.checkBox4_4.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.checkBox4_4.sizePolicy().hasHeightForWidth()))
        layout5.addWidget(self.checkBox4_4)

        self.checkBox4_5 = QCheckBox(self.buttonGroup2,"checkBox4_5")
        self.checkBox4_5.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.checkBox4_5.sizePolicy().hasHeightForWidth()))
        layout5.addWidget(self.checkBox4_5)

        buttonGroup2Layout.addMultiCellLayout(layout5,3,3,2,3)

        layout4 = QVBoxLayout(None,0,6,"layout4")

        self.lineEdit3 = QLineEdit(self.buttonGroup2,"lineEdit3")
        self.lineEdit3.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit3.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.lineEdit3)

        self.lineEdit3_3 = QLineEdit(self.buttonGroup2,"lineEdit3_3")
        self.lineEdit3_3.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit3_3.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.lineEdit3_3)

        self.lineEdit3_2 = QLineEdit(self.buttonGroup2,"lineEdit3_2")
        self.lineEdit3_2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit3_2.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.lineEdit3_2)

        self.lineEdit3_4 = QLineEdit(self.buttonGroup2,"lineEdit3_4")
        self.lineEdit3_4.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit3_4.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.lineEdit3_4)

        self.lineEdit3_5 = QLineEdit(self.buttonGroup2,"lineEdit3_5")
        self.lineEdit3_5.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.lineEdit3_5.sizePolicy().hasHeightForWidth()))
        layout4.addWidget(self.lineEdit3_5)

        buttonGroup2Layout.addLayout(layout4,3,4)

        Form1Layout.addWidget(self.buttonGroup2,1,0)

        self.languageChange()

        self.resize(QSize(485,419).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Proxy Settings"))
        self.textLabel1.setText(i18n("Profile name:"))
        self.buttonGroup2.setTitle(i18n("Options"))
        self.textLabel5.setText(i18n("Port"))
        self.textLabel5_2.setText(i18n("Port"))
        self.textLabel5_3.setText(i18n("Port"))
        self.textLabel5_4.setText(i18n("Port"))
        self.textLabel5_5.setText(i18n("Port"))
        self.radioButton2.setText(i18n("Use proxy server"))
        self.radioButton1.setText(i18n("Direct connection"))
        self.radioButton3.setText(i18n("Automatic settings"))
        self.textLabel6.setText(i18n("URL"))
        self.checkBox1.setText(i18n("Use a general proxy"))
        self.checkBox4.setText(i18n("Http"))
        self.checkBox4_2.setText(i18n("Ftp"))
        self.checkBox4_3.setText(i18n("Gopher"))
        self.checkBox4_4.setText(i18n("SSL"))
        self.checkBox4_5.setText(i18n("SOCKS"))


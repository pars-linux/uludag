# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pakito/gui/pspecWidget/dialogs/historyDialogUI.ui'
#
# Created: Sal Ağu 5 10:45:07 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class HistoryDialogUI(KDialog):
    def __init__(self,parent = None,name = None):
        KDialog.__init__(self,parent,name)

        if not name:
            self.setName("HistoryDialogUI")


        HistoryDialogUILayout = QVBoxLayout(self,11,6,"HistoryDialogUILayout")

        self.groupBox2 = QGroupBox(self,"groupBox2")
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(6)
        self.groupBox2.layout().setMargin(11)
        groupBox2Layout = QGridLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.textLabel12 = QLabel(self.groupBox2,"textLabel12")

        groupBox2Layout.addWidget(self.textLabel12,1,3)
        spacer20 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        groupBox2Layout.addItem(spacer20,1,2)

        self.textLabel7 = QLabel(self.groupBox2,"textLabel7")

        groupBox2Layout.addWidget(self.textLabel7,0,3)

        self.textLabel8 = QLabel(self.groupBox2,"textLabel8")

        groupBox2Layout.addWidget(self.textLabel8,1,0)

        layout22 = QVBoxLayout(None,0,6,"layout22")

        self.textLabel9 = QLabel(self.groupBox2,"textLabel9")
        layout22.addWidget(self.textLabel9)
        spacer29 = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout22.addItem(spacer29)

        groupBox2Layout.addLayout(layout22,2,0)

        self.leVersion = KLineEdit(self.groupBox2,"leVersion")

        groupBox2Layout.addWidget(self.leVersion,1,1)

        self.dwDate = KDateWidget(self.groupBox2,"dwDate")
        self.dwDate.setDate(QDate(2006,1,1))

        groupBox2Layout.addWidget(self.dwDate,0,4)

        self.teComment = KTextEdit(self.groupBox2,"teComment")

        groupBox2Layout.addMultiCellWidget(self.teComment,2,2,1,4)

        self.cbType = KComboBox(0,self.groupBox2,"cbType")

        groupBox2Layout.addWidget(self.cbType,1,4)

        self.textLabel6 = QLabel(self.groupBox2,"textLabel6")

        groupBox2Layout.addWidget(self.textLabel6,0,0)

        self.niRelease = KIntNumInput(self.groupBox2,"niRelease")
        self.niRelease.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.niRelease.sizePolicy().hasHeightForWidth()))
        self.niRelease.setValue(1)
        self.niRelease.setMinValue(1)
        self.niRelease.setMaxValue(1000)

        groupBox2Layout.addWidget(self.niRelease,0,1)
        spacer19 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        groupBox2Layout.addItem(spacer19,0,2)
        HistoryDialogUILayout.addWidget(self.groupBox2)

        self.groupBox3 = QGroupBox(self,"groupBox3")
        self.groupBox3.setColumnLayout(0,Qt.Vertical)
        self.groupBox3.layout().setSpacing(6)
        self.groupBox3.layout().setMargin(11)
        groupBox3Layout = QHBoxLayout(self.groupBox3.layout())
        groupBox3Layout.setAlignment(Qt.AlignTop)

        self.textLabel10 = QLabel(self.groupBox3,"textLabel10")
        groupBox3Layout.addWidget(self.textLabel10)

        self.leName = KLineEdit(self.groupBox3,"leName")
        groupBox3Layout.addWidget(self.leName)
        spacer21 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        groupBox3Layout.addItem(spacer21)

        self.textLabel11 = QLabel(self.groupBox3,"textLabel11")
        groupBox3Layout.addWidget(self.textLabel11)

        self.leEmail = KLineEdit(self.groupBox3,"leEmail")
        groupBox3Layout.addWidget(self.leEmail)
        HistoryDialogUILayout.addWidget(self.groupBox3)
        spacer25 = QSpacerItem(20,10,QSizePolicy.Minimum,QSizePolicy.Fixed)
        HistoryDialogUILayout.addItem(spacer25)

        Layout1 = QHBoxLayout(None,0,6,"Layout1")

        self.btnHelp = QPushButton(self,"btnHelp")
        self.btnHelp.setAutoDefault(1)
        Layout1.addWidget(self.btnHelp)
        Horizontal_Spacing2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)

        self.btnOk = QPushButton(self,"btnOk")
        self.btnOk.setAutoDefault(1)
        self.btnOk.setDefault(1)
        Layout1.addWidget(self.btnOk)

        self.btnCancel = QPushButton(self,"btnCancel")
        self.btnCancel.setAutoDefault(1)
        Layout1.addWidget(self.btnCancel)
        HistoryDialogUILayout.addLayout(Layout1)

        self.languageChange()

        self.resize(QSize(550,421).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.niRelease,self.leVersion)
        self.setTabOrder(self.leVersion,self.cbType)
        self.setTabOrder(self.cbType,self.teComment)
        self.setTabOrder(self.teComment,self.leName)
        self.setTabOrder(self.leName,self.leEmail)
        self.setTabOrder(self.leEmail,self.btnHelp)
        self.setTabOrder(self.btnHelp,self.btnOk)
        self.setTabOrder(self.btnOk,self.btnCancel)


    def languageChange(self):
        self.setCaption(i18n("History"))
        self.groupBox2.setTitle(i18n("Release Info"))
        self.textLabel12.setText(i18n("Type:"))
        self.textLabel7.setText(i18n("Date:"))
        self.textLabel8.setText(i18n("Version:"))
        self.textLabel9.setText(i18n("Comment:"))
        self.cbType.clear()
        self.cbType.insertItem(QString.null)
        self.cbType.insertItem(i18n("bug"))
        self.cbType.insertItem(i18n("security"))
        self.textLabel6.setText(i18n("Release:"))
        self.groupBox3.setTitle(i18n("Updater"))
        self.textLabel10.setText(i18n("Name:"))
        self.textLabel11.setText(i18n("E-mail:"))
        self.btnHelp.setText(i18n("&Help"))
        self.btnHelp.setAccel(QKeySequence(i18n("F1")))
        self.btnOk.setText(i18n("&OK"))
        self.btnOk.setAccel(QKeySequence(QString.null))
        self.btnCancel.setText(i18n("&Cancel"))
        self.btnCancel.setAccel(QKeySequence(QString.null))


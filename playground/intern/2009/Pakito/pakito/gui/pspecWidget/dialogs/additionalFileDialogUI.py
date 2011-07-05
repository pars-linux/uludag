# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pakito/gui/pspecWidget/dialogs/additionalFileDialogUI.ui'
#
# Created: Sal Ağu 5 10:45:07 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class AdditionalFileDialogUI(KDialog):
    def __init__(self,parent = None,name = None):
        KDialog.__init__(self,parent,name)

        if not name:
            self.setName("AdditionalFileDialogUI")


        AdditionalFileDialogUILayout = QGridLayout(self,1,1,11,6,"AdditionalFileDialogUILayout")

        self.textLabel1 = QLabel(self,"textLabel1")

        AdditionalFileDialogUILayout.addWidget(self.textLabel1,0,0)

        self.textLabel2 = QLabel(self,"textLabel2")

        AdditionalFileDialogUILayout.addWidget(self.textLabel2,0,3)

        self.lePermission = KLineEdit(self,"lePermission")

        AdditionalFileDialogUILayout.addWidget(self.lePermission,0,4)

        self.textLabel3 = QLabel(self,"textLabel3")

        AdditionalFileDialogUILayout.addWidget(self.textLabel3,1,0)

        self.leTarget = KLineEdit(self,"leTarget")

        AdditionalFileDialogUILayout.addMultiCellWidget(self.leTarget,1,1,1,4)

        self.textLabel4 = QLabel(self,"textLabel4")

        AdditionalFileDialogUILayout.addWidget(self.textLabel4,2,0)
        spacer24 = QSpacerItem(16,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        AdditionalFileDialogUILayout.addItem(spacer24,0,2)

        layout22 = QHBoxLayout(None,0,6,"layout22")

        self.leFile = KLineEdit(self,"leFile")
        layout22.addWidget(self.leFile)

        self.pbFile = KPushButton(self,"pbFile")
        layout22.addWidget(self.pbFile)

        AdditionalFileDialogUILayout.addMultiCellLayout(layout22,2,2,1,4)
        spacer25 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        AdditionalFileDialogUILayout.addItem(spacer25,3,1)

        self.cbOwner = KComboBox(0,self,"cbOwner")
        self.cbOwner.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.cbOwner.sizePolicy().hasHeightForWidth()))
        self.cbOwner.setEditable(1)

        AdditionalFileDialogUILayout.addWidget(self.cbOwner,0,1)

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

        AdditionalFileDialogUILayout.addMultiCellLayout(Layout1,4,4,0,4)

        self.languageChange()

        self.resize(QSize(427,137).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.cbOwner,self.lePermission)
        self.setTabOrder(self.lePermission,self.leTarget)
        self.setTabOrder(self.leTarget,self.leFile)
        self.setTabOrder(self.leFile,self.pbFile)
        self.setTabOrder(self.pbFile,self.btnHelp)
        self.setTabOrder(self.btnHelp,self.btnOk)
        self.setTabOrder(self.btnOk,self.btnCancel)


    def languageChange(self):
        self.setCaption(i18n("Additional File"))
        self.textLabel1.setText(i18n("Owner:"))
        self.textLabel2.setText(i18n("Permission:"))
        self.textLabel3.setText(i18n("Target:"))
        self.textLabel4.setText(i18n("File:"))
        self.pbFile.setText(QString.null)
        self.cbOwner.clear()
        self.cbOwner.insertItem(QString.null)
        self.cbOwner.insertItem(i18n("root"))
        self.btnHelp.setText(i18n("&Help"))
        self.btnHelp.setAccel(QKeySequence(i18n("F1")))
        self.btnOk.setText(i18n("&OK"))
        self.btnOk.setAccel(QKeySequence(QString.null))
        self.btnCancel.setText(i18n("&Cancel"))
        self.btnCancel.setAccel(QKeySequence(QString.null))


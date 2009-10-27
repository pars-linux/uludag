# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pakito/gui/pspecWidget/dialogs/patchDialogUI.ui'
#
# Created: Sal Ağu 5 10:45:06 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class PatchDialogUI(KDialog):
    def __init__(self,parent = None,name = None):
        KDialog.__init__(self,parent,name)

        if not name:
            self.setName("PatchDialogUI")


        PatchDialogUILayout = QGridLayout(self,1,1,11,6,"PatchDialogUILayout")

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel3.sizePolicy().hasHeightForWidth()))

        PatchDialogUILayout.addWidget(self.textLabel3,1,0)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        PatchDialogUILayout.addWidget(self.textLabel1,0,0)

        self.niLevel = KIntNumInput(self,"niLevel")
        self.niLevel.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.niLevel.sizePolicy().hasHeightForWidth()))
        self.niLevel.setMinValue(0)
        self.niLevel.setMaxValue(20)

        PatchDialogUILayout.addWidget(self.niLevel,0,1)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(QSizePolicy.Maximum,QSizePolicy.Preferred,0,0,self.textLabel2.sizePolicy().hasHeightForWidth()))

        PatchDialogUILayout.addWidget(self.textLabel2,0,2)

        self.cbType = KComboBox(0,self,"cbType")
        self.cbType.setEditable(1)

        PatchDialogUILayout.addWidget(self.cbType,0,3)
        spacer14 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        PatchDialogUILayout.addItem(spacer14,2,2)

        Layout1 = QHBoxLayout(None,0,6,"Layout1")

        self.btnHelp = QPushButton(self,"btnHelp")
        self.btnHelp.setAutoDefault(1)
        Layout1.addWidget(self.btnHelp)
        Horizontal_Spacing2 = QSpacerItem(191,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)

        self.btnOk = QPushButton(self,"btnOk")
        self.btnOk.setAutoDefault(1)
        self.btnOk.setDefault(1)
        Layout1.addWidget(self.btnOk)

        self.btnCancel = QPushButton(self,"btnCancel")
        self.btnCancel.setAutoDefault(1)
        Layout1.addWidget(self.btnCancel)

        PatchDialogUILayout.addMultiCellLayout(Layout1,3,3,0,3)

        layout16 = QHBoxLayout(None,0,6,"layout16")

        self.lePatch = KLineEdit(self,"lePatch")
        layout16.addWidget(self.lePatch)

        self.pbPatch = KPushButton(self,"pbPatch")
        layout16.addWidget(self.pbPatch)

        PatchDialogUILayout.addMultiCellLayout(layout16,1,1,1,3)

        self.languageChange()

        self.resize(QSize(398,123).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.niLevel,self.cbType)
        self.setTabOrder(self.cbType,self.lePatch)
        self.setTabOrder(self.lePatch,self.pbPatch)
        self.setTabOrder(self.pbPatch,self.btnHelp)
        self.setTabOrder(self.btnHelp,self.btnOk)
        self.setTabOrder(self.btnOk,self.btnCancel)


    def languageChange(self):
        self.setCaption(i18n("Patch"))
        self.textLabel3.setText(i18n("Patch:"))
        self.textLabel1.setText(i18n("Level:"))
        self.textLabel2.setText(i18n("Compression Type:"))
        self.cbType.clear()
        self.cbType.insertItem(QString.null)
        self.cbType.insertItem(i18n("bz2"))
        self.cbType.insertItem(i18n("gz"))
        self.cbType.insertItem(i18n("targz"))
        self.cbType.insertItem(i18n("tarbz2"))
        self.cbType.insertItem(i18n("zip"))
        self.cbType.insertItem(i18n("tar"))
        self.cbType.insertItem(i18n("tarlzma"))
        self.btnHelp.setText(i18n("&Help"))
        self.btnHelp.setAccel(QKeySequence(i18n("F1")))
        self.btnOk.setText(i18n("&OK"))
        self.btnOk.setAccel(QKeySequence(QString.null))
        self.btnCancel.setText(i18n("&Cancel"))
        self.btnCancel.setAccel(QKeySequence(QString.null))
        self.pbPatch.setText(QString.null)


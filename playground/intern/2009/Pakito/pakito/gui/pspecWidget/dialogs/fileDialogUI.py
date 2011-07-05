# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pakito/gui/pspecWidget/dialogs/fileDialogUI.ui'
#
# Created: Sal Ağu 5 10:45:06 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class FileDialogUI(KDialog):
    def __init__(self,parent = None,name = None):
        KDialog.__init__(self,parent,name)

        if not name:
            self.setName("FileDialogUI")


        FileDialogUILayout = QVBoxLayout(self,11,6,"FileDialogUILayout")

        layout16 = QHBoxLayout(None,0,6,"layout16")

        self.lblType = QLabel(self,"lblType")
        self.lblType.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.lblType.sizePolicy().hasHeightForWidth()))
        layout16.addWidget(self.lblType)

        self.cbType = KComboBox(0,self,"cbType")
        self.cbType.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.cbType.sizePolicy().hasHeightForWidth()))
        layout16.addWidget(self.cbType)
        spacer15 = QSpacerItem(40,20,QSizePolicy.Minimum,QSizePolicy.Minimum)
        layout16.addItem(spacer15)

        self.chbPermanent = QCheckBox(self,"chbPermanent")
        layout16.addWidget(self.chbPermanent)
        FileDialogUILayout.addLayout(layout16)

        layout15 = QHBoxLayout(None,0,6,"layout15")

        self.lblPath = QLabel(self,"lblPath")
        layout15.addWidget(self.lblPath)

        self.lePath = KLineEdit(self,"lePath")
        layout15.addWidget(self.lePath)
        FileDialogUILayout.addLayout(layout15)
        spacer16 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        FileDialogUILayout.addItem(spacer16)

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
        FileDialogUILayout.addLayout(Layout1)

        self.languageChange()

        self.resize(QSize(460,121).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("File"))
        self.lblType.setText(i18n("Type:"))
        self.cbType.clear()
        self.cbType.insertItem(i18n("executable"))
        self.cbType.insertItem(i18n("library"))
        self.cbType.insertItem(i18n("doc"))
        self.cbType.insertItem(i18n("man"))
        self.cbType.insertItem(i18n("config"))
        self.cbType.insertItem(i18n("header"))
        self.cbType.insertItem(i18n("data"))
        self.cbType.insertItem(i18n("info"))
        self.cbType.insertItem(i18n("localedata"))
        self.chbPermanent.setText(i18n("Permanent?"))
        self.lblPath.setText(i18n("Path:"))
        self.btnHelp.setText(i18n("&Help"))
        self.btnHelp.setAccel(QKeySequence(i18n("F1")))
        self.btnOk.setText(i18n("&OK"))
        self.btnOk.setAccel(QKeySequence(QString.null))
        self.btnCancel.setText(i18n("&Cancel"))
        self.btnCancel.setAccel(QKeySequence(QString.null))


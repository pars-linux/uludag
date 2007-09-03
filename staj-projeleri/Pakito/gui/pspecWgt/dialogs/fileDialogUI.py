# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../../uis/dialogs/fileDialog/fileDialogUI.ui'
#
# Created: Pzt Eyl 3 10:47:28 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *
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
        self.setCaption(self.__tr("File"))
        self.lblType.setText(self.__tr("Type:"))
        self.cbType.clear()
        self.cbType.insertItem(self.__tr("executable"))
        self.cbType.insertItem(self.__tr("library"))
        self.cbType.insertItem(self.__tr("doc"))
        self.cbType.insertItem(self.__tr("man"))
        self.cbType.insertItem(self.__tr("config"))
        self.cbType.insertItem(self.__tr("header"))
        self.cbType.insertItem(self.__tr("data"))
        self.cbType.insertItem(self.__tr("info"))
        self.cbType.insertItem(self.__tr("localedata"))
        self.chbPermanent.setText(self.__tr("Permanent?"))
        self.lblPath.setText(self.__tr("Path:"))
        self.btnHelp.setText(self.__tr("&Help"))
        self.btnHelp.setAccel(QKeySequence(self.__tr("F1")))
        self.btnOk.setText(self.__tr("&OK"))
        self.btnOk.setAccel(QKeySequence(QString.null))
        self.btnCancel.setText(self.__tr("&Cancel"))
        self.btnCancel.setAccel(QKeySequence(QString.null))


    def __tr(self,s,c = None):
        return qApp.translate("FileDialogUI",s,c)

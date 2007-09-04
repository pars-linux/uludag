# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../../uis/dialogs/COMARDialog/comarDialogUI.ui'
#
# Created: Sal Eyl 4 12:07:29 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdeui import *



class COMARDialogUI(KDialog):
    def __init__(self,parent = None,name = None):
        KDialog.__init__(self,parent,name)

        if not name:
            self.setName("COMARDialogUI")


        COMARDialogUILayout = QGridLayout(self,1,1,11,6,"COMARDialogUILayout")

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

        COMARDialogUILayout.addMultiCellLayout(Layout1,3,3,0,1)

        self.textLabel6 = QLabel(self,"textLabel6")

        COMARDialogUILayout.addWidget(self.textLabel6,0,0)

        self.cbProvides = KComboBox(0,self,"cbProvides")
        self.cbProvides.setEditable(1)

        COMARDialogUILayout.addWidget(self.cbProvides,0,1)

        self.textLabel4 = QLabel(self,"textLabel4")

        COMARDialogUILayout.addWidget(self.textLabel4,1,0)

        layout22 = QHBoxLayout(None,0,6,"layout22")

        self.leFile = KLineEdit(self,"leFile")
        layout22.addWidget(self.leFile)

        self.pbFile = KPushButton(self,"pbFile")
        layout22.addWidget(self.pbFile)

        COMARDialogUILayout.addLayout(layout22,1,1)
        spacer70 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        COMARDialogUILayout.addItem(spacer70,2,1)

        self.languageChange()

        self.resize(QSize(438,110).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.cbProvides,self.leFile)
        self.setTabOrder(self.leFile,self.pbFile)
        self.setTabOrder(self.pbFile,self.btnHelp)
        self.setTabOrder(self.btnHelp,self.btnOk)
        self.setTabOrder(self.btnOk,self.btnCancel)


    def languageChange(self):
        self.setCaption(self.__tr("COMAR Script"))
        self.btnHelp.setText(self.__tr("&Help"))
        self.btnHelp.setAccel(QKeySequence(self.__tr("F1")))
        self.btnOk.setText(self.__tr("&OK"))
        self.btnOk.setAccel(QKeySequence(QString.null))
        self.btnCancel.setText(self.__tr("&Cancel"))
        self.btnCancel.setAccel(QKeySequence(QString.null))
        self.textLabel6.setText(self.__tr("Provides:"))
        self.cbProvides.clear()
        self.cbProvides.insertItem(QString.null)
        self.cbProvides.insertItem(self.__tr("System.Package"))
        self.cbProvides.insertItem(self.__tr("System.Service"))
        self.textLabel4.setText(self.__tr("Script:"))
        self.pbFile.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("COMARDialogUI",s,c)

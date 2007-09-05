# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../../uis/dialogs/dependencyDialog/dependencyDialogUI.ui'
#
# Created: Sal Eyl 4 15:38:53 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdeui import *



class DependencyDialogUI(KDialog):
    def __init__(self,parent = None,name = None):
        KDialog.__init__(self,parent,name)

        if not name:
            self.setName("DependencyDialogUI")


        DependencyDialogUILayout = QGridLayout(self,1,1,11,6,"DependencyDialogUILayout")

        self.lblCondition = QLabel(self,"lblCondition")

        DependencyDialogUILayout.addWidget(self.lblCondition,0,0)

        self.leDependency = KLineEdit(self,"leDependency")

        DependencyDialogUILayout.addWidget(self.leDependency,1,1)

        self.lblDependency = QLabel(self,"lblDependency")

        DependencyDialogUILayout.addWidget(self.lblDependency,1,0)

        layout20 = QHBoxLayout(None,0,6,"layout20")

        self.cbRelease = KComboBox(0,self,"cbRelease")
        layout20.addWidget(self.cbRelease)

        self.cbToFrom = KComboBox(0,self,"cbToFrom")
        layout20.addWidget(self.cbToFrom)

        self.leCondition = KLineEdit(self,"leCondition")
        layout20.addWidget(self.leCondition)

        DependencyDialogUILayout.addLayout(layout20,0,1)
        spacer22 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        DependencyDialogUILayout.addItem(spacer22,2,0)
        spacer23 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        DependencyDialogUILayout.addItem(spacer23,2,1)

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

        DependencyDialogUILayout.addMultiCellLayout(Layout1,3,3,0,1)

        self.languageChange()

        self.resize(QSize(473,119).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.cbRelease,self.cbToFrom)
        self.setTabOrder(self.cbToFrom,self.leCondition)
        self.setTabOrder(self.leCondition,self.leDependency)
        self.setTabOrder(self.leDependency,self.btnOk)
        self.setTabOrder(self.btnOk,self.btnCancel)
        self.setTabOrder(self.btnCancel,self.btnHelp)


    def languageChange(self):
        self.setCaption(self.__tr("Dependencies"))
        self.lblCondition.setText(self.__tr("Condition:"))
        self.leDependency.setText(QString.null)
        self.lblDependency.setText(self.__tr("Dependency:"))
        self.cbRelease.clear()
        self.cbRelease.insertItem(QString.null)
        self.cbRelease.insertItem(self.__tr("Release"))
        self.cbRelease.insertItem(self.__tr("Version"))
        self.cbToFrom.clear()
        self.cbToFrom.insertItem(QString.null)
        self.cbToFrom.insertItem(self.__tr("="))
        self.cbToFrom.insertItem(self.__tr(">="))
        self.cbToFrom.insertItem(self.__tr("<="))
        self.btnHelp.setText(self.__tr("&Help"))
        self.btnHelp.setAccel(QKeySequence(self.__tr("F1")))
        self.btnOk.setText(self.__tr("&OK"))
        self.btnOk.setAccel(QKeySequence(QString.null))
        self.btnCancel.setText(self.__tr("&Cancel"))
        self.btnCancel.setAccel(QKeySequence(QString.null))


    def __tr(self,s,c = None):
        return qApp.translate("DependencyDialogUI",s,c)

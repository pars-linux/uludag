# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../../uis/dialogs/summaryDialog/summaryDialogUI.ui'
#
# Created: Paz Eyl 2 17:53:54 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdeui import *



class SummaryDialogUI(KDialog):
    def __init__(self,parent = None,name = None):
        KDialog.__init__(self,parent,name)

        if not name:
            self.setName("SummaryDialogUI")

        self.setSizeGripEnabled(1)
        self.setModal(1)

        SummaryDialogUILayout = QVBoxLayout(self,11,6,"SummaryDialogUILayout")

        self.tbLanguage = QToolBox(self,"tbLanguage")
        self.tbLanguage.setCurrentIndex(0)
        SummaryDialogUILayout.addWidget(self.tbLanguage)

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
        Layout1.addWidget(self.btnCancel)
        SummaryDialogUILayout.addLayout(Layout1)

        self.languageChange()

        self.resize(QSize(502,454).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Summaries and Descriptions"))
        self.btnHelp.setText(self.__tr("&Help"))
        self.btnHelp.setAccel(QKeySequence(self.__tr("F1")))
        self.btnOk.setText(self.__tr("&OK"))
        self.btnCancel.setText(self.__tr("&Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("SummaryDialogUI",s,c)

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pakito/gui/pspecWidget/dialogs/summaryDialogUI.ui'
#
# Created: Sal Ağu 5 10:45:06 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
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
        self.setCaption(i18n("Summaries and Descriptions"))
        self.btnHelp.setText(i18n("&Help"))
        self.btnHelp.setAccel(QKeySequence(i18n("F1")))
        self.btnOk.setText(i18n("&OK"))
        self.btnCancel.setText(i18n("&Cancel"))


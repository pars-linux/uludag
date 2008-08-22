# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pakito/gui/pspecWidget/dialogs/summaryWidgetUI.ui'
#
# Created: Sal Ağu 5 10:45:06 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class SummaryWidgetUI(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("summaryWidgetUI")


        summaryWidgetUILayout = QHBoxLayout(self,11,6,"summaryWidgetUILayout")

        layout4 = QGridLayout(None,1,1,0,6,"layout4")

        self.leSummary = KLineEdit(self,"leSummary")

        layout4.addWidget(self.leSummary,1,1)

        self.lblLanguage = QLabel(self,"lblLanguage")

        layout4.addWidget(self.lblLanguage,0,0)

        layout3_3 = QVBoxLayout(None,0,6,"layout3_3")

        self.lblDescription = QLabel(self,"lblDescription")
        layout3_3.addWidget(self.lblDescription)
        spacer2_3 = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout3_3.addItem(spacer2_3)

        layout4.addLayout(layout3_3,2,0)

        self.teDescription = KTextEdit(self,"teDescription")

        layout4.addWidget(self.teDescription,2,1)

        self.lblSummary = QLabel(self,"lblSummary")

        layout4.addWidget(self.lblSummary,1,0)

        self.leLanguage = KLineEdit(self,"leLanguage")

        layout4.addWidget(self.leLanguage,0,1)
        summaryWidgetUILayout.addLayout(layout4)

        self.languageChange()

        self.resize(QSize(675,343).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.leLanguage,self.leSummary)
        self.setTabOrder(self.leSummary,self.teDescription)


    def languageChange(self):
        self.setCaption(i18n("Form1"))
        self.lblLanguage.setText(i18n("Language:"))
        self.lblDescription.setText(i18n("Description:"))
        self.lblSummary.setText(i18n("Summary:"))


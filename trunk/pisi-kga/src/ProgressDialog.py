# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProgressDialog.ui'
#
# Created: Cum Eyl 30 14:36:55 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.15
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class ProgressDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ProgressDialog")

        self.setMinimumSize(QSize(460,100))
        self.setMaximumSize(QSize(460,100))
        self.setModal(1)


        LayoutWidget = QWidget(self,"layout2")
        LayoutWidget.setGeometry(QRect(20,10,420,70))
        layout2 = QVBoxLayout(LayoutWidget,11,6,"layout2")

        self.progressLabel = QLabel(LayoutWidget,"progressLabel")
        layout2.addWidget(self.progressLabel)
        spacer1 = QSpacerItem(20,21,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout2.addItem(spacer1)

        self.progressBar = QProgressBar(LayoutWidget,"progressBar")
        layout2.addWidget(self.progressBar)

        self.languageChange()

        self.resize(QSize(460,100).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Progress"))
        self.progressLabel.setText(i18n("PiSi hazırlanıyor ..."))


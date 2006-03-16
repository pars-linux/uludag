# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProgressDialog.ui'
#
# Created: Prş Mar 16 17:28:11 2006
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20060126
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

        self.setModal(1)

        ProgressDialogLayout = QGridLayout(self,1,1,11,6,"ProgressDialogLayout")

        self.progressBar = QProgressBar(self,"progressBar")

        ProgressDialogLayout.addWidget(self.progressBar,4,1)

        self.animeLabel = QLabel(self,"animeLabel")
        self.animeLabel.setMinimumSize(QSize(100,135))
        self.animeLabel.setScaledContents(1)

        ProgressDialogLayout.addMultiCellWidget(self.animeLabel,0,4,0,0)

        self.sizeLabel = QLabel(self,"sizeLabel")

        ProgressDialogLayout.addWidget(self.sizeLabel,3,1)

        self.speedLabel = QLabel(self,"speedLabel")

        ProgressDialogLayout.addWidget(self.speedLabel,2,1)

        self.currentOperationLabel = QLabel(self,"currentOperationLabel")

        ProgressDialogLayout.addWidget(self.currentOperationLabel,1,1)
        spacer1 = QSpacerItem(20,41,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ProgressDialogLayout.addItem(spacer1,0,1)

        self.languageChange()

        self.resize(QSize(488,167).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Progress"))
        self.animeLabel.setText(QString.null)
        self.sizeLabel.setText(i18n("<b>Downloaded/Total:</b> Unknown"))
        self.speedLabel.setText(i18n("<b>Speed:</b> Unknown"))
        self.currentOperationLabel.setText(i18n("<h3>Preparing PiSi...</h3>"))


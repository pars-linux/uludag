# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Progress.ui'
#
# Created: Prş May 22 01:02:04 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class progressForm(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("progressForm")


        progressFormLayout = QGridLayout(self,1,1,11,6,"progressFormLayout")

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer1 = QSpacerItem(351,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer1)

        self.cancelPushButton = QPushButton(self,"cancelPushButton")
        layout1.addWidget(self.cancelPushButton)

        progressFormLayout.addMultiCellLayout(layout1,3,3,0,1)

        self.progressBar = QProgressBar(self,"progressBar")

        progressFormLayout.addMultiCellWidget(self.progressBar,2,2,0,1)

        self.bigTextLabel = QLabel(self,"bigTextLabel")
        self.bigTextLabel.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.bigTextLabel.sizePolicy().hasHeightForWidth()))

        progressFormLayout.addWidget(self.bigTextLabel,0,1)

        self.progressTextLabel = QLabel(self,"progressTextLabel")
        self.progressTextLabel.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.progressTextLabel.sizePolicy().hasHeightForWidth()))

        progressFormLayout.addWidget(self.progressTextLabel,1,1)

        self.animeLabel = QLabel(self,"animeLabel")

        progressFormLayout.addMultiCellWidget(self.animeLabel,0,1,0,0)

        self.languageChange()

        self.resize(QSize(629,205).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Progress Dialog"))
        self.cancelPushButton.setText(self.__tr("Cancel"))
        self.bigTextLabel.setText(self.__tr("<h2><b>Preparing PISI</b></h2>"))
        self.progressTextLabel.setText(self.__tr("Taking a snapshot of system"))
        self.animeLabel.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("progressForm",s,c)

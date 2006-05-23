# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RepoDialog.ui'
#
# Created: Prş Nis 20 12:13:54 2006
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20060126
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class RepoDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("RepoDialog")


        RepoDialogLayout = QGridLayout(self,1,1,11,6,"RepoDialogLayout")

        layout4 = QVBoxLayout(None,0,6,"layout4")

        self.textLabel1 = QLabel(self,"textLabel1")
        layout4.addWidget(self.textLabel1)

        self.repoName = KLineEdit(self,"repoName")
        layout4.addWidget(self.repoName)

        self.textLabel2 = QLabel(self,"textLabel2")
        layout4.addWidget(self.textLabel2)

        self.repoAddress = KLineEdit(self,"repoAddress")
        layout4.addWidget(self.repoAddress)

        RepoDialogLayout.addLayout(layout4,0,0)

        layout3 = QHBoxLayout(None,0,6,"layout3")
        spacer5 = QSpacerItem(174,16,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout3.addItem(spacer5)

        self.okButton = KPushButton(self,"okButton")
        self.okButton.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.okButton.sizePolicy().hasHeightForWidth()))
        layout3.addWidget(self.okButton)

        self.cancelButton = KPushButton(self,"cancelButton")
        self.cancelButton.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.cancelButton.sizePolicy().hasHeightForWidth()))
        layout3.addWidget(self.cancelButton)

        RepoDialogLayout.addLayout(layout3,1,0)

        self.languageChange()

        self.resize(QSize(323,143).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("clicked()"),self.close)

        self.textLabel1.setBuddy(self.repoName)
        self.textLabel2.setBuddy(self.repoAddress)


    def languageChange(self):
        self.setCaption(i18n("Repository Dialog"))
        self.textLabel1.setText(i18n("Repository &Name"))
        QToolTip.add(self.textLabel1,i18n("Name of the repository, e.g <b>pardus-devel</b>"))
        self.textLabel2.setText(i18n("Repository &Address"))
        QToolTip.add(self.textLabel2,i18n("Adress of the repository, e.g <b>http://foo.bar.com/pisi-index.xml</b>"))
        self.okButton.setText(i18n("&Ok"))
        self.cancelButton.setText(i18n("&Cancel"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pakito/gui/optionsDialogUI.ui'
#
# Created: Sal Ağu 5 10:45:07 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class OptionsDialogUI(KDialog):
    def __init__(self,parent = None,name = None):
        KDialog.__init__(self,parent,name)

        if not name:
            self.setName("OptionsDialogUI")


        OptionsDialogUILayout = QGridLayout(self,1,1,11,6,"OptionsDialogUILayout")

        self.gbPackager = QGroupBox(self,"gbPackager")
        self.gbPackager.setColumnLayout(0,Qt.Vertical)
        self.gbPackager.layout().setSpacing(6)
        self.gbPackager.layout().setMargin(11)
        gbPackagerLayout = QGridLayout(self.gbPackager.layout())
        gbPackagerLayout.setAlignment(Qt.AlignTop)

        self.textLabel1 = QLabel(self.gbPackager,"textLabel1")

        gbPackagerLayout.addWidget(self.textLabel1,0,0)

        self.textLabel2 = QLabel(self.gbPackager,"textLabel2")

        gbPackagerLayout.addWidget(self.textLabel2,1,0)

        self.leEmail = KLineEdit(self.gbPackager,"leEmail")

        gbPackagerLayout.addWidget(self.leEmail,1,1)

        self.leName = KLineEdit(self.gbPackager,"leName")

        gbPackagerLayout.addWidget(self.leName,0,1)

        OptionsDialogUILayout.addWidget(self.gbPackager,0,0)

        Layout1 = QHBoxLayout(None,0,6,"Layout1")

        self.pbHelp = QPushButton(self,"pbHelp")
        self.pbHelp.setAutoDefault(1)
        Layout1.addWidget(self.pbHelp)
        Horizontal_Spacing2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)

        self.pbOk = QPushButton(self,"pbOk")
        self.pbOk.setAutoDefault(1)
        self.pbOk.setDefault(1)
        Layout1.addWidget(self.pbOk)

        self.pbCancel = QPushButton(self,"pbCancel")
        self.pbCancel.setAutoDefault(1)
        Layout1.addWidget(self.pbCancel)

        OptionsDialogUILayout.addLayout(Layout1,2,0)
        spacer3 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        OptionsDialogUILayout.addItem(spacer3,1,0)

        self.languageChange()

        self.resize(QSize(450,156).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.leName,self.leEmail)
        self.setTabOrder(self.leEmail,self.pbOk)
        self.setTabOrder(self.pbOk,self.pbCancel)
        self.setTabOrder(self.pbCancel,self.pbHelp)


    def languageChange(self):
        self.setCaption(i18n("Options"))
        self.gbPackager.setTitle(i18n("Packager Information"))
        self.textLabel1.setText(i18n("Name:"))
        self.textLabel2.setText(i18n("E-mail:"))
        self.pbHelp.setText(i18n("&Help"))
        self.pbHelp.setAccel(QKeySequence(i18n("F1")))
        self.pbOk.setText(i18n("&OK"))
        self.pbOk.setAccel(QKeySequence(QString.null))
        self.pbCancel.setText(i18n("&Cancel"))
        self.pbCancel.setAccel(QKeySequence(QString.null))


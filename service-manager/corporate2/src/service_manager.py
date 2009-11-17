# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'service_manager.ui'
#
# Created: Sal Kas 17 11:49:47 2009
#      by: The PyQt User Interface Compiler (pyuic) 3.18.1
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class formMain(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("formMain")


        formMainLayout = QGridLayout(self,1,1,11,6,"formMainLayout")

        self.frame3 = QFrame(self,"frame3")
        self.frame3.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.frame3.sizePolicy().hasHeightForWidth()))
        self.frame3.setMinimumSize(QSize(400,0))
        self.frame3.setMaximumSize(QSize(32767,200))
        self.frame3.setFrameShape(QFrame.StyledPanel)
        self.frame3.setFrameShadow(QFrame.Raised)
        frame3Layout = QGridLayout(self.frame3,1,1,11,6,"frame3Layout")

        self.buttonGroup2 = QButtonGroup(self.frame3,"buttonGroup2")
        self.buttonGroup2.setMaximumSize(QSize(180,32767))
        self.buttonGroup2.setFrameShape(QButtonGroup.NoFrame)
        self.buttonGroup2.setFrameShadow(QButtonGroup.Plain)
        self.buttonGroup2.setAlignment(QButtonGroup.AlignVCenter)
        self.buttonGroup2.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup2.layout().setSpacing(0)
        self.buttonGroup2.layout().setMargin(0)
        buttonGroup2Layout = QGridLayout(self.buttonGroup2.layout())
        buttonGroup2Layout.setAlignment(Qt.AlignTop)

        self.radioAutoRun = QRadioButton(self.buttonGroup2,"radioAutoRun")

        buttonGroup2Layout.addWidget(self.radioAutoRun,0,0)

        self.radioNoAutoRun = QRadioButton(self.buttonGroup2,"radioNoAutoRun")

        buttonGroup2Layout.addWidget(self.radioNoAutoRun,1,0)

        frame3Layout.addWidget(self.buttonGroup2,0,1)

        self.textInformation = QLabel(self.frame3,"textInformation")
        self.textInformation.setAlignment(QLabel.WordBreak | QLabel.AlignTop | QLabel.AlignLeft)

        frame3Layout.addWidget(self.textInformation,0,0)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.buttonStart = QPushButton(self.frame3,"buttonStart")
        self.buttonStart.setEnabled(1)
        self.buttonStart.setMinimumSize(QSize(32,32))
        self.buttonStart.setMaximumSize(QSize(64,64))
        layout2.addWidget(self.buttonStart)

        self.buttonRestart = QPushButton(self.frame3,"buttonRestart")
        self.buttonRestart.setEnabled(1)
        self.buttonRestart.setMinimumSize(QSize(32,32))
        self.buttonRestart.setMaximumSize(QSize(64,64))
        layout2.addWidget(self.buttonRestart)

        self.buttonStop = QPushButton(self.frame3,"buttonStop")
        self.buttonStop.setEnabled(1)
        self.buttonStop.setMinimumSize(QSize(32,32))
        self.buttonStop.setMaximumSize(QSize(64,64))
        layout2.addWidget(self.buttonStop)

        frame3Layout.addLayout(layout2,0,2)

        formMainLayout.addWidget(self.frame3,2,0)

        self.listServices = KListView(self,"listServices")
        self.listServices.addColumn(i18n("1"))
        self.listServices.addColumn(i18n("Service"))
        self.listServices.addColumn(i18n("Run on Startup"))
        self.listServices.addColumn(i18n("Package"))
        self.listServices.setMinimumSize(QSize(0,150))
        self.listServices.setAllColumnsShowFocus(1)
        self.listServices.setShowSortIndicator(1)

        formMainLayout.addWidget(self.listServices,1,0)

        layout4 = QHBoxLayout(None,0,6,"layout4")

        self.buttonClearSearch = QPushButton(self,"buttonClearSearch")
        self.buttonClearSearch.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.buttonClearSearch.sizePolicy().hasHeightForWidth()))
        self.buttonClearSearch.setMinimumSize(QSize(32,32))
        self.buttonClearSearch.setMaximumSize(QSize(32,32))
        layout4.addWidget(self.buttonClearSearch)

        self.labelSearch = QLabel(self,"labelSearch")
        layout4.addWidget(self.labelSearch)

        self.editSearch = QLineEdit(self,"editSearch")
        layout4.addWidget(self.editSearch)

        self.checkServersOnly = QCheckBox(self,"checkServersOnly")
        self.checkServersOnly.setChecked(1)
        layout4.addWidget(self.checkServersOnly)

        formMainLayout.addLayout(layout4,0,0)

        self.languageChange()

        self.resize(QSize(506,400).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Service Manager"))
        self.buttonGroup2.setTitle(QString.null)
        self.radioAutoRun.setText(i18n("Run on startup."))
        self.radioNoAutoRun.setText(i18n("Don't run on startup."))
        self.textInformation.setText(i18n("Select a service from list."))
        self.buttonStart.setText(QString.null)
        QToolTip.add(self.buttonStart,i18n("Start"))
        self.buttonRestart.setText(QString.null)
        QToolTip.add(self.buttonRestart,i18n("Start"))
        self.buttonStop.setText(QString.null)
        QToolTip.add(self.buttonStop,i18n("Stop"))
        self.listServices.header().setLabel(0,i18n("1"))
        self.listServices.header().setLabel(1,i18n("Service"))
        self.listServices.header().setLabel(2,i18n("Run on Startup"))
        self.listServices.header().setLabel(3,i18n("Package"))
        self.buttonClearSearch.setText(QString.null)
        QToolTip.add(self.buttonClearSearch,i18n("Reset Search"))
        self.labelSearch.setText(i18n("Search:"))
        self.checkServersOnly.setText(i18n("&List servers only."))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historygui.ui'
#
# Created: Cts May 17 02:49:34 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class formMain(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("formMain")

        self.setMinimumSize(QSize(450,400))

        formMainLayout = QGridLayout(self,1,1,11,6,"formMainLayout")

        self.tabWidget = QTabWidget(self,"tabWidget")

        self.tab = QWidget(self.tabWidget,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.snapshotsListView = QListView(self.tab,"snapshotsListView")
        self.snapshotsListView.addColumn(self.__tr("No"))
        self.snapshotsListView.addColumn(self.__tr("Date"))
        self.snapshotsListView.addColumn(self.__tr("Type"))
        self.snapshotsListView.setMinimumSize(QSize(0,150))
        self.snapshotsListView.setAllColumnsShowFocus(1)
        self.snapshotsListView.setShowSortIndicator(1)

        tabLayout.addWidget(self.snapshotsListView,0,0)
        self.tabWidget.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        layout10 = QVBoxLayout(None,0,6,"layout10")

        self.infoTextEdit = QTextEdit(self.tab_2,"infoTextEdit")
        self.infoTextEdit.setEnabled(1)
        self.infoTextEdit.setTextFormat(QTextEdit.RichText)
        layout10.addWidget(self.infoTextEdit)

        self.infoProgressBar = QProgressBar(self.tab_2,"infoProgressBar")
        self.infoProgressBar.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.infoProgressBar.sizePolicy().hasHeightForWidth()))
        self.infoProgressBar.setTotalSteps(0)
        layout10.addWidget(self.infoProgressBar)

        tabLayout_2.addLayout(layout10,0,0)
        self.tabWidget.insertTab(self.tab_2,QString.fromLatin1(""))

        formMainLayout.addMultiCellWidget(self.tabWidget,1,1,0,1)

        self.buttonGroup1 = QButtonGroup(self,"buttonGroup1")
        self.buttonGroup1.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup1.layout().setSpacing(6)
        self.buttonGroup1.layout().setMargin(11)
        buttonGroup1Layout = QGridLayout(self.buttonGroup1.layout())
        buttonGroup1Layout.setAlignment(Qt.AlignTop)

        self.snapshotPushButton = QPushButton(self.buttonGroup1,"snapshotPushButton")

        buttonGroup1Layout.addWidget(self.snapshotPushButton,0,2)
        spacer1 = QSpacerItem(70,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        buttonGroup1Layout.addItem(spacer1,0,1)

        self.helpPushButton = QPushButton(self.buttonGroup1,"helpPushButton")

        buttonGroup1Layout.addWidget(self.helpPushButton,0,0)

        self.restorePushButton = QPushButton(self.buttonGroup1,"restorePushButton")
        self.restorePushButton.setEnabled(0)

        buttonGroup1Layout.addWidget(self.restorePushButton,0,3)

        formMainLayout.addMultiCellWidget(self.buttonGroup1,2,2,0,1)

        self.snapshotsCheckBox = QCheckBox(self,"snapshotsCheckBox")
        self.snapshotsCheckBox.setChecked(1)

        formMainLayout.addWidget(self.snapshotsCheckBox,0,0)
        spacer2 = QSpacerItem(301,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        formMainLayout.addItem(spacer2,0,1)

        self.languageChange()

        self.resize(QSize(503,429).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("History Manager"))
        self.snapshotsListView.header().setLabel(0,self.__tr("No"))
        self.snapshotsListView.header().setLabel(1,self.__tr("Date"))
        self.snapshotsListView.header().setLabel(2,self.__tr("Type"))
        self.tabWidget.changeTab(self.tab,self.__tr("History"))
        self.tabWidget.changeTab(self.tab_2,self.__tr("More Info"))
        self.buttonGroup1.setTitle(QString.null)
        self.snapshotPushButton.setText(self.__tr("New"))
        self.helpPushButton.setText(self.__tr("Help"))
        self.restorePushButton.setText(self.__tr("Restore"))
        self.snapshotsCheckBox.setText(self.__tr("List only Snapshots"))


    def __tr(self,s,c = None):
        return qApp.translate("formMain",s,c)

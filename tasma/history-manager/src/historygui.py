# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historygui.ui'
#
# Created: Prş May 22 17:20:04 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class formMain(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("formMain")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(450,400))

        formMainLayout = QGridLayout(self,1,1,11,6,"formMainLayout")

        layout10 = QHBoxLayout(None,0,6,"layout10")

        self.snapshotsCheckBox = QCheckBox(self,"snapshotsCheckBox")
        self.snapshotsCheckBox.setChecked(1)
        layout10.addWidget(self.snapshotsCheckBox)
        spacer2 = QSpacerItem(301,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout10.addItem(spacer2)

        formMainLayout.addLayout(layout10,0,0)

        self.tabWidget = QTabWidget(self,"tabWidget")

        self.tab = QWidget(self.tabWidget,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.snapshotsListView = QListView(self.tab,"snapshotsListView")
        self.snapshotsListView.addColumn(self.__tr("1"))
        self.snapshotsListView.addColumn(self.__tr("No"))
        self.snapshotsListView.addColumn(self.__tr("Date"))
        self.snapshotsListView.addColumn(self.__tr("Type"))
        self.snapshotsListView.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.snapshotsListView.sizePolicy().hasHeightForWidth()))
        self.snapshotsListView.setMinimumSize(QSize(0,150))
        self.snapshotsListView.setAllColumnsShowFocus(1)
        self.snapshotsListView.setShowSortIndicator(1)

        tabLayout.addWidget(self.snapshotsListView,0,0)
        self.tabWidget.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        self.infoProgressBar = QProgressBar(self.tab_2,"infoProgressBar")
        self.infoProgressBar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.infoProgressBar.sizePolicy().hasHeightForWidth()))
        self.infoProgressBar.setTotalSteps(0)

        tabLayout_2.addWidget(self.infoProgressBar,1,0)

        self.infoTextEdit = QTextEdit(self.tab_2,"infoTextEdit")
        self.infoTextEdit.setEnabled(1)
        self.infoTextEdit.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding,0,0,self.infoTextEdit.sizePolicy().hasHeightForWidth()))
        self.infoTextEdit.setTextFormat(QTextEdit.RichText)

        tabLayout_2.addWidget(self.infoTextEdit,0,0)
        self.tabWidget.insertTab(self.tab_2,QString.fromLatin1(""))

        formMainLayout.addWidget(self.tabWidget,1,0)

        layout11 = QHBoxLayout(None,0,6,"layout11")

        self.helpPushButton = QPushButton(self,"helpPushButton")
        layout11.addWidget(self.helpPushButton)
        spacer1 = QSpacerItem(160,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(spacer1)

        self.snapshotPushButton = QPushButton(self,"snapshotPushButton")
        layout11.addWidget(self.snapshotPushButton)

        self.restorePushButton = QPushButton(self,"restorePushButton")
        self.restorePushButton.setEnabled(0)
        layout11.addWidget(self.restorePushButton)

        formMainLayout.addLayout(layout11,2,0)

        self.languageChange()

        self.resize(QSize(450,403).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("History Manager"))
        self.snapshotsCheckBox.setText(self.__tr("List only Snapshots"))
        self.snapshotsListView.header().setLabel(0,self.__tr("1"))
        self.snapshotsListView.header().setLabel(1,self.__tr("No"))
        self.snapshotsListView.header().setLabel(2,self.__tr("Date"))
        self.snapshotsListView.header().setLabel(3,self.__tr("Type"))
        self.tabWidget.changeTab(self.tab,self.__tr("History"))
        self.tabWidget.changeTab(self.tab_2,self.__tr("More Info"))
        self.helpPushButton.setText(self.__tr("Help"))
        self.snapshotPushButton.setText(self.__tr("New"))
        self.restorePushButton.setText(self.__tr("Restore"))


    def __tr(self,s,c = None):
        return qApp.translate("formMain",s,c)

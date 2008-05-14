# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historygui.ui'
#
# Created: Çrş May 14 16:01:22 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
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

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.sizePolicy().hasHeightForWidth()))

        formMainLayout = QGridLayout(self,1,1,11,6,"formMainLayout")

        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.snapshotsCheckBox = QCheckBox(self,"snapshotsCheckBox")
        self.snapshotsCheckBox.setChecked(1)
        layout7.addWidget(self.snapshotsCheckBox)
        spacer2 = QSpacerItem(231,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7.addItem(spacer2)

        formMainLayout.addLayout(layout7,0,0)

        self.tabWidget = QTabWidget(self,"tabWidget")

        self.tab = QWidget(self.tabWidget,"tab")
        tabLayout = QGridLayout(self.tab,1,1,11,6,"tabLayout")

        self.snapshotsListView = KListView(self.tab,"snapshotsListView")
        self.snapshotsListView.addColumn(self.__tr("No"))
        self.snapshotsListView.addColumn(self.__tr("Date"))
        self.snapshotsListView.addColumn(self.__tr("Type"))

        tabLayout.addWidget(self.snapshotsListView,0,0)
        self.tabWidget.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget,"tab_2")
        tabLayout_2 = QGridLayout(self.tab_2,1,1,11,6,"tabLayout_2")

        self.infoTextEdit = QTextEdit(self.tab_2,"infoTextEdit")

        tabLayout_2.addWidget(self.infoTextEdit,0,0)
        self.tabWidget.insertTab(self.tab_2,QString.fromLatin1(""))

        formMainLayout.addWidget(self.tabWidget,1,0)

        layout3 = QHBoxLayout(None,0,6,"layout3")
        spacer1 = QSpacerItem(190,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout3.addItem(spacer1)

        self.snapshotPushButton = QPushButton(self,"snapshotPushButton")
        layout3.addWidget(self.snapshotPushButton)

        self.deletePushButton = QPushButton(self,"deletePushButton")
        self.deletePushButton.setEnabled(0)
        layout3.addWidget(self.deletePushButton)

        self.restorePushButton = QPushButton(self,"restorePushButton")
        self.restorePushButton.setEnabled(0)
        layout3.addWidget(self.restorePushButton)

        formMainLayout.addLayout(layout3,2,0)

        self.languageChange()

        self.resize(QSize(524,485).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("History Manager"))
        self.snapshotsCheckBox.setText(self.__tr("List only Snapshots"))
        self.snapshotsListView.header().setLabel(0,self.__tr("No"))
        self.snapshotsListView.header().setLabel(1,self.__tr("Date"))
        self.snapshotsListView.header().setLabel(2,self.__tr("Type"))
        self.tabWidget.changeTab(self.tab,self.__tr("History"))
        self.tabWidget.changeTab(self.tab_2,self.__tr("More Info"))
        self.snapshotPushButton.setText(self.__tr("New"))
        self.deletePushButton.setText(self.__tr("Delete"))
        self.restorePushButton.setText(self.__tr("Restore"))


    def __tr(self,s,c = None):
        return qApp.translate("formMain",s,c)

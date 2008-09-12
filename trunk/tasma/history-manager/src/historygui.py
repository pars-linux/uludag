# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historygui.ui'
#
# Created: Cts Eyl 13 01:13:44 2008
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

        layout11 = QHBoxLayout(None,0,6,"layout11")

        self.helpPushButton = QPushButton(self,"helpPushButton")
        self.helpPushButton.setFlat(1)
        layout11.addWidget(self.helpPushButton)
        spacer1 = QSpacerItem(160,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(spacer1)

        self.snapshotPushButton = QPushButton(self,"snapshotPushButton")
        self.snapshotPushButton.setFlat(1)
        layout11.addWidget(self.snapshotPushButton)

        self.restorePushButton = QPushButton(self,"restorePushButton")
        self.restorePushButton.setEnabled(0)
        self.restorePushButton.setFlat(1)
        layout11.addWidget(self.restorePushButton)

        formMainLayout.addMultiCellLayout(layout11,3,3,0,1)

        layout5 = QVBoxLayout(None,0,6,"layout5")

        self.comboBox = QComboBox(0,self,"comboBox")
        self.comboBox.setBackgroundOrigin(QComboBox.ParentOrigin)
        self.comboBox.setMaxCount(10)
        self.comboBox.setDuplicatesEnabled(0)
        layout5.addWidget(self.comboBox)

        self.snapshotsListView = QListView(self,"snapshotsListView")
        self.snapshotsListView.addColumn(self.__tr("1"))
        self.snapshotsListView.addColumn(self.__tr("Date"))
        self.snapshotsListView.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.snapshotsListView.sizePolicy().hasHeightForWidth()))
        self.snapshotsListView.setMinimumSize(QSize(0,150))
        self.snapshotsListView.setHScrollBarMode(QListView.AlwaysOff)
        self.snapshotsListView.setAllColumnsShowFocus(1)
        self.snapshotsListView.setShowSortIndicator(1)
        layout5.addWidget(self.snapshotsListView)

        formMainLayout.addMultiCellLayout(layout5,0,2,0,0)

        self.toolBox = QToolBox(self,"toolBox")
        self.toolBox.setCurrentIndex(1)

        self.page1 = QWidget(self.toolBox,"page1")
        self.page1.setBackgroundMode(QWidget.PaletteBase)
        page1Layout = QGridLayout(self.page1,1,1,11,6,"page1Layout")

        self.planTextEdit = QTextEdit(self.page1,"planTextEdit")
        self.planTextEdit.setFrameShape(QTextEdit.MenuBarPanel)
        self.planTextEdit.setReadOnly(1)

        page1Layout.addWidget(self.planTextEdit,0,0)
        self.toolBox.addItem(self.page1,QString.fromLatin1(""))

        self.takeBackPage = QWidget(self.toolBox,"takeBackPage")
        self.takeBackPage.setBackgroundMode(QWidget.PaletteBase)
        takeBackPageLayout = QGridLayout(self.takeBackPage,1,1,11,6,"takeBackPageLayout")

        self.opDetailsListBox = QListBox(self.takeBackPage,"opDetailsListBox")
        self.opDetailsListBox.setFrameShape(QListBox.MenuBarPanel)
        self.opDetailsListBox.setSelectionMode(QListBox.Extended)

        takeBackPageLayout.addWidget(self.opDetailsListBox,0,0)
        self.toolBox.addItem(self.takeBackPage,QString.fromLatin1(""))

        formMainLayout.addWidget(self.toolBox,2,1)

        layout8 = QHBoxLayout(None,0,6,"layout8")

        self.noLabel = QLabel(self,"noLabel")
        layout8.addWidget(self.noLabel)

        self.typeLabel = QLabel(self,"typeLabel")
        layout8.addWidget(self.typeLabel)

        formMainLayout.addLayout(layout8,1,1)
        spacer2 = QSpacerItem(500,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        formMainLayout.addItem(spacer2,0,1)

        self.languageChange()

        self.resize(QSize(682,556).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("History Manager"))
        self.helpPushButton.setText(self.__tr("Help"))
        self.snapshotPushButton.setText(self.__tr("New"))
        self.restorePushButton.setText(self.__tr("Restore"))
        self.comboBox.setCurrentItem(0)
        self.snapshotsListView.header().setLabel(0,self.__tr("1"))
        self.snapshotsListView.header().setLabel(1,self.__tr("Date"))
        self.toolBox.setItemLabel(self.toolBox.indexOf(self.page1),self.__tr("TakeBack Plan"))
        self.toolBox.setItemLabel(self.toolBox.indexOf(self.takeBackPage),self.__tr("Operation Details"))
        self.noLabel.setText(QString.null)
        self.typeLabel.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("formMain",s,c)

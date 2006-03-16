# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PreferencesDialog.ui'
#
# Created: Prş Mar 16 17:28:11 2006
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20060126
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class PreferencesDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PreferencesDialog")

        self.setSizeGripEnabled(1)

        PreferencesDialogLayout = QGridLayout(self,1,1,11,6,"PreferencesDialogLayout")

        Layout1 = QHBoxLayout(None,0,6,"Layout1")

        self.buttonHelp = QPushButton(self,"buttonHelp")
        self.buttonHelp.setAutoDefault(1)
        Layout1.addWidget(self.buttonHelp)
        Horizontal_Spacing2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout1.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setAutoDefault(1)
        Layout1.addWidget(self.buttonCancel)

        PreferencesDialogLayout.addLayout(Layout1,1,0)

        self.tabWidget = QTabWidget(self,"tabWidget")

        self.Widget3 = QWidget(self.tabWidget,"Widget3")
        Widget3Layout = QGridLayout(self.Widget3,1,1,11,6,"Widget3Layout")

        self.repoListView = KListView(self.Widget3,"repoListView")
        self.repoListView.addColumn(i18n("Repository Name"))
        self.repoListView.addColumn(i18n("Address"))
        self.repoListView.setAllColumnsShowFocus(1)
        self.repoListView.setResizeMode(KListView.LastColumn)
        self.repoListView.setFullWidth(1)

        Widget3Layout.addWidget(self.repoListView,0,0)

        layout3 = QVBoxLayout(None,0,6,"layout3")

        self.addButton = KPushButton(self.Widget3,"addButton")
        layout3.addWidget(self.addButton)

        self.editButton = KPushButton(self.Widget3,"editButton")
        layout3.addWidget(self.editButton)

        self.removeButton = KPushButton(self.Widget3,"removeButton")
        layout3.addWidget(self.removeButton)

        self.moveUpButton = KPushButton(self.Widget3,"moveUpButton")
        layout3.addWidget(self.moveUpButton)

        self.moveDownButton = KPushButton(self.Widget3,"moveDownButton")
        layout3.addWidget(self.moveDownButton)

        self.updateRepoButton = KPushButton(self.Widget3,"updateRepoButton")
        layout3.addWidget(self.updateRepoButton)
        spacer1 = QSpacerItem(41,20,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout3.addItem(spacer1)

        Widget3Layout.addLayout(layout3,0,1)
        self.tabWidget.insertTab(self.Widget3,QString.fromLatin1(""))

        self.Widget2 = QWidget(self.tabWidget,"Widget2")
        Widget2Layout = QGridLayout(self.Widget2,1,1,11,6,"Widget2Layout")

        self.onlyShowPrograms = QCheckBox(self.Widget2,"onlyShowPrograms")

        Widget2Layout.addWidget(self.onlyShowPrograms,0,0)

        self.checkBox2 = QCheckBox(self.Widget2,"checkBox2")

        Widget2Layout.addWidget(self.checkBox2,1,0)
        spacer4 = QSpacerItem(31,170,QSizePolicy.Minimum,QSizePolicy.Expanding)
        Widget2Layout.addItem(spacer4,2,0)
        self.tabWidget.insertTab(self.Widget2,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabWidget,"TabPage")
        TabPageLayout = QGridLayout(self.TabPage,1,1,11,6,"TabPageLayout")

        self.groupBox2 = QGroupBox(self.TabPage,"groupBox2")

        self.pushButton4 = QPushButton(self.groupBox2,"pushButton4")
        self.pushButton4.setGeometry(QRect(19,67,140,23))

        self.textLabel3 = QLabel(self.groupBox2,"textLabel3")
        self.textLabel3.setGeometry(QRect(10,20,394,40))

        TabPageLayout.addWidget(self.groupBox2,1,0)

        self.groupBox1 = QGroupBox(self.TabPage,"groupBox1")

        self.textLabel1_2 = QLabel(self.groupBox1,"textLabel1_2")
        self.textLabel1_2.setEnabled(0)
        self.textLabel1_2.setGeometry(QRect(42,51,123,21))

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")
        self.textLabel2.setEnabled(0)
        self.textLabel2.setGeometry(QRect(320,50,110,20))

        self.textLabel1 = QLabel(self.groupBox1,"textLabel1")
        self.textLabel1.setEnabled(0)
        self.textLabel1.setGeometry(QRect(283,51,18,21))

        self.lineEdit1 = QLineEdit(self.groupBox1,"lineEdit1")
        self.lineEdit1.setEnabled(0)
        self.lineEdit1.setGeometry(QRect(171,51,106,21))
        self.lineEdit1.setFrameShape(QLineEdit.LineEditPanel)
        self.lineEdit1.setFrame(1)

        self.checkBox2_2 = QCheckBox(self.groupBox1,"checkBox2_2")
        self.checkBox2_2.setGeometry(QRect(13,26,310,19))
        self.checkBox2_2.setChecked(0)
        self.checkBox2_2.setTristate(0)

        TabPageLayout.addWidget(self.groupBox1,0,0)
        self.tabWidget.insertTab(self.TabPage,QString.fromLatin1(""))

        PreferencesDialogLayout.addWidget(self.tabWidget,0,0)

        self.languageChange()

        self.resize(QSize(611,348).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(i18n("PiSi Settings"))
        self.buttonHelp.setText(i18n("&Help"))
        self.buttonHelp.setAccel(QKeySequence(i18n("F1")))
        self.buttonOk.setText(i18n("&OK"))
        self.buttonOk.setAccel(QKeySequence(QString.null))
        self.buttonCancel.setText(i18n("&Cancel"))
        self.buttonCancel.setAccel(QKeySequence(QString.null))
        self.repoListView.header().setLabel(0,i18n("Repository Name"))
        self.repoListView.header().setLabel(1,i18n("Address"))
        QToolTip.add(self.repoListView,i18n("You can see current software repositories and corresponding addresses here"))
        self.addButton.setText(i18n("&Add New Repository"))
        QToolTip.add(self.addButton,i18n("Click here to add a new software repository"))
        self.editButton.setText(i18n("&Edit Repository"))
        QToolTip.add(self.editButton,i18n("Click here to modify the name or address of a repository"))
        self.removeButton.setText(i18n("&Remove Repository"))
        QToolTip.add(self.removeButton,i18n("Click here to delete a repository from the list"))
        self.moveUpButton.setText(i18n("Move &Up"))
        QToolTip.add(self.moveUpButton,i18n("Click here to move the repository one level up"))
        self.moveDownButton.setText(i18n("Move &Down"))
        QToolTip.add(self.moveDownButton,i18n("Click here to move the repository one level down"))
        self.updateRepoButton.setText(i18n("&Update All Repositories"))
        QToolTip.add(self.updateRepoButton,i18n("Click here to update all repositories so that you can use  "))
        self.tabWidget.changeTab(self.Widget3,i18n("&Repositories"))
        self.onlyShowPrograms.setText(i18n("&Show only desktop applications"))
        QToolTip.add(self.onlyShowPrograms,i18n("If checked, then pisi will only show desktop applications"))
        self.checkBox2.setText(i18n("&Automatically check for updates when started"))
        QToolTip.add(self.checkBox2,i18n("If checked, then updates for Pardus will be automatically checked and you will be notified"))
        self.tabWidget.changeTab(self.Widget2,i18n("&General Settings"))
        self.groupBox2.setTitle(i18n("Cache cleaning"))
        self.pushButton4.setText(i18n("C&lean disk cache now"))
        self.textLabel3.setText(i18n("Cleaning up the disk cache will remove all downloaded software. \n"
"This will not delete installed software or affect your system stability."))
        self.groupBox1.setTitle(i18n("Cache usage"))
        self.textLabel1_2.setText(i18n("Maximum cache size:"))
        self.textLabel2.setText(i18n("<i>(Use 0 for no limit)</i>"))
        self.textLabel1.setText(i18n("Mb"))
        self.lineEdit1.setText(i18n("2000"))
        self.checkBox2_2.setText(i18n("&Use hard disk cache for downloaded software"))
        QToolTip.add(self.checkBox2_2,i18n("If checked, then updates for Pardus will be automatically checked and you will be notified"))
        self.tabWidget.changeTab(self.TabPage,i18n("C&ache"))


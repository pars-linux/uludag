# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './setupuserswidget.ui'
#
# Created: Pzt Ara 26 13:17:51 2005
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20051013
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class SetupUsersWidget(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("SetupUsersWidget")


        SetupUsersWidgetLayout = QGridLayout(self,1,1,11,6,"SetupUsersWidgetLayout")

        self.pass_error = QLabel(self,"pass_error")
        self.pass_error.setTextFormat(QLabel.RichText)
        self.pass_error.setAlignment(QLabel.WordBreak | QLabel.AlignCenter)

        SetupUsersWidgetLayout.addMultiCellWidget(self.pass_error,1,1,0,1)

        self.buttonGroup1 = QButtonGroup(self,"buttonGroup1")
        self.buttonGroup1.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup1.layout().setSpacing(6)
        self.buttonGroup1.layout().setMargin(11)
        buttonGroup1Layout = QGridLayout(self.buttonGroup1.layout())
        buttonGroup1Layout.setAlignment(Qt.AlignTop)

        self.textLabel1_3 = QLabel(self.buttonGroup1,"textLabel1_3")

        buttonGroup1Layout.addWidget(self.textLabel1_3,0,0)

        self.username = QLineEdit(self.buttonGroup1,"username")

        buttonGroup1Layout.addWidget(self.username,0,1)

        self.pass2 = QLineEdit(self.buttonGroup1,"pass2")
        self.pass2.setEchoMode(QLineEdit.Password)

        buttonGroup1Layout.addWidget(self.pass2,3,1)

        self.textLabel1 = QLabel(self.buttonGroup1,"textLabel1")

        buttonGroup1Layout.addWidget(self.textLabel1,3,0)

        self.textLabel1_2 = QLabel(self.buttonGroup1,"textLabel1_2")

        buttonGroup1Layout.addWidget(self.textLabel1_2,2,0)

        self.pass1 = QLineEdit(self.buttonGroup1,"pass1")
        self.pass1.setEchoMode(QLineEdit.Password)

        buttonGroup1Layout.addWidget(self.pass1,2,1)

        self.textLabel1_4 = QLabel(self.buttonGroup1,"textLabel1_4")

        buttonGroup1Layout.addWidget(self.textLabel1_4,1,0)

        self.realname = QLineEdit(self.buttonGroup1,"realname")

        buttonGroup1Layout.addWidget(self.realname,1,1)

        self.pix = QLabel(self.buttonGroup1,"pix")
        self.pix.setAlignment(QLabel.AlignCenter)

        buttonGroup1Layout.addMultiCellWidget(self.pix,2,3,2,2)

        layout2 = QVBoxLayout(None,0,6,"layout2")

        self.createButton = QPushButton(self.buttonGroup1,"createButton")
        layout2.addWidget(self.createButton)

        self.cancelButton = KPushButton(self.buttonGroup1,"cancelButton")
        layout2.addWidget(self.cancelButton)

        buttonGroup1Layout.addMultiCellLayout(layout2,0,1,2,2)

        SetupUsersWidgetLayout.addMultiCellWidget(self.buttonGroup1,0,0,0,1)

        self.deleteButton = QPushButton(self,"deleteButton")

        SetupUsersWidgetLayout.addWidget(self.deleteButton,3,1)
        spacer7 = QSpacerItem(20,130,QSizePolicy.Minimum,QSizePolicy.Expanding)
        SetupUsersWidgetLayout.addItem(spacer7,4,1)

        self.textLabel2 = QLabel(self,"textLabel2")

        SetupUsersWidgetLayout.addMultiCellWidget(self.textLabel2,2,2,0,1)

        self.userList = QListBox(self,"userList")

        SetupUsersWidgetLayout.addMultiCellWidget(self.userList,3,4,0,0)

        self.languageChange()

        self.resize(QSize(383,377).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.username,self.realname)
        self.setTabOrder(self.realname,self.pass1)
        self.setTabOrder(self.pass1,self.pass2)
        self.setTabOrder(self.pass2,self.createButton)
        self.setTabOrder(self.createButton,self.userList)
        self.setTabOrder(self.userList,self.deleteButton)


    def languageChange(self):
        self.pass_error.setText(QString.null)
        self.buttonGroup1.setTitle(i18n("New User"))
        self.textLabel1_3.setText(i18n("User Name:"))
        self.textLabel1.setText(i18n("Password (again):"))
        self.textLabel1_2.setText(i18n("Password:"))
        self.textLabel1_4.setText(i18n("Real Name:"))
        self.pix.setText(QString.null)
        self.createButton.setText(i18n("Create User"))
        self.createButton.setAccel(QString.null)
        self.cancelButton.setText(i18n("&Cancel"))
        self.deleteButton.setText(i18n("Delete Selected User"))
        self.textLabel2.setText(i18n("Users:"))


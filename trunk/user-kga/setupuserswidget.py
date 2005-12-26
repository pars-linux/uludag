# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setupuserswidget.ui'
#
# Created: Pzt Ara 26 06:35:53 2005
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20051013
#
# WARNING! All changes made in this file will be lost!


from qt import *


class SetupUsersWidget(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("SetupUsersWidget")


        SetupUsersWidgetLayout = QGridLayout(self,1,1,11,6,"SetupUsersWidgetLayout")
        spacer9 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        SetupUsersWidgetLayout.addItem(spacer9,0,1)
        spacer12 = QSpacerItem(61,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        SetupUsersWidgetLayout.addItem(spacer12,1,2)
        spacer12_2 = QSpacerItem(61,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        SetupUsersWidgetLayout.addItem(spacer12_2,1,0)
        spacer14_2 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        SetupUsersWidgetLayout.addItem(spacer14_2,4,0)

        layout5 = QGridLayout(None,1,1,0,6,"layout5")
        spacer7 = QSpacerItem(20,70,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout5.addItem(spacer7,2,1)

        self.deleteButton = QPushButton(self,"deleteButton")

        layout5.addWidget(self.deleteButton,1,1)

        self.userList = QListBox(self,"userList")

        layout5.addMultiCellWidget(self.userList,1,2,0,0)

        self.textLabel2 = QLabel(self,"textLabel2")

        layout5.addMultiCellWidget(self.textLabel2,0,0,0,1)

        SetupUsersWidgetLayout.addLayout(layout5,4,1)
        spacer11 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        SetupUsersWidgetLayout.addItem(spacer11,5,1)
        spacer14 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        SetupUsersWidgetLayout.addItem(spacer14,4,2)

        self.pass_error = QLabel(self,"pass_error")
        self.pass_error.setTextFormat(QLabel.RichText)
        self.pass_error.setAlignment(QLabel.WordBreak | QLabel.AlignCenter)

        SetupUsersWidgetLayout.addWidget(self.pass_error,2,1)

        self.buttonGroup1 = QButtonGroup(self,"buttonGroup1")
        self.buttonGroup1.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup1.layout().setSpacing(6)
        self.buttonGroup1.layout().setMargin(11)
        buttonGroup1Layout = QGridLayout(self.buttonGroup1.layout())
        buttonGroup1Layout.setAlignment(Qt.AlignTop)

        self.textLabel1_3 = QLabel(self.buttonGroup1,"textLabel1_3")

        buttonGroup1Layout.addWidget(self.textLabel1_3,0,0)

        self.createButton = QPushButton(self.buttonGroup1,"createButton")

        buttonGroup1Layout.addWidget(self.createButton,0,2)

        self.username = QLineEdit(self.buttonGroup1,"username")

        buttonGroup1Layout.addWidget(self.username,0,1)

        self.pass2 = QLineEdit(self.buttonGroup1,"pass2")
        self.pass2.setEchoMode(QLineEdit.Password)

        buttonGroup1Layout.addMultiCellWidget(self.pass2,3,4,1,1)

        self.textLabel1 = QLabel(self.buttonGroup1,"textLabel1")

        buttonGroup1Layout.addMultiCellWidget(self.textLabel1,3,4,0,0)

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

        buttonGroup1Layout.addMultiCellWidget(self.pix,1,3,2,2)

        SetupUsersWidgetLayout.addWidget(self.buttonGroup1,1,1)

        self.languageChange()

        self.resize(QSize(501,459).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.username,self.realname)
        self.setTabOrder(self.realname,self.pass1)
        self.setTabOrder(self.pass1,self.pass2)
        self.setTabOrder(self.pass2,self.createButton)
        self.setTabOrder(self.createButton,self.userList)
        self.setTabOrder(self.userList,self.deleteButton)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.deleteButton.setText(self.__tr("Delete Selected User"))
        self.textLabel2.setText(self.__tr("Users:"))
        self.pass_error.setText(QString.null)
        self.buttonGroup1.setTitle(self.__tr("New User"))
        self.textLabel1_3.setText(self.__tr("User Name:"))
        self.createButton.setText(self.__tr("Create User"))
        self.textLabel1.setText(self.__tr("Password (again):"))
        self.textLabel1_2.setText(self.__tr("Password:"))
        self.textLabel1_4.setText(self.__tr("Real Name:"))
        self.pix.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("SetupUsersWidget",s,c)

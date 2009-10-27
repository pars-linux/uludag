# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newConn.ui'
#
# Created: Sal Eki 28 22:46:14 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class NewConn(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("NewConn")


        NewConnLayout = QGridLayout(self,1,1,11,6,"NewConnLayout")

        self.deviceLabel = QLabel(self,"deviceLabel")

        NewConnLayout.addMultiCellWidget(self.deviceLabel,0,0,0,2)

        self.links = QListView(self,"links")
        self.links.addColumn(QString.null)
        self.links.addColumn(QString.null)
        self.links.setAllColumnsShowFocus(1)

        NewConnLayout.addMultiCellWidget(self.links,1,1,0,2)

        self.cancelBut = QPushButton(self,"cancelBut")

        NewConnLayout.addWidget(self.cancelBut,2,2)

        self.createBut = QPushButton(self,"createBut")
        self.createBut.setEnabled(0)
        self.createBut.setDefault(1)

        NewConnLayout.addWidget(self.createBut,2,1)
        spacer2 = QSpacerItem(91,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        NewConnLayout.addItem(spacer2,2,0)

        self.languageChange()

        self.resize(QSize(295,369).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Form2"))
        self.deviceLabel.setText(QString.null)
        self.links.header().setLabel(0,QString.null)
        self.links.header().setLabel(1,QString.null)
        self.cancelBut.setText(QString.null)
        self.createBut.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("NewConn",s,c)

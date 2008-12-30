# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connSharing.ui'
#
# Created: Sal Eki 28 19:34:23 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class ConnSharing(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ConnSharing")


        ConnSharingLayout = QGridLayout(self,1,1,11,6,"ConnSharingLayout")

        self.applyBut = QPushButton(self,"applyBut")
        self.applyBut.setEnabled(0)

        ConnSharingLayout.addWidget(self.applyBut,2,1)

        self.cancelBut = QPushButton(self,"cancelBut")

        ConnSharingLayout.addWidget(self.cancelBut,2,2)

        self.sharecheckBox = QCheckBox(self,"sharecheckBox")

        ConnSharingLayout.addWidget(self.sharecheckBox,0,0)

        self.groupBox1 = QGroupBox(self,"groupBox1")
        self.groupBox1.setEnabled(0)
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.textLabel1 = QLabel(self.groupBox1,"textLabel1")

        groupBox1Layout.addWidget(self.textLabel1,0,0)

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")

        groupBox1Layout.addWidget(self.textLabel2,1,0)

        self.intcombo = QComboBox(0,self.groupBox1,"intcombo")

        groupBox1Layout.addWidget(self.intcombo,0,1)

        self.sharecombo = QComboBox(0,self.groupBox1,"sharecombo")

        groupBox1Layout.addWidget(self.sharecombo,1,1)

        ConnSharingLayout.addMultiCellWidget(self.groupBox1,1,1,0,2)
        spacer1 = QSpacerItem(131,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        ConnSharingLayout.addItem(spacer1,2,0)

        self.languageChange()

        self.resize(QSize(359,147).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.textLabel1.setBuddy(self.intcombo)
        self.textLabel2.setBuddy(self.sharecombo)


    def languageChange(self):
        self.setCaption(QString.null)
        self.applyBut.setText(QString.null)
        self.cancelBut.setText(QString.null)
        self.sharecheckBox.setText(QString.null)
        self.groupBox1.setTitle(QString.null)
        self.textLabel1.setText(QString.null)
        self.textLabel2.setText(QString.null)


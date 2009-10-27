# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nameConf.ui'
#
# Created: Sal Eki 28 20:44:43 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class NameConf(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("NameConf")


        NameConfLayout = QGridLayout(self,1,1,7,4,"NameConfLayout")

        self.host = QLineEdit(self,"host")

        NameConfLayout.addMultiCellWidget(self.host,0,0,1,3)

        self.hostNameLabel = QLabel(self,"hostNameLabel")

        NameConfLayout.addWidget(self.hostNameLabel,0,0)

        layout4 = QVBoxLayout(None,5,2,"layout4")

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.line1 = QFrame(self,"line1")
        self.line1.setMinimumSize(QSize(30,0))
        self.line1.setMaximumSize(QSize(30,32767))
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        layout3.addWidget(self.line1)

        self.nameServLabel = QLabel(self,"nameServLabel")
        layout3.addWidget(self.nameServLabel)

        self.line2 = QFrame(self,"line2")
        self.line2.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Fixed,0,0,self.line2.sizePolicy().hasHeightForWidth()))
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        self.line2.setFrameShape(QFrame.HLine)
        layout3.addWidget(self.line2)
        layout4.addLayout(layout3)

        self.dns = QListBox(self,"dns")
        layout4.addWidget(self.dns)

        layout1 = QHBoxLayout(None,3,3,"layout1")

        self.b1 = QPushButton(self,"b1")
        layout1.addWidget(self.b1)

        self.b2 = QPushButton(self,"b2")
        layout1.addWidget(self.b2)

        self.b4 = QPushButton(self,"b4")
        layout1.addWidget(self.b4)

        self.b3 = QPushButton(self,"b3")
        layout1.addWidget(self.b3)
        layout4.addLayout(layout1)

        NameConfLayout.addMultiCellLayout(layout4,1,1,0,3)

        self.cancelBut = QPushButton(self,"cancelBut")

        NameConfLayout.addWidget(self.cancelBut,2,3)

        self.applyBut = QPushButton(self,"applyBut")

        NameConfLayout.addWidget(self.applyBut,2,2)
        spacer1 = QSpacerItem(140,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        NameConfLayout.addMultiCell(spacer1,2,2,0,1)

        self.languageChange()

        self.resize(QSize(343,236).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(QString.null)
        self.hostNameLabel.setText(self.__tr("Host Name :"))
        self.nameServLabel.setText(self.__tr("Name Servers"))
        self.b1.setText(self.__tr("Up"))
        self.b2.setText(self.__tr("Down"))
        self.b4.setText(self.__tr("Add"))
        self.b3.setText(self.__tr("Remove"))
        self.cancelBut.setText(self.__tr("Cancel"))
        self.applyBut.setText(self.__tr("Apply"))


    def __tr(self,s,c = None):
        return qApp.translate("NameConf",s,c)

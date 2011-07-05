# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './disconnect.ui'
#
# Created: Fri Sep 12 16:29:45 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Disconnect(object):
    def setupUi(self, Disconnect):
        Disconnect.setObjectName("Disconnect")
        Disconnect.resize(316, 137)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Disconnect.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Disconnect)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.iconDisLabel = QtGui.QLabel(Disconnect)
        self.iconDisLabel.setPixmap(QtGui.QPixmap("/usr/share/sinerji/images/connect.png"))
        self.iconDisLabel.setObjectName("iconDisLabel")
        self.horizontalLayout_2.addWidget(self.iconDisLabel)
        self.clientTextLabel = QtGui.QLabel(Disconnect)
        self.clientTextLabel.setObjectName("clientTextLabel")
        self.horizontalLayout_2.addWidget(self.clientTextLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtGui.QFrame(Disconnect)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(140, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.disconnectButton = QtGui.QPushButton(Disconnect)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/disconnect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.disconnectButton.setIcon(icon1)
        self.disconnectButton.setObjectName("disconnectButton")
        self.horizontalLayout.addWidget(self.disconnectButton)
        self.okButton = QtGui.QPushButton(Disconnect)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/buttonApply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okButton.setIcon(icon2)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Disconnect)
        QtCore.QMetaObject.connectSlotsByName(Disconnect)

    def retranslateUi(self, Disconnect):
        Disconnect.setWindowTitle(QtGui.QApplication.translate("Disconnect", "Sinerji", None, QtGui.QApplication.UnicodeUTF8))
        self.disconnectButton.setText(QtGui.QApplication.translate("Disconnect", "Disconnect", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Disconnect", "Ok", None, QtGui.QApplication.UnicodeUTF8))


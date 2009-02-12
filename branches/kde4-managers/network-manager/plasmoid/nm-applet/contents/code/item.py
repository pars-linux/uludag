# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nm-applet/contents/ui/item.ui'
#
# Created: Thu Feb 12 18:01:12 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_connectionItem(object):
    def setupUi(self, connectionItem):
        connectionItem.setObjectName("connectionItem")
        connectionItem.resize(228, 32)
        connectionItem.setMinimumSize(QtCore.QSize(0, 32))
        connectionItem.setMaximumSize(QtCore.QSize(16777215, 32))
        self.gridLayout_2 = QtGui.QGridLayout(connectionItem)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtGui.QFrame(connectionItem)
        self.frame.setMinimumSize(QtCore.QSize(0, 30))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 32))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.connectionStatus = QtGui.QLabel(self.frame)
        self.connectionStatus.setMinimumSize(QtCore.QSize(22, 22))
        self.connectionStatus.setMaximumSize(QtCore.QSize(22, 22))
        self.connectionStatus.setPixmap(QtGui.QPixmap(":/icons/icons/network-wireless_tools.png"))
        self.connectionStatus.setScaledContents(True)
        self.connectionStatus.setObjectName("connectionStatus")
        self.horizontalLayout.addWidget(self.connectionStatus)
        self.connectionName = QtGui.QLabel(self.frame)
        self.connectionName.setObjectName("connectionName")
        self.horizontalLayout.addWidget(self.connectionName)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.connectionSignal = QtGui.QProgressBar(self.frame)
        self.connectionSignal.setMaximumSize(QtCore.QSize(80, 16777215))
        self.connectionSignal.setProperty("value", QtCore.QVariant(24))
        self.connectionSignal.setTextVisible(False)
        self.connectionSignal.setObjectName("connectionSignal")
        self.horizontalLayout.addWidget(self.connectionSignal)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(connectionItem)
        QtCore.QMetaObject.connectSlotsByName(connectionItem)

    def retranslateUi(self, connectionItem):
        connectionItem.setWindowTitle(QtGui.QApplication.translate("connectionItem", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.connectionName.setText(QtGui.QApplication.translate("connectionItem", "test", None, QtGui.QApplication.UnicodeUTF8))

import data_rc

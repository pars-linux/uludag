# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nm-applet/contents/ui/popup.ui'
#
# Created: Tue Feb 24 08:37:29 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Connection(object):
    def setupUi(self, Connection):
        Connection.setObjectName("Connection")
        Connection.resize(253, 163)
        self.verticalLayout_5 = QtGui.QVBoxLayout(Connection)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.net_tools = QtGui.QGroupBox(Connection)
        self.net_tools.setAutoFillBackground(False)
        self.net_tools.setFlat(True)
        self.net_tools.setObjectName("net_tools")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.net_tools)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(-1, 5, -1, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.net_tools)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.ethernetStatus = QtGui.QLabel(self.net_tools)
        self.ethernetStatus.setObjectName("ethernetStatus")
        self.verticalLayout.addWidget(self.ethernetStatus)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.label_3 = QtGui.QLabel(self.net_tools)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(32, 32))
        self.label_3.setMaximumSize(QtCore.QSize(32, 32))
        self.label_3.setPixmap(QtGui.QPixmap(":/icons/network-net_tools.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.ethernetConnections = QtGui.QFrame(self.net_tools)
        self.ethernetConnections.setFrameShape(QtGui.QFrame.NoFrame)
        self.ethernetConnections.setFrameShadow(QtGui.QFrame.Raised)
        self.ethernetConnections.setLineWidth(0)
        self.ethernetConnections.setObjectName("ethernetConnections")
        self.ethernetLayout = QtGui.QVBoxLayout(self.ethernetConnections)
        self.ethernetLayout.setSpacing(2)
        self.ethernetLayout.setMargin(0)
        self.ethernetLayout.setObjectName("ethernetLayout")
        self.verticalLayout_2.addWidget(self.ethernetConnections)
        self.verticalLayout_5.addWidget(self.net_tools)
        self.seperator = QtGui.QFrame(Connection)
        self.seperator.setFrameShape(QtGui.QFrame.HLine)
        self.seperator.setFrameShadow(QtGui.QFrame.Sunken)
        self.seperator.setObjectName("seperator")
        self.verticalLayout_5.addWidget(self.seperator)
        self.wireless_tools = QtGui.QGroupBox(Connection)
        self.wireless_tools.setAutoFillBackground(False)
        self.wireless_tools.setFlat(True)
        self.wireless_tools.setObjectName("wireless_tools")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.wireless_tools)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(-1, 3, -1, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtGui.QLabel(self.wireless_tools)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.wirelessStatus = QtGui.QLabel(self.wireless_tools)
        self.wirelessStatus.setObjectName("wirelessStatus")
        self.verticalLayout_3.addWidget(self.wirelessStatus)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.label_6 = QtGui.QLabel(self.wireless_tools)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(32, 32))
        self.label_6.setMaximumSize(QtCore.QSize(32, 32))
        self.label_6.setPixmap(QtGui.QPixmap(":/icons/network-wireless_tools.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.wirelessConnections = QtGui.QFrame(self.wireless_tools)
        self.wirelessConnections.setFrameShape(QtGui.QFrame.NoFrame)
        self.wirelessConnections.setFrameShadow(QtGui.QFrame.Raised)
        self.wirelessConnections.setLineWidth(0)
        self.wirelessConnections.setObjectName("wirelessConnections")
        self.wirelessLayout = QtGui.QVBoxLayout(self.wirelessConnections)
        self.wirelessLayout.setSpacing(2)
        self.wirelessLayout.setMargin(0)
        self.wirelessLayout.setObjectName("wirelessLayout")
        self.verticalLayout_4.addWidget(self.wirelessConnections)
        self.verticalLayout_5.addWidget(self.wireless_tools)

        self.retranslateUi(Connection)
        QtCore.QMetaObject.connectSlotsByName(Connection)

    def retranslateUi(self, Connection):
        Connection.setWindowTitle(QtGui.QApplication.translate("Connection", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Connection", "Ethernet", None, QtGui.QApplication.UnicodeUTF8))
        self.ethernetStatus.setText(QtGui.QApplication.translate("Connection", "Not connected.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Connection", "Wireless", None, QtGui.QApplication.UnicodeUTF8))
        self.wirelessStatus.setText(QtGui.QApplication.translate("Connection", "Not connected.", None, QtGui.QApplication.UnicodeUTF8))

import data_rc

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nm-applet/contents/ui/item.ui'
#
# Created: Thu Feb 19 12:46:18 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_connectionItem(object):
    def setupUi(self, connectionItem):
        connectionItem.setObjectName("connectionItem")
        connectionItem.resize(210, 28)
        connectionItem.setMinimumSize(QtCore.QSize(0, 28))
        connectionItem.setMaximumSize(QtCore.QSize(16777215, 30))
        self.gridLayout = QtGui.QGridLayout(connectionItem)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.button = QtGui.QPushButton(connectionItem)
        self.button.setMinimumSize(QtCore.QSize(0, 28))
        self.button.setMaximumSize(QtCore.QSize(16777215, 28))
        self.button.setStyleSheet("""padding-left:4px;
padding-right:4px;
text-align:left;
border:1px solid rgba(0,0,0,0);""")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/network-wireless_tools.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(icon)
        self.button.setFlat(False)
        self.button.setObjectName("button")
        self.gridLayout.addWidget(self.button, 0, 0, 1, 1)

        self.retranslateUi(connectionItem)
        QtCore.QMetaObject.connectSlotsByName(connectionItem)

    def retranslateUi(self, connectionItem):
        connectionItem.setWindowTitle(QtGui.QApplication.translate("connectionItem", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.button.setText(QtGui.QApplication.translate("connectionItem", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

import data_rc
import data_rc

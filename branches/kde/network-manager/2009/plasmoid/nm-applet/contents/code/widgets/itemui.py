#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from contents/ui/item.ui on Thu Jul  2 11:15:17 2009
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

class Ui_connectionItem(object):
    def setupUi(self, connectionItem):
        connectionItem.setObjectName("connectionItem")
        connectionItem.resize(212, 28)
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
        connectionItem.setWindowTitle(kdecore.i18n("Form"))
        self.button.setText(kdecore.i18n("PushButton"))

import data_rc
import data_rc
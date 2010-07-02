# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgetOptCD.ui'
#
# Created: Mon Jun 14 20:48:51 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_widgetOptCD(object):
    def setupUi(self, widgetOptCD):
        widgetOptCD.setObjectName("widgetOptCD")
        widgetOptCD.resize(407, 174)
        widgetOptCD.setWindowTitle("")
        self.verticalLayoutWidget = QtGui.QWidget(widgetOptCD)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblDescription = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblDescription.setObjectName("lblDescription")
        self.verticalLayout.addWidget(self.lblDescription)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtPath = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.txtPath.setEnabled(False)
        self.txtPath.setObjectName("txtPath")
        self.horizontalLayout.addWidget(self.txtPath)
        self.btnBrowse = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btnBrowse.setObjectName("btnBrowse")
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(widgetOptCD)
        QtCore.QMetaObject.connectSlotsByName(widgetOptCD)

    def retranslateUi(self, widgetOptCD):
        self.lblDescription.setText(QtGui.QApplication.translate("widgetOptCD", "Description for choosing CD/DVD path", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("widgetOptCD", "Browse...", None, QtGui.QApplication.UnicodeUTF8))


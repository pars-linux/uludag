# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgetOptISO.ui'
#
# Created: Mon Jun 14 20:48:52 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_widgetOptISO(object):
    def setupUi(self, widgetOptISO):
        widgetOptISO.setObjectName("widgetOptISO")
        widgetOptISO.resize(402, 192)
        widgetOptISO.setWindowTitle("")
        self.verticalLayoutWidget = QtGui.QWidget(widgetOptISO)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelDescription = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelDescription.setObjectName("labelDescription")
        self.verticalLayout.addWidget(self.labelDescription)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtFileName = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.txtFileName.setEnabled(False)
        self.txtFileName.setObjectName("txtFileName")
        self.horizontalLayout.addWidget(self.txtFileName)
        self.btnBrowse = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btnBrowse.setObjectName("btnBrowse")
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(widgetOptISO)
        QtCore.QMetaObject.connectSlotsByName(widgetOptISO)

    def retranslateUi(self, widgetOptISO):
        self.labelDescription.setText(QtGui.QApplication.translate("widgetOptISO", "Description for choosing ISO from file.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("widgetOptISO", "Browse...", None, QtGui.QApplication.UnicodeUTF8))


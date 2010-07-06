# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgetOptCD.ui'
#
# Created: Tue Jul 06 15:01:17 2010
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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 418, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblDescription = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblDescription.setObjectName("lblDescription")
        self.verticalLayout.addWidget(self.lblDescription)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboDrive = QtGui.QComboBox(self.verticalLayoutWidget)
        self.comboDrive.setObjectName("comboDrive")
        self.horizontalLayout.addWidget(self.comboDrive)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(widgetOptCD)
        QtCore.QMetaObject.connectSlotsByName(widgetOptCD)

    def retranslateUi(self, widgetOptCD):
        self.lblDescription.setText(QtGui.QApplication.translate("widgetOptCD", "Choose your CD drive which has Pardus Live CD in it.", None, QtGui.QApplication.UnicodeUTF8))


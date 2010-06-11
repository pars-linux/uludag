# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgetWelcome.ui'
#
# Created: Fri Jun 11 02:42:44 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_widgetWelcome(object):
    def setupUi(self, widgetWelcome):
        widgetWelcome.setObjectName("widgetWelcome")
        widgetWelcome.resize(462, 264)
        self.verticalLayoutWidget = QtGui.QWidget(widgetWelcome)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 421, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblWelcome = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblWelcome.setObjectName("lblWelcome")
        self.verticalLayout.addWidget(self.lblWelcome)
        self.lblDescription = QtGui.QLabel(self.verticalLayoutWidget)
        self.lblDescription.setObjectName("lblDescription")
        self.verticalLayout.addWidget(self.lblDescription)

        self.retranslateUi(widgetWelcome)
        QtCore.QMetaObject.connectSlotsByName(widgetWelcome)

    def retranslateUi(self, widgetWelcome):
        self.lblWelcome.setText(QtGui.QApplication.translate("widgetWelcome", "Welcome message for PaWn", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDescription.setText(QtGui.QApplication.translate("widgetWelcome", "Installation description about PaWn", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgetWelcome.ui'
#
# Created: Tue Jul 06 14:44:22 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_widgetWelcome(object):
    def setupUi(self, widgetWelcome):
        widgetWelcome.setObjectName("widgetWelcome")
        widgetWelcome.resize(462, 264)
        widgetWelcome.setWindowTitle("")
        self.gridLayout = QtGui.QGridLayout(widgetWelcome)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblWelcome = QtGui.QLabel(widgetWelcome)
        self.lblWelcome.setWordWrap(True)
        self.lblWelcome.setObjectName("lblWelcome")
        self.verticalLayout.addWidget(self.lblWelcome)
        self.lblDescription = QtGui.QLabel(widgetWelcome)
        self.lblDescription.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.lblDescription.setWordWrap(True)
        self.lblDescription.setObjectName("lblDescription")
        self.verticalLayout.addWidget(self.lblDescription)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(widgetWelcome)
        QtCore.QMetaObject.connectSlotsByName(widgetWelcome)

    def retranslateUi(self, widgetWelcome):
        self.lblWelcome.setText(QtGui.QApplication.translate("widgetWelcome", "Welcome to PaW–Pardus Installer for Microsoft(R) Windows(TM)!\n"
"\n"
"You can set up a Pardus Linux installation to your computer easily and without loss of your files or documents.\n"
"\n"
"Pardus is an Linux based open source and free operating system powered by TÜBİTAK/UEKAE.", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDescription.setText(QtGui.QApplication.translate("widgetWelcome", "This setup wizard will help you proceed configuration and installation of Pardus. Please press Next to start configuring your new Pardus!\n"
"\n"
"It is recommeded to close all running programs before starting installation. ", None, QtGui.QApplication.UnicodeUTF8))


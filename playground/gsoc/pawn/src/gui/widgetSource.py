# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgetSource.ui'
#
# Created: Thu Jun 10 04:10:32 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_widgetSource(object):
    def setupUi(self, widgetSource):
        widgetSource.setObjectName("widgetSource")
        widgetSource.resize(425, 167)
        self.verticalLayoutWidget = QtGui.QWidget(widgetSource)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 421, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.optInternet = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.optInternet.setObjectName("optInternet")
        self.verticalLayout_2.addWidget(self.optInternet)
        self.optCD = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.optCD.setObjectName("optCD")
        self.verticalLayout_2.addWidget(self.optCD)
        self.optISO = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.optISO.setObjectName("optISO")
        self.verticalLayout_2.addWidget(self.optISO)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(widgetSource)
        QtCore.QMetaObject.connectSlotsByName(widgetSource)

    def retranslateUi(self, widgetSource):
        self.label.setText(QtGui.QApplication.translate("widgetSource", "Label for installation source about PaWn", None, QtGui.QApplication.UnicodeUTF8))
        self.optInternet.setText(QtGui.QApplication.translate("widgetSource", "Download Pardus from Internet (recommended)", None, QtGui.QApplication.UnicodeUTF8))
        self.optCD.setText(QtGui.QApplication.translate("widgetSource", "I have Pardus installation CD", None, QtGui.QApplication.UnicodeUTF8))
        self.optISO.setText(QtGui.QApplication.translate("widgetSource", "I have Pardus installation file (.ISO)", None, QtGui.QApplication.UnicodeUTF8))


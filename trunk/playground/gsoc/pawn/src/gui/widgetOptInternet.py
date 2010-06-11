# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './widgetOptInternet.ui'
#
# Created: Fri Jun 11 02:42:43 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_widgetOptInternet(object):
    def setupUi(self, widgetOptInternet):
        widgetOptInternet.setObjectName("widgetOptInternet")
        widgetOptInternet.resize(452, 232)
        self.formLayoutWidget = QtGui.QWidget(widgetOptInternet)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 421, 114))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.lblChoose = QtGui.QLabel(self.formLayoutWidget)
        self.lblChoose.setObjectName("lblChoose")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblChoose)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboVersion = QtGui.QComboBox(self.formLayoutWidget)
        self.comboVersion.setObjectName("comboVersion")
        self.horizontalLayout_2.addWidget(self.comboVersion)
        self.lblSize = QtGui.QLabel(self.formLayoutWidget)
        self.lblSize.setObjectName("lblSize")
        self.horizontalLayout_2.addWidget(self.lblSize)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.mirrorLabel = QtGui.QLabel(self.formLayoutWidget)
        self.mirrorLabel.setObjectName("mirrorLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.mirrorLabel)
        self.comboMirror = QtGui.QComboBox(self.formLayoutWidget)
        self.comboMirror.setObjectName("comboMirror")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboMirror)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnUpdate = QtGui.QPushButton(self.formLayoutWidget)
        self.btnUpdate.setObjectName("btnUpdate")
        self.horizontalLayout_3.addWidget(self.btnUpdate)
        self.btnProxy1 = QtGui.QPushButton(self.formLayoutWidget)
        self.btnProxy1.setObjectName("btnProxy1")
        self.horizontalLayout_3.addWidget(self.btnProxy1)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.lblVersion = QtGui.QLabel(self.formLayoutWidget)
        self.lblVersion.setObjectName("lblVersion")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblVersion)
        self.horizontalLayoutWidget = QtGui.QWidget(widgetOptInternet)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 180, 421, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnCheck = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnCheck.setObjectName("btnCheck")
        self.horizontalLayout.addWidget(self.btnCheck)
        self.btnProxy2 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnProxy2.setObjectName("btnProxy2")
        self.horizontalLayout.addWidget(self.btnProxy2)
        self.lblDescription = QtGui.QLabel(widgetOptInternet)
        self.lblDescription.setGeometry(QtCore.QRect(10, 130, 421, 41))
        self.lblDescription.setWordWrap(True)
        self.lblDescription.setObjectName("lblDescription")

        self.retranslateUi(widgetOptInternet)
        QtCore.QMetaObject.connectSlotsByName(widgetOptInternet)

    def retranslateUi(self, widgetOptInternet):
        self.lblChoose.setText(QtGui.QApplication.translate("widgetOptInternet", "Version:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSize.setText(QtGui.QApplication.translate("widgetOptInternet", " MB", None, QtGui.QApplication.UnicodeUTF8))
        self.mirrorLabel.setText(QtGui.QApplication.translate("widgetOptInternet", "Mirror:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpdate.setText(QtGui.QApplication.translate("widgetOptInternet", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.btnProxy1.setText(QtGui.QApplication.translate("widgetOptInternet", "Set Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVersion.setText(QtGui.QApplication.translate("widgetOptInternet", "Version List:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCheck.setText(QtGui.QApplication.translate("widgetOptInternet", "Check Compatibility", None, QtGui.QApplication.UnicodeUTF8))
        self.btnProxy2.setText(QtGui.QApplication.translate("widgetOptInternet", "Set Proxy For Download", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDescription.setText(QtGui.QApplication.translate("widgetOptInternet", "You are about to download Pardus from Internet. Make sure that you are connected to Internet.", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon Sep 13 01:17:26 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(355, 186)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(110)
        sizePolicy.setVerticalStretch(110)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 146, 341, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(148, 25, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_create = QtGui.QPushButton(self.layoutWidget)
        self.button_create.setObjectName("button_create")
        self.horizontalLayout.addWidget(self.button_create)
        self.button_cancel = QtGui.QPushButton(self.layoutWidget)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 20, 341, 121))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.groupBox = QtGui.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 351, 121))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget1 = QtGui.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(240, 30, 91, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_open = QtGui.QPushButton(self.layoutWidget1)
        self.button_open.setObjectName("button_open")
        self.verticalLayout.addWidget(self.button_open)
        self.select_disk = QtGui.QPushButton(self.layoutWidget1)
        self.select_disk.setObjectName("select_disk")
        self.verticalLayout.addWidget(self.select_disk)
        self.layoutWidget2 = QtGui.QWidget(self.groupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 30, 221, 71))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.lineEdit_2 = QtGui.QLineEdit(self.layoutWidget2)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEdit, self.button_open)
        Dialog.setTabOrder(self.button_open, self.lineEdit_2)
        Dialog.setTabOrder(self.lineEdit_2, self.select_disk)
        Dialog.setTabOrder(self.select_disk, self.button_create)
        Dialog.setTabOrder(self.button_create, self.button_cancel)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "mainwindow", None, QtGui.QApplication.UnicodeUTF8))
        self.button_create.setText(QtGui.QApplication.translate("Dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.button_cancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "pardUSB", None, QtGui.QApplication.UnicodeUTF8))
        self.button_open.setText(QtGui.QApplication.translate("Dialog", "Select ISO", None, QtGui.QApplication.UnicodeUTF8))
        self.select_disk.setText(QtGui.QApplication.translate("Dialog", "Select Disk", None, QtGui.QApplication.UnicodeUTF8))


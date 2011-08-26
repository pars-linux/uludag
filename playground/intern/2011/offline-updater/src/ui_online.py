# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_offline.ui'
#
# Created: Wed Aug 24 10:00:36 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Online(object):
    def setupUi(self, Online):
        Online.setObjectName(_fromUtf8("Online"))
        Online.resize(358, 306)
        self.gridLayout = QtGui.QGridLayout(Online)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pb_action = QtGui.QPushButton(Online)
        self.pb_action.setObjectName(_fromUtf8("pb_action"))
        self.gridLayout.addWidget(self.pb_action, 1, 1, 1, 3)
        self.le_path = QtGui.QLineEdit(Online)
        self.le_path.setObjectName(_fromUtf8("le_path"))
        self.gridLayout.addWidget(self.le_path, 0, 1, 1, 2)
        self.listWidget = QtGui.QListWidget(Online)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 2, 1, 1, 3)
        self.pb_help = QtGui.QPushButton(Online)
        self.pb_help.setObjectName(_fromUtf8("pb_help"))
        self.gridLayout.addWidget(self.pb_help, 4, 2, 1, 1)
        self.pb_close = QtGui.QPushButton(Online)
        self.pb_close.setObjectName(_fromUtf8("pb_close"))
        self.gridLayout.addWidget(self.pb_close, 4, 3, 1, 1)
        self.pb_path = QtGui.QPushButton(Online)
        self.pb_path.setObjectName(_fromUtf8("pb_path"))
        self.gridLayout.addWidget(self.pb_path, 0, 3, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Online)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lbl_file = QtGui.QLabel(Online)
        self.lbl_file.setObjectName(_fromUtf8("lbl_file"))
        self.horizontalLayout.addWidget(self.lbl_file)
        self.lbl_progress = QtGui.QLabel(Online)
        self.lbl_progress.setObjectName(_fromUtf8("lbl_progress"))
        self.horizontalLayout.addWidget(self.lbl_progress)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 3)

        self.retranslateUi(Online)
        QtCore.QMetaObject.connectSlotsByName(Online)

    def retranslateUi(self, Online):
        Online.setWindowTitle(QtGui.QApplication.translate("Online", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_action.setText(QtGui.QApplication.translate("Online", "İşleme Başla", None, QtGui.QApplication.UnicodeUTF8))
        self.le_path.setText(QtGui.QApplication.translate("Online", "/home/user/", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_help.setText(QtGui.QApplication.translate("Online", "Yardım", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_close.setText(QtGui.QApplication.translate("Online", "Kapat", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_path.setText(QtGui.QApplication.translate("Online", "Dizin Seç", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Online", "İndirme İşlemi:", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_file.setText(QtGui.QApplication.translate("Online", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_progress.setText(QtGui.QApplication.translate("Online", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

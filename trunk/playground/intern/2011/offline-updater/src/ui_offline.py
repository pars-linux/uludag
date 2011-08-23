# -*- coding: utf-8 -*-

# Offline implementation generated from reading ui file 'ui_main.ui'
#
# Created: Tue Aug 23 15:04:48 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Offline(object):
    def setupUi(self, Offline):
        Offline.setObjectName(_fromUtf8("Offline"))
        Offline.resize(418, 282)
        self.gridLayout = QtGui.QGridLayout(Offline)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rb_export = QtGui.QRadioButton(Offline)
        self.rb_export.setObjectName(_fromUtf8("rb_export"))
        self.gridLayout.addWidget(self.rb_export, 1, 2, 1, 1)
        self.rb_setup = QtGui.QRadioButton(Offline)
        self.rb_setup.setObjectName(_fromUtf8("rb_setup"))
        self.gridLayout.addWidget(self.rb_setup, 1, 3, 1, 1)
        self.line = QtGui.QFrame(Offline)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 2, 2, 1, 2)
        self.frame = QtGui.QFrame(Offline)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.le_path_export = QtGui.QLineEdit(self.frame)
        self.le_path_export.setObjectName(_fromUtf8("le_path_export"))
        self.gridLayout_2.addWidget(self.le_path_export, 2, 0, 1, 1)
        self.pb_path_export = QtGui.QPushButton(self.frame)
        self.pb_path_export.setObjectName(_fromUtf8("pb_path_export"))
        self.gridLayout_2.addWidget(self.pb_path_export, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 3, 2, 1, 2)
        self.line_2 = QtGui.QFrame(Offline)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 4, 2, 1, 2)
        self.frame_2 = QtGui.QFrame(Offline)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.le_path_setup = QtGui.QLineEdit(self.frame_2)
        self.le_path_setup.setObjectName(_fromUtf8("le_path_setup"))
        self.gridLayout_3.addWidget(self.le_path_setup, 1, 0, 1, 1)
        self.pb_path_setup = QtGui.QPushButton(self.frame_2)
        self.pb_path_setup.setObjectName(_fromUtf8("pb_path_setup"))
        self.gridLayout_3.addWidget(self.pb_path_setup, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 5, 2, 1, 2)
        self.pb_action = QtGui.QPushButton(Offline)
        self.pb_action.setObjectName(_fromUtf8("pb_action"))
        self.gridLayout.addWidget(self.pb_action, 6, 2, 1, 2)
        self.progressBar = QtGui.QProgressBar(Offline)
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 7, 2, 1, 2)
        self.pb_help = QtGui.QPushButton(Offline)
        self.pb_help.setObjectName(_fromUtf8("pb_help"))
        self.gridLayout.addWidget(self.pb_help, 8, 2, 1, 1)
        self.pb_close = QtGui.QPushButton(Offline)
        self.pb_close.setObjectName(_fromUtf8("pb_close"))
        self.gridLayout.addWidget(self.pb_close, 8, 3, 1, 1)
        

        self.retranslateUi(Offline)
        QtCore.QMetaObject.connectSlotsByName(Offline)

    def retranslateUi(self, Offline):
        Offline.setWindowTitle(QtGui.QApplication.translate("Offline", "Offline", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_export.setText(QtGui.QApplication.translate("Offline", "Paket Listesini Dışarı Aktar", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_setup.setText(QtGui.QApplication.translate("Offline", "Paketleri Kur", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Offline", "Paket Listesini Dışarı Aktar:", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_path_export.setText(QtGui.QApplication.translate("Offline", "Dizin Seç", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Offline", "Paketleri Kur:", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_path_setup.setText(QtGui.QApplication.translate("Offline", "Dizin Seç", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_help.setText(QtGui.QApplication.translate("Offline", "Yardım", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_close.setText(QtGui.QApplication.translate("Offline", "Kapat", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_action.setText(QtGui.QApplication.translate("Offline", "İşleme Başla", None, QtGui.QApplication.UnicodeUTF8))

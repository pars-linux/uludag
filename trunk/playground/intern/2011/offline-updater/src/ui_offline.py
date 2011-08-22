# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_offline.ui'
#
# Created: Wed Aug 17 10:48:30 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Offline(object):
    def setupUi(self, Offline):
        Offline.setObjectName(_fromUtf8("Offline"))
        Offline.resize(358, 306)
        self.gridLayout = QtGui.QGridLayout(Offline)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pb_action = QtGui.QPushButton(Offline)
        self.pb_action.setObjectName(_fromUtf8("pb_action"))
        self.gridLayout.addWidget(self.pb_action, 1, 1, 1, 3)
        self.progressBar = QtGui.QProgressBar(Offline)
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 1, 1, 3)
        self.le_path = QtGui.QLineEdit(Offline)
        self.le_path.setObjectName(_fromUtf8("le_path"))
        self.gridLayout.addWidget(self.le_path, 0, 1, 1, 2)
        self.listWidget = QtGui.QListWidget(Offline)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 2, 1, 1, 3)
        self.pb_help = QtGui.QPushButton(Offline)
        self.pb_help.setObjectName(_fromUtf8("pb_help"))
        self.gridLayout.addWidget(self.pb_help, 4, 2, 1, 1)
        self.pb_close = QtGui.QPushButton(Offline)
        self.pb_close.setObjectName(_fromUtf8("pb_close"))
        self.gridLayout.addWidget(self.pb_close, 4, 3, 1, 1)
        self.pb_path = QtGui.QPushButton(Offline)
        self.pb_path.setObjectName(_fromUtf8("pb_path"))
        self.gridLayout.addWidget(self.pb_path, 0, 3, 1, 1)

        self.retranslateUi(Offline)
        QtCore.QMetaObject.connectSlotsByName(Offline)

    def retranslateUi(self, Offline):
        Offline.setWindowTitle(QtGui.QApplication.translate("Offline", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_action.setText(QtGui.QApplication.translate("Offline", "İşleme Başla", None, QtGui.QApplication.UnicodeUTF8))
        self.le_path.setText(QtGui.QApplication.translate("Offline", "/home/user/", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_help.setText(QtGui.QApplication.translate("Offline", "Yardım", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_close.setText(QtGui.QApplication.translate("Offline", "Kapat", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_path.setText(QtGui.QApplication.translate("Offline", "Dizin Seç", None, QtGui.QApplication.UnicodeUTF8))
        
    def updateListWidget(self, message):
        item = QListWidgetItem(message)
        self.listWidget.addItem(message)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Offline = QtGui.QWidget()
    ui = Ui_Offline()
    ui.setupUi(Offline)
    Offline.show()
    sys.exit(app.exec_())

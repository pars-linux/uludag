# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fingerform.ui'
#
# Created: Fri Jul  4 13:34:32 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dialogFinger(object):
    def setupUi(self, dialogFinger):
        dialogFinger.setObjectName("dialogFinger")
        dialogFinger.resize(268,161)
        dialogFinger.setModal(True)
        self.horizontalLayout = QtGui.QHBoxLayout(dialogFinger)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.viewFinger = QtGui.QLabel(dialogFinger)
        self.viewFinger.setScaledContents(True)
        self.viewFinger.setAlignment(QtCore.Qt.AlignCenter)
        self.viewFinger.setObjectName("viewFinger")
        self.horizontalLayout.addWidget(self.viewFinger)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushEnroll = QtGui.QPushButton(dialogFinger)
        self.pushEnroll.setObjectName("pushEnroll")
        self.verticalLayout.addWidget(self.pushEnroll)
        self.pushErase = QtGui.QPushButton(dialogFinger)
        self.pushErase.setObjectName("pushErase")
        self.verticalLayout.addWidget(self.pushErase)
        self.pushVerify = QtGui.QPushButton(dialogFinger)
        self.pushVerify.setObjectName("pushVerify")
        self.verticalLayout.addWidget(self.pushVerify)
        self.pushClose = QtGui.QPushButton(dialogFinger)
        self.pushClose.setObjectName("pushClose")
        self.verticalLayout.addWidget(self.pushClose)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(dialogFinger)
        QtCore.QMetaObject.connectSlotsByName(dialogFinger)
        dialogFinger.setTabOrder(self.pushEnroll,self.pushErase)
        dialogFinger.setTabOrder(self.pushErase,self.pushVerify)

    def retranslateUi(self, dialogFinger):
        dialogFinger.setWindowTitle(QtGui.QApplication.translate("dialogFinger", "Parmak İzi Düzenleyici", None, QtGui.QApplication.UnicodeUTF8))
        self.viewFinger.setText(QtGui.QApplication.translate("dialogFinger", "Resim \n"
" Yok", None, QtGui.QApplication.UnicodeUTF8))
        self.pushEnroll.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzi Tanıt", None, QtGui.QApplication.UnicodeUTF8))
        self.pushErase.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzini Sil", None, QtGui.QApplication.UnicodeUTF8))
        self.pushVerify.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzini Dene", None, QtGui.QApplication.UnicodeUTF8))
        self.pushClose.setText(QtGui.QApplication.translate("dialogFinger", "Kapat", None, QtGui.QApplication.UnicodeUTF8))


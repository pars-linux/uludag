# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fingerform.ui'
#
# Created: Mon Jun 30 09:22:40 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dialogFinger(object):
    def setupUi(self, dialogFinger):
        dialogFinger.setObjectName("dialogFinger")
        dialogFinger.resize(303,164)
        dialogFinger.setModal(True)
        self.horizontalLayout = QtGui.QHBoxLayout(dialogFinger)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.viewFinger = QtGui.QGraphicsView(dialogFinger)
        self.viewFinger.setFocusPolicy(QtCore.Qt.NoFocus)
        self.viewFinger.setInteractive(False)
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
        self.buttonBox = QtGui.QDialogButtonBox(dialogFinger)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(dialogFinger)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),dialogFinger.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),dialogFinger.reject)
        QtCore.QMetaObject.connectSlotsByName(dialogFinger)
        dialogFinger.setTabOrder(self.pushEnroll,self.pushErase)
        dialogFinger.setTabOrder(self.pushErase,self.pushVerify)
        dialogFinger.setTabOrder(self.pushVerify,self.buttonBox)

    def retranslateUi(self, dialogFinger):
        dialogFinger.setWindowTitle(QtGui.QApplication.translate("dialogFinger", "Parmak İzi Düzenleyici", None, QtGui.QApplication.UnicodeUTF8))
        self.pushEnroll.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzi Tanıt", None, QtGui.QApplication.UnicodeUTF8))
        self.pushErase.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzini Sil", None, QtGui.QApplication.UnicodeUTF8))
        self.pushVerify.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzini Dene", None, QtGui.QApplication.UnicodeUTF8))


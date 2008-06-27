# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fingerform.ui'
#
# Created: Fri Jun 27 14:47:53 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dialogFinger(object):
    def setupUi(self, dialogFinger):
        dialogFinger.setObjectName("dialogFinger")
        dialogFinger.resize(355,215)
        dialogFinger.setModal(True)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(dialogFinger)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.viewFinger = QtGui.QGraphicsView(dialogFinger)
        self.viewFinger.setFocusPolicy(QtCore.Qt.NoFocus)
        self.viewFinger.setInteractive(False)
        self.viewFinger.setObjectName("viewFinger")
        self.horizontalLayout_2.addWidget(self.viewFinger)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelFinger = QtGui.QLabel(dialogFinger)
        self.labelFinger.setObjectName("labelFinger")
        self.horizontalLayout.addWidget(self.labelFinger)
        self.comboFinger = QtGui.QComboBox(dialogFinger)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboFinger.sizePolicy().hasHeightForWidth())
        self.comboFinger.setSizePolicy(sizePolicy)
        self.comboFinger.setObjectName("comboFinger")
        self.horizontalLayout.addWidget(self.comboFinger)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushEnroll = QtGui.QPushButton(dialogFinger)
        self.pushEnroll.setObjectName("pushEnroll")
        self.verticalLayout.addWidget(self.pushEnroll)
        self.pushErase = QtGui.QPushButton(dialogFinger)
        self.pushErase.setObjectName("pushErase")
        self.verticalLayout.addWidget(self.pushErase)
        self.pushVerify = QtGui.QPushButton(dialogFinger)
        self.pushVerify.setObjectName("pushVerify")
        self.verticalLayout.addWidget(self.pushVerify)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(dialogFinger)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.labelFinger.setBuddy(self.comboFinger)

        self.retranslateUi(dialogFinger)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),dialogFinger.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),dialogFinger.reject)
        QtCore.QMetaObject.connectSlotsByName(dialogFinger)
        dialogFinger.setTabOrder(self.comboFinger,self.pushEnroll)
        dialogFinger.setTabOrder(self.pushEnroll,self.pushErase)
        dialogFinger.setTabOrder(self.pushErase,self.pushVerify)
        dialogFinger.setTabOrder(self.pushVerify,self.buttonBox)

    def retranslateUi(self, dialogFinger):
        dialogFinger.setWindowTitle(QtGui.QApplication.translate("dialogFinger", "Parmak İzi Düzenleyici", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFinger.setText(QtGui.QApplication.translate("dialogFinger", "Parmak:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboFinger.addItem(QtGui.QApplication.translate("dialogFinger", "Sağ Orta Parmak", None, QtGui.QApplication.UnicodeUTF8))
        self.comboFinger.addItem(QtGui.QApplication.translate("dialogFinger", "Sağ İşaret Parmağı", None, QtGui.QApplication.UnicodeUTF8))
        self.pushEnroll.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzi Tanıt", None, QtGui.QApplication.UnicodeUTF8))
        self.pushErase.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzini Sil", None, QtGui.QApplication.UnicodeUTF8))
        self.pushVerify.setText(QtGui.QApplication.translate("dialogFinger", "Parmak İzini Dene", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'swipeform.ui'
#
# Created: Mon Jul  7 10:30:26 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dialogSwipe(object):
    def setupUi(self, dialogSwipe):
        dialogSwipe.setObjectName("dialogSwipe")
        dialogSwipe.resize(177,61)
        dialogSwipe.setSizeGripEnabled(False)
        dialogSwipe.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(dialogSwipe)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelSwipe = QtGui.QLabel(dialogSwipe)
        self.labelSwipe.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSwipe.setWordWrap(True)
        self.labelSwipe.setObjectName("labelSwipe")
        self.verticalLayout.addWidget(self.labelSwipe)

        self.retranslateUi(dialogSwipe)
        QtCore.QMetaObject.connectSlotsByName(dialogSwipe)

    def retranslateUi(self, dialogSwipe):
        dialogSwipe.setWindowTitle(QtGui.QApplication.translate("dialogSwipe", "Swipe!", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSwipe.setText(QtGui.QApplication.translate("dialogSwipe", "Please swipe your finger!", None, QtGui.QApplication.UnicodeUTF8))


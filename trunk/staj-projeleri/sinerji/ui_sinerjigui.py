# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './sinerjigui.ui'
#
# Created: Sun Aug 31 12:54:07 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SinerjiGui(object):
    def setupUi(self, SinerjiGui):
        SinerjiGui.setObjectName("SinerjiGui")
        SinerjiGui.resize(406, 329)
        self.gridLayout_2 = QtGui.QGridLayout(SinerjiGui)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtGui.QFrame(SinerjiGui)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.topComboBox = QtGui.QComboBox(self.frame)
        self.topComboBox.setObjectName("topComboBox")
        self.gridLayout.addWidget(self.topComboBox, 0, 1, 1, 1)
        self.leftComboBox = QtGui.QComboBox(self.frame)
        self.leftComboBox.setObjectName("leftComboBox")
        self.gridLayout.addWidget(self.leftComboBox, 1, 0, 1, 1)
        self.rightComboBox = QtGui.QComboBox(self.frame)
        self.rightComboBox.setObjectName("rightComboBox")
        self.gridLayout.addWidget(self.rightComboBox, 1, 2, 1, 1)
        self.bottomComboBox = QtGui.QComboBox(self.frame)
        self.bottomComboBox.setObjectName("bottomComboBox")
        self.gridLayout.addWidget(self.bottomComboBox, 2, 1, 1, 1)
        self.icobLabel = QtGui.QLabel(self.frame)
        self.icobLabel.setPixmap(QtGui.QPixmap("style.png"))
        self.icobLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.icobLabel.setObjectName("icobLabel")
        self.gridLayout.addWidget(self.icobLabel, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 3)
        self.savequitButton = QtGui.QPushButton(SinerjiGui)
        self.savequitButton.setObjectName("savequitButton")
        self.gridLayout_2.addWidget(self.savequitButton, 2, 1, 1, 1)
        self.cancelButton = QtGui.QPushButton(SinerjiGui)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.serverBox = QtGui.QCheckBox(SinerjiGui)
        self.serverBox.setObjectName("serverBox")
        self.gridLayout_2.addWidget(self.serverBox, 0, 0, 1, 1)
        self.clientBox = QtGui.QCheckBox(SinerjiGui)
        self.clientBox.setChecked(True)
        self.clientBox.setObjectName("clientBox")
        self.gridLayout_2.addWidget(self.clientBox, 0, 1, 1, 1)

        self.retranslateUi(SinerjiGui)
        QtCore.QMetaObject.connectSlotsByName(SinerjiGui)

    def retranslateUi(self, SinerjiGui):
        SinerjiGui.setWindowTitle(QtGui.QApplication.translate("SinerjiGui", "Sinerji", None, QtGui.QApplication.UnicodeUTF8))
        self.savequitButton.setText(QtGui.QApplication.translate("SinerjiGui", "Save and Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("SinerjiGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.serverBox.setText(QtGui.QApplication.translate("SinerjiGui", "I want to share", None, QtGui.QApplication.UnicodeUTF8))
        self.clientBox.setText(QtGui.QApplication.translate("SinerjiGui", "I want to be shared", None, QtGui.QApplication.UnicodeUTF8))


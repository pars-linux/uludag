# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './sinerjigui.ui'
#
# Created: Thu Sep  4 09:26:53 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SinerjiGui(object):
    def setupUi(self, SinerjiGui):
        SinerjiGui.setObjectName("SinerjiGui")
        SinerjiGui.resize(389, 365)
        self.gridLayout_2 = QtGui.QGridLayout(SinerjiGui)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.serverButton = QtGui.QRadioButton(SinerjiGui)
        self.serverButton.setObjectName("serverButton")
        self.gridLayout_2.addWidget(self.serverButton, 0, 0, 1, 1)
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
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 4)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 2)
        self.savequitButton = QtGui.QPushButton(SinerjiGui)
        self.savequitButton.setObjectName("savequitButton")
        self.gridLayout_2.addWidget(self.savequitButton, 2, 2, 1, 1)
        self.cancelButton = QtGui.QPushButton(SinerjiGui)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_2.addWidget(self.cancelButton, 2, 3, 1, 1)
        self.clientButton = QtGui.QRadioButton(SinerjiGui)
        self.clientButton.setObjectName("clientButton")
        self.gridLayout_2.addWidget(self.clientButton, 0, 2, 1, 1)

        self.retranslateUi(SinerjiGui)
        QtCore.QMetaObject.connectSlotsByName(SinerjiGui)

    def retranslateUi(self, SinerjiGui):
        SinerjiGui.setWindowTitle(QtGui.QApplication.translate("SinerjiGui", "Sinerji", None, QtGui.QApplication.UnicodeUTF8))
        self.serverButton.setText(QtGui.QApplication.translate("SinerjiGui", "Server Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.savequitButton.setText(QtGui.QApplication.translate("SinerjiGui", "Save and Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("SinerjiGui", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.clientButton.setText(QtGui.QApplication.translate("SinerjiGui", "Client Mode", None, QtGui.QApplication.UnicodeUTF8))


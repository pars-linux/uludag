# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './sinerjigui.ui'
#
# Created: Mon Sep 15 10:36:30 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SinerjiGui(object):
    def setupUi(self, SinerjiGui):
        SinerjiGui.setObjectName("SinerjiGui")
        SinerjiGui.resize(413, 374)
        self.gridLayout_2 = QtGui.QGridLayout(SinerjiGui)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(SinerjiGui)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
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
        self.icobLabel.setPixmap(QtGui.QPixmap("images/icon.png"))
        self.icobLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.icobLabel.setObjectName("icobLabel")
        self.gridLayout.addWidget(self.icobLabel, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(189, 27, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.applyButton = QtGui.QPushButton(SinerjiGui)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/buttonOk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.applyButton.setIcon(icon)
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout.addWidget(self.applyButton)
        self.closeButton = QtGui.QPushButton(SinerjiGui)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/buttonCancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon1)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(SinerjiGui)
        QtCore.QMetaObject.connectSlotsByName(SinerjiGui)

    def retranslateUi(self, SinerjiGui):
        SinerjiGui.setWindowTitle(QtGui.QApplication.translate("SinerjiGui", "Sinerji", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SinerjiGui", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#333333;\">Yönetmek istediğiniz bilgisayarı ve fiziksel konumunu seçin</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("SinerjiGui", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("SinerjiGui", "Close", None, QtGui.QApplication.UnicodeUTF8))


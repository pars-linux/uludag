# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './sinerjigui.ui'
#
# Created: Tue Sep 16 09:30:27 2008
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
        self.label.setText(QtGui.QApplication.translate("SinerjiGui", "<b>" + _("Choose the computer and his position to manage it") + "</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.applyButton.setText(QtGui.QApplication.translate("SinerjiGui", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("SinerjiGui", "Close", None, QtGui.QApplication.UnicodeUTF8))


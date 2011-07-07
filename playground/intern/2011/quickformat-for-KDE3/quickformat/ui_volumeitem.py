#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from ui/volumeitem.ui on Fri Jul  1 13:15:54 2011
#
# WARNING! All changes to this file will be lost.
#from PyKDE4 import kdecore
#from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VolumeItem(object):
    def setupUi(self, VolumeItem):
        VolumeItem.setObjectName(_fromUtf8("VolumeItem"))
        VolumeItem.resize(300, 70)
        VolumeItem.setMinimumSize(QtCore.QSize(300, 70))
        VolumeItem.setMaximumSize(QtCore.QSize(300, 70))
        VolumeItem.setWindowTitle(_fromUtf8("Form"))
        VolumeItem.setAutoFillBackground(False)
        VolumeItem.setStyleSheet(_fromUtf8("#VolumeItem QLabel {\n"
"        color: #222222;\n"
"}\n"
"#frame{background-color: white}\n"
"#frame:hover{background-color: qlineargradient(spread:pad, x1:0.519597, y1:1, x2:0.518067, y2:0, stop:0 rgba(189, 189, 189, 255), stop:1 rgba(225, 225, 225, 255))}\n"
""))
        self.horizontalLayout = QtGui.QHBoxLayout(VolumeItem)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(VolumeItem)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setMargin(10)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.name = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.name.setFont(font)
        self.name.setToolTip(_fromUtf8(""))
        self.name.setText(_fromUtf8("Brand USB Storage Device"))
        self.name.setObjectName(_fromUtf8("name"))
        self.horizontalLayout_2.addWidget(self.name)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 1, 1, 2)
        self.icon = QtGui.QLabel(self.frame)
        self.icon.setMinimumSize(QtCore.QSize(48, 48))
        self.icon.setMaximumSize(QtCore.QSize(48, 48))
        self.icon.setText(_fromUtf8(""))
        self.icon.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/media-flash-sd-mmc.png")))
        self.icon.setScaledContents(True)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.gridLayout.addWidget(self.icon, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setToolTip(_fromUtf8(""))
        self.label.setText(_fromUtf8("label"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.path = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setWeight(50)
        font.setBold(False)
        self.path.setFont(font)
        self.path.setToolTip(_fromUtf8(""))
        self.path.setText(_fromUtf8("sdaX"))
        self.path.setObjectName(_fromUtf8("path"))
        self.horizontalLayout_3.addWidget(self.path)
        self.label_3 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.format = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.format.setFont(font)
        self.format.setToolTip(_fromUtf8(""))
        self.format.setText(_fromUtf8("ext4"))
        self.format.setObjectName(_fromUtf8("format"))
        self.horizontalLayout_3.addWidget(self.format)
        self.label_2 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setWeight(50)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.size = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.size.setFont(font)
        self.size.setToolTip(_fromUtf8(""))
        self.size.setText(_fromUtf8("1mb"))
        self.size.setObjectName(_fromUtf8("size"))
        self.horizontalLayout_3.addWidget(self.size)
        self.device = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.device.setFont(font)
        self.device.setToolTip(_fromUtf8(""))
        self.device.setText(_fromUtf8("*hidden"))
        self.device.setObjectName(_fromUtf8("device"))
        self.horizontalLayout_3.addWidget(self.device)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 1, 1, 2)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(VolumeItem)
        QtCore.QMetaObject.connectSlotsByName(VolumeItem)

    def retranslateUi(self, VolumeItem):
        self.label_3.setText(":")
        self.label_2.setText("-")

import images_rc

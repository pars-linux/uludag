# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_detailWidget.ui'
#
# Created: Thu Aug 11 08:37:00 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InfoWidget(object):
    def setupUi(self, InfoWidget):
        InfoWidget.setObjectName(_fromUtf8("InfoWidget"))
        InfoWidget.resize(422, 308)
        InfoWidget.setMinimumSize(QtCore.QSize(0, 48))
        self.gridLayout = QtGui.QGridLayout(InfoWidget)
        self.gridLayout.setContentsMargins(8, -1, 8, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.description = QtGui.QLabel(InfoWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setStyleSheet(_fromUtf8("QLabel#description { color:white; }"))
        self.description.setWordWrap(True)
        self.description.setObjectName(_fromUtf8("description"))
        self.gridLayout.addWidget(self.description, 0, 0, 1, 1)
        self.buttonHide = QtGui.QPushButton(InfoWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonHide.sizePolicy().hasHeightForWidth())
        self.buttonHide.setSizePolicy(sizePolicy)
        self.buttonHide.setMaximumSize(QtCore.QSize(36, 16777215))
        self.buttonHide.setText(_fromUtf8(""))
        self.buttonHide.setFlat(False)
        self.buttonHide.setObjectName(_fromUtf8("buttonHide"))
        self.gridLayout.addWidget(self.buttonHide, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(308, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        self.retranslateUi(InfoWidget)
        QtCore.QMetaObject.connectSlotsByName(InfoWidget)

    def retranslateUi(self, InfoWidget):
        InfoWidget.setWindowTitle(QtGui.QApplication.translate("InfoWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.description.setText(QtGui.QApplication.translate("InfoWidget", "Service information is not available", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonHide.setToolTip(QtGui.QApplication.translate("InfoWidget", "Hide Information", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    InfoWidget = QtGui.QWidget()
    ui = Ui_InfoWidget()
    ui.setupUi(InfoWidget)
    InfoWidget.show()
    sys.exit(app.exec_())


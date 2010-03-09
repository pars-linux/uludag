# -*- coding: utf-8 -*-
import time

from PyQt4 import QtCore, QtGui
from qticonloader import *

class Ui_Test(object):
    def setupUi(self, Test):
        Test.setObjectName("Test")
        Test.resize(460, 300)
        self.gridLayout = QtGui.QGridLayout(Test)
        self.gridLayout.setObjectName("gridLayout")
        self.name = QtGui.QLineEdit(Test)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 0, 1, 1)
        self.size = QtGui.QComboBox(Test)
        self.size.setObjectName("size")
        self.size.addItem("16")
        self.size.addItem("22")
        self.size.addItem("32")
        self.size.addItem("48")
        self.size.addItem("64")
        self.size.addItem("128")
        self.gridLayout.addWidget(self.size, 0, 1, 1, 1)
        self.getButton = QtGui.QPushButton(Test)
        self.getButton.setText("Get Icon")
        self.gridLayout.addWidget(self.getButton, 0, 2, 1, 1)
        self.label = QtGui.QLabel(Test)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 3)
        self.getButton.clicked.connect(self.showIcon)
        QtCore.QMetaObject.connectSlotsByName(Test)
        self.loader = QIconLoader(debug = False)

        print "Desktop Session : ", self.loader.desktopSession
        print "Desktop Version : ", self.loader.desktopVersion
        print "Theme : ", self.loader.themeName

    def showIcon(self):
        icons = unicode(self.name.text())
        self.label.setPixmap(self.loader.load(icons.split(','), self.size.currentText()))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Test = QtGui.QWidget()
    ui = Ui_Test()
    ui.setupUi(Test)
    Test.show()
    sys.exit(app.exec_())


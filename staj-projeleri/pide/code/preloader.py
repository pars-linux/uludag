#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python

# progressbar.py

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from ui_progressbar import Ui_MainWindow

class ProgressBar(QtGui.QWidget, Ui_MainWindow):
    def __init__(self, fileSize, transferSize):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

        self.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.onStart)
        self.timer = QtCore.QBasicTimer()
        self.step = 0;

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.incVal = (self.transferSize*100)/self.fileSize
        self.step = self.step + self.incVal
        self.progressBar.setValue(self.step)

    def onStart(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pushButton.setText('Continue')
            self.label.setText("Stopped!")
        else:
            self.timer.start(100, self)
            self.pushButton.setText('Stop')
            self.label.setText("Sending...")



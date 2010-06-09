from gui.stepTemplate import StepWidget
from PyQt4 import QtGui

from gui.widgetSource import Ui_widgetSource

class Widget(QtGui.QWidget, StepWidget):
    heading = "Select the source"

    def __init__(self):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self)

	self.gui = Ui_widgetSource()
	self.gui.setupUi(self)


    def nextIndex(self):
	print 'THIS IS SPARTAAAAAAAAAAAA!!!'
	return -1

    def isFinishStep(self):
	return True
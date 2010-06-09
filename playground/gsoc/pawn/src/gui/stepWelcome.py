from gui.stepTemplate import StepWidget
from PyQt4 import QtGui

from gui.widgetWelcome import Ui_widgetWelcome

class Widget(QtGui.QWidget, StepWidget):
    heading = "Welcome to PaWn"

    def __init__(self):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self)

	self.gui = Ui_widgetWelcome()
	self.gui.setupUi(self)


    def nextIndex(self):
	return 1
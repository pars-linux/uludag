from gui.stepTemplate import StepWidget
from PyQt4 import QtGui

from gui.widgetOptCD import Ui_widgetOptCD

class Widget(QtGui.QWidget, StepWidget):
    heading = "Show Your CD/DVD Path"

    def __init__(self):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self)

	self.gui = Ui_widgetOptCD()
	self.gui.setupUi(self)


    def nextIndex(self):
	return 0 # TODO: implement

    def onSubmit(self):
	return false # TODO: implement
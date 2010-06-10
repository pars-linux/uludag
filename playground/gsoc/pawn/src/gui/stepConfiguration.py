from gui.stepTemplate import StepWidget
from PyQt4 import QtGui

from gui.widgetConfiguration import Ui_widgetConfiguration

class Widget(QtGui.QWidget, StepWidget):
    heading = "Configure Your Pardus"

    def __init__(self):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self)

	self.gui = Ui_widgetConfiguration()
	self.gui.setupUi(self)

    def nextIndex(self):
	return 2 # TODO: implement

    def onSubmit(self):
	return True # TODO: implement checks
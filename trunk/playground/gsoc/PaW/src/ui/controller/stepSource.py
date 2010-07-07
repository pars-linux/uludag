from PyQt4 import QtGui
from ui.controller.stepTemplate import StepWidget
from ui.gui.source import Ui_source

class Widget(QtGui.QWidget, StepWidget):
    heading = "Choose the source"

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_source()
	self.gui.setupUi(self)
	
	self.options = [self.gui.optInternet, self.gui.optISO,
            self.gui.optCD, self.gui.optUSB]

    def nextIndex(self):
	if self.gui.optISO.isChecked():
	    return 3
	if self.gui.optCD.isChecked():
	    return 4
	if self.gui.optInternet.isChecked():
	    return 5
        if self.gui.optUSB.isChecked():
	    return 6

	return 0 # TODO: implement other interfaces

    def onSubmit(self):
	for option in self.options:
	    if option.isChecked():
		return True

	error = QtGui.QMessageBox(self)
	error.setWindowTitle("Warning")
	error.setText("Please choose an option to proceed.")
	error.show()
	return False

    def onRollback(self):
	for option in self.options:
	    option.setChecked(False) # TODO: Does not work LOL

	return True
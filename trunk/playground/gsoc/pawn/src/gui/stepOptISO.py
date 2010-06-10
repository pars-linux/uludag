from gui.stepTemplate import StepWidget
from PyQt4 import QtGui, QtCore

from gui.widgetOptISO import Ui_widgetOptISO

class Widget(QtGui.QWidget, StepWidget):
    heading = "Choose ISO File"

    def __init__(self):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self)

	self.gui = Ui_widgetOptISO()
	self.gui.setupUi(self)

	self.fileName = ''
	QtCore.QObject.connect(self.gui.btnBrowse, QtCore.SIGNAL('clicked()'), self.openFileDialog)
	QtCore.QObject.connect(self.gui.txtFileName, QtCore.SIGNAL('clicked()'), self.openFileDialog)

    def openFileDialog(self):
	fileDialog =QtGui.QFileDialog()
	fileDialog.setNameFilter('*.iso') # Does not work!
	self.fileName = fileDialog.getOpenFileName(self, 'Open ISO File')

	self.onFileUpdated()

    def onFileUpdated(self):
	self.gui.txtFileName.setText(self.fileName)

    def onSubmit(self):
	if not self.fileName:
	    error = QtGui.QMessageBox(self)
	    error.setWindowTitle("Warning")
	    error.setText("Please choose an ISO file (*.iso) to proceed.")
	    error.show()
	    return False
	else:
	    return True

    def nextIndex(self):
	return 0
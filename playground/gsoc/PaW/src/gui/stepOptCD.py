from gui.stepTemplate import StepWidget
from PyQt4 import QtGui,QtCore

from gui.widgetOptCD import Ui_widgetOptCD

class Widget(QtGui.QWidget, StepWidget):
    heading = "Show Your CD/DVD Path"

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_widgetOptCD()
	self.gui.setupUi(self)

	self.cdPath = ''
	QtCore.QObject.connect(self.gui.btnBrowse, QtCore.SIGNAL('clicked()'), self.openFileDialog)
	

    def openFileDialog(self):
	fileDialog =QtGui.QFileDialog()
	self.cdPath = fileDialog.getExistingDirectory(self, 'Select CD Drive or Folder')

	self.onPathUpdated()

    def onPathUpdated(self):
	self.gui.txtPath.setText(self.cdPath)

    def onSubmit(self):
	if not self.cdPath:
	    QtGui.QMessageBox.warning(self, 'Warning', 'Please choose Pardus CD drive or folder to proceed.', QtGui.QMessageBox.Ok)
	    return False
	else:
	    return True

    def nextIndex(self):
	return 0
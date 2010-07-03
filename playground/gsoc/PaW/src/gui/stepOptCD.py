import os

from gui.stepTemplate import StepWidget
from PyQt4 import QtGui

from gui.widgetOptCD import Ui_widgetOptCD

class Widget(QtGui.QWidget, StepWidget):
    heading = "Show Your CD/DVD Path"
    cd = None

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_widgetOptCD()
	self.gui.setupUi(self)

	self.populateCDs()

    def openFileDialog(self):
	fileDialog =QtGui.QFileDialog()
	self.cdPath = fileDialog.getExistingDirectory(self, 'Select CD Drive or Folder')

	self.onPathUpdated()

    def onPathUpdated(self):
	self.gui.txtPath.setText(self.cdPath)

    def populateCDs(self):
	self.gui.comboDrive.clear()
	for cd in self.mainEngine.compatibility.cds:
	    self.gui.comboDrive.addItem('%s %s' %(cd.DeviceID, cd.Name))

    def getSelectedCDDrive(self):
	for cd in self.mainEngine.compatibility.cds:
	    if cd.DeviceID == self.gui.comboDrive.currentText()[:2]:
                # TODO: TBD: First 2 letters of combobox is drive letter+colon.
                # This may fail in the future.
		return cd
	return None

    def isEmptyDrive(self, CD):
        """
        Returns False if CD root is accessible.
        True if any IO, Permission errors occur. That means CD is not readable.
        """
        try:
            print CD.DeviceID
            return not isinstance(os.listdir(CD.DeviceID),list) # check i.e. f:\
        except WindowsError, IOError:
            return True

    def onSubmit(self):
	currentDrive = self.getSelectedCDDrive()

        if not currentDrive:
	    QtGui.QMessageBox.warning(self, 'Warning', 'Please choose Pardus CD drive or folder to proceed.', QtGui.QMessageBox.Ok)
	    return False
        elif self.isEmptyDrive(currentDrive):
            QtGui.QMessageBox.warning(self, 'Could not read CD/DVD', 'You do not have CD/DVD in %s or drive is not ready. If you have a working CD/DVD in it, please try again.' % currentDrive.DeviceID, QtGui.QMessageBox.Ok)
            return False
	else:
            self.mainEngine.config.cdDrive = self.getSelectedCDDrive()
	    return True

    def nextIndex(self):
	return 0

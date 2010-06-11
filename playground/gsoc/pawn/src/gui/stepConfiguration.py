from gui.stepTemplate import StepWidget
from PyQt4 import QtGui,QtCore

from gui.widgetConfiguration import Ui_widgetConfiguration

class Widget(QtGui.QWidget, StepWidget):
    heading = "Configure Your Pardus"

    defaultSize = 5
    minSize = 3

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_widgetConfiguration()
	self.gui.setupUi(self)
	self.connect(self.gui.comboDrive, QtCore.SIGNAL('currentIndexChanged(int)'), self.driveChanged)
	self.connect(self.gui.sizeSlider, QtCore.SIGNAL('valueChanged(int)'), self.sizeChanged)
	
	self.mainEngine = mainEngine
	self.populateDrives()

    def driveChanged(self, index):
	free = self.freeSpaceOnDrive()
	self.gui.lblDriveFreeSpace.setText('%d GB Free' % free)

	self.updateSliderRange()
	self.updateProgressBarRange()


    def sizeChanged(self, value):
	free = self.freeSpaceOnDrive()
	value = self.gui.sizeSlider.value()
	freeLeft = free-value
	
	self.gui.pbFreeSpace.setValue(free+value)
	self.gui.lblFreeLeft.setText('%d GB Free' % freeLeft)
	self.gui.lblSize.setText('%d GB' % self.gui.sizeSlider.value())
	

    def updateSliderRange(self):
	free = self.freeSpaceOnDrive()

	self.gui.sizeSlider.setMinimum(self.minSize)
	self.gui.sizeSlider.setMaximum(free)
	self.gui.sizeSlider.setValue(self.defaultSize)

    def updateProgressBarRange(self):
	total = self.totalSpaceOnDrive()

	self.gui.pbFreeSpace.setMinimum(0)
	self.gui.pbFreeSpace.setMaximum(total)

    def freeSpaceOnDrive(self):
	return 30 # TODO: !

    def totalSpaceOnDrive(self):
	return 100 # TODO: !

    def populateDrives(self):
	drives = ['C:', 'D:', 'E:']

	self.gui.comboDrive.clear()
	for drive in drives:
	    self.gui.comboDrive.addItem(drive)

    def onEnter(self):
	self.gui.txtPassword.setText('')
	self.gui.txtRetypePassword.setText('')
	self.mainEngine.password = None

    def onSubmit(self):
	# TODO: 'Not enough free space' warnings
	errorText = ''

	username = self.gui.txtUsername.text()
	password = self.gui.txtPassword.text()
	retypePassword = self.gui.txtRetypePassword.text()

	if not username:  # TODO: other limitations?
	    errorText += 'Please enter a username.\n'

	if not password:
	    errorText += 'Please enter a password.\n'

	if not retypePassword :
	    errorText += 'Please retype the password.\n'
	else:
	    if password != retypePassword:
		errorText += 'Passwords do not match. Be careful.'

	if errorText:
	    error = QtGui.QMessageBox(self)
	    error.setWindowTitle("Warning")
	    error.setText(errorText)
	    error.show()
	    return False

	self.mainEngine.config.username = username
	self.mainEngine.config.password = password
	# TODO: config size and drive
	return True


    def nextIndex(self):
	return 2 # TODO: implement better
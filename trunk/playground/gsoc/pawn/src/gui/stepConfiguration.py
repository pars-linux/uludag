import math
from gui.stepTemplate import StepWidget
from utils import humanReadableSize
from PyQt4 import QtGui,QtCore

from gui.widgetConfiguration import Ui_widgetConfiguration

class Widget(QtGui.QWidget, StepWidget):
    heading = "Configure Your Pardus"

    defaultSize = long(5*1024*1024*1024)
    minSize = long(1.5*1024*1024*1024)

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
	h=humanReadableSize
	free = self.freeSpaceOnDrive()
	total = self.totalSpaceOnDrive()
	self.gui.lblDriveFreeSpace.setText('%s free' % (humanReadableSize(free)))

	self.updateProgressBarRange()

	percentage = math.floor((self.defaultSize-self.minSize)*100/(free-self.minSize)*1.0)

	self.gui.sizeSlider.setValue(percentage)



    def sizeChanged(self, value):
	h=humanReadableSize
	free = self.freeSpaceOnDrive()
	total = self.totalSpaceOnDrive()
	sliderValue = self.gui.sizeSlider.value()

	self.size = math.floor((free-self.minSize) * sliderValue / 100.0 + self.minSize)
	percentUsed = (total-free+(self.size))*100/(total*1.0)

	size = self.size

	if (percentUsed>100):
	    percentUsed = 99

	if (self.size > free):
	    size = free

	self.gui.pbFreeSpace.setValue(percentUsed)
	self.gui.lblFreeLeft.setText('%s Free' % h(free-size))
	self.gui.lblSize.setText('%s' % h(size))
	

    def updateProgressBarRange(self):
	self.gui.pbFreeSpace.setMinimum(0)
	self.gui.pbFreeSpace.setMaximum(99)

    def freeSpaceOnDrive(self):
	drive = self.getSelectedDrive()

	if drive: return drive.FreeSpace
	else: return 0


    def totalSpaceOnDrive(self):
	drive = self.getSelectedDrive()
	
	if drive: return drive.Size
	else: return 0

    def populateDrives(self):
	self.gui.comboDrive.clear()
	for disk in self.mainEngine.compatibility.disks:
	    self.gui.comboDrive.addItem(disk.DeviceID)

    def getSelectedDrive(self):
	for disk in self.mainEngine.compatibility.disks:
	    if disk.DeviceID == self.gui.comboDrive.currentText():
		return disk
	return None

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

	if self.getSelectedDrive().FreeSpace < self.size:
	    errorText += 'You do not have enough (%s required) free space on current drive.\n' % humanReadableSize(self.size)
	else:
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
	    QtGui.QMessageBox.warning(self, 'Warning', errorText, QtGui.QMessageBox.Ok)
	    return False

	self.mainEngine.config.username = username
	self.mainEngine.config.password = password
	self.mainEngine.config.drive = self.getSelectedDrive()
	self.mainEngine.config.size = self.size
	# TODO: config size and drive
	return True


    def nextIndex(self):
	return 2 # TODO: implement better
import math
from PyQt4 import QtGui,QtCore
from ui.controller.stepTemplate import StepWidget
from utils import humanReadableSize

from ui.gui.configuration import Ui_configuration

class Widget(QtGui.QWidget, StepWidget):
    heading = "Configure Your Pardus"

    defaultSize = long(5.0*1024*1024*1024)
    minSize = long(1.0*1024*1024*1024)

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_configuration()
	self.gui.setupUi(self)
	self.connect(self.gui.comboDrive, QtCore.SIGNAL('currentIndexChanged(int)'), self.driveChanged)
	self.connect(self.gui.sizeSlider, QtCore.SIGNAL('valueChanged(int)'), self.sizeChanged)
	
	self.mainEngine = mainEngine
	

    def driveChanged(self, index):
	free = self.freeSpaceOnDrive()
	self.gui.lblDriveFreeSpace.setText('%s free' % (humanReadableSize(free)))

	self.updateProgressBarRange()

	percentage = math.floor((self.defaultSize-self.minSize)*100/(free-self.minSize)*1.0)

	self.gui.sizeSlider.setValue(percentage)

    def sizeChanged(self, value):
	h=humanReadableSize
	free = self.freeSpaceOnDrive()
	total = self.totalSpaceOnDrive()
	sliderValue = self.gui.sizeSlider.value()

	self.installationSize = math.floor((free-self.minSize) * sliderValue / 100.0 + self.minSize)
        try:
            percentUsed = (total-free+(self.installationSize))*100/(total*1.0)
        except ZeroDivisionError as e:
            percentUsed = 0

	size = self.installationSize

	if (percentUsed>100):
	    percentUsed = 99

	if (self.installationSize > free):
	    size = free

	if not int(percentUsed)==self.gui.pbFreeSpace.value():
	    self.gui.pbFreeSpace.setValue(int(percentUsed))
	self.gui.lblFreeLeft.setText('%s Free' % h(free-size))
	self.gui.lblSize.setText('%s' % h(size))
	

    def updateProgressBarRange(self):
	pass

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
        self.mainEngine.compatibility.winPopulateDisks()
	for disk in self.mainEngine.compatibility.disks:
	    self.gui.comboDrive.addItem('%s %s' %(disk.DeviceID, disk.Name))


    def getSelectedDrive(self):
	for disk in self.mainEngine.compatibility.disks:
	    if disk.DeviceID == self.gui.comboDrive.currentText()[:2]:
                # TODO: TBD: First 2 letters of combobox is drive letter+colon.
                # This may fail in the future.
		return disk
	return None

    def onEnter(self):
        self.populateDrives()

	self.gui.txtPassword.setText('')
	self.gui.txtRetypePassword.setText('')
	self.mainEngine.password = None

    def onSubmit(self):
	# TODO: 'Not enough free space' warnings
	errorText = ''

	username = self.gui.txtUsername.text()
	password = self.gui.txtPassword.text()
	retypePassword = self.gui.txtRetypePassword.text()

	if self.getSelectedDrive().FreeSpace < self.installationSize:
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
	    #return False # TODO: re-activate ASAP.

	self.mainEngine.config.username = username
	self.mainEngine.config.password = password
	self.mainEngine.config.drive = self.getSelectedDrive()
	self.mainEngine.config.size = long(self.installationSize)
	return True


    def nextIndex(self):
	return 2

from PyQt4 import QtGui,QtCore
from ui.controller.stepTemplate import StepWidget
from ui.gui.internet import Ui_internet

from utils import humanReadableSize as hrS

class Widget(QtGui.QWidget, StepWidget):
    heading = "Download Your Pardus"

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_internet()
	self.gui.setupUi(self)
	self.mainEngine.versionManager.connectGui(self.slotUpdateDone)

	self.connect(self.gui.comboVersion, QtCore.SIGNAL('currentIndexChanged(int)'), self.versionChanged)
	self.connect(self.gui.comboMirror, QtCore.SIGNAL('currentIndexChanged(int)'), self.mirrorChanged)
	self.connect(self.gui.btnProxy1, QtCore.SIGNAL('clicked()'), self.setUpdateProxy)
	self.connect(self.gui.btnProxy2, QtCore.SIGNAL('clicked()'), self.setDownloadProxy)
	self.connect(self.gui.btnUpdate, QtCore.SIGNAL('clicked()'), self.updateVersions)
	self.connect(self.gui.btnCheck, QtCore.SIGNAL('clicked()'), self.checkCompatibility)


	self.populateVersions()


    def populateVersions(self):
	self.gui.comboVersion.clear()
	for version in self.mainEngine.versionManager.versions:
	    self.gui.comboVersion.addItem(version.name)

    def getVersionByName(self, name):
	for version in self.mainEngine.versionManager.versions:
	    if version.name == name:
		return version

	return None

    def getMirrorByName(self, name):
	version = self.getVersionByName(self.gui.comboVersion.currentText())
	for mirror in version.mirrors:
	    if mirror.hostname == str(name).split(' ')[0]:
		return mirror

	return None

    def versionChanged(self, index):
	if self.gui.comboVersion.currentIndex() > -1:
	    self.version = self.getVersionByName(self.gui.comboVersion.currentText())
	    self.gui.lblSize.setText('%s' % hrS(self.version.size))
	    self.populateMirrors(self.version)

    def populateMirrors(self, version):
	self.gui.comboMirror.clear()
	for mirror in version.mirrors:
	    self.gui.comboMirror.addItem('%s (%s)' % (mirror.hostname, mirror.country))

    def setUpdateProxy(self):
	self.setProxyDialog(self.mainEngine.versionManager,'Version List Update Proxy')

    def setDownloadProxy(self):
	self.setProxyDialog(self.mainEngine.ftpDownloader, 'Download Proxy')

    def setProxyDialog(self, target, title):
	proxy,ok = QtGui.QInputDialog.getText(self, title, 'Enter proxy in host:port format')
	proxy = proxy.split(':')

	if ok:
	    if len(proxy)==2:
		target.updateProxy(proxy[0],proxy[1])
	    else:
		QtGui.QMessageBox.warning(self, 'Error', 'Proxy could not be set. Invalid proxy format. i.e 4.4.4.4:4444', QtGui.QMessageBox.Ok)

    def mirrorChanged(self):
	self.mirror = self.getMirrorByName(self.gui.comboMirror.currentText().split(' ')[0])
	
    def onSubmit(self):
	errorText=''
	
	if not self.version:  # TODO: other limitations?
	    errorText += 'Please choose a version.\n'

	elif not self.mirror:
	    errorText += 'Please choose a mirror.\n'

	else:
	    if long(self.version.minspace) > self.mainEngine.config.size:
		errorText += 'You have reserved %s for installation but %s requires %s of space (recommended %s). Go back and increase installation size.\n' % (hrS(self.mainEngine.config.size), self.version.name, hrS(self.version.minspace), hrS(self.version.space))

	    archBit = self.mainEngine.compatibility.architectureBit

	    if self.version.type=='64-bit' and archBit==32:
		errorText += '%s is an 64-bit operating system and will not work on your %d-bit architecture. Try installing a 32-bit alternative.'  %(self.version.name, archBit)

	if errorText:
	    QtGui.QMessageBox.warning(self, 'Warning', errorText, QtGui.QMessageBox.Ok)
	    return False
	
	self.mainEngine.version = self.version
	self.mainEngine.ftpDownloader.setMirror(self.mirror)

	return True

    def updateVersions(self):
	self.gui.btnUpdate.setText('Updating...')
	self.mainEngine.versionManager.updateDefinitionsFile()
	

    def slotUpdateDone(self, success):
	if success:
	    self.populateVersions()
	    self.gui.btnUpdate.setText('Updated!')
	    self.gui.btnUpdate.setEnabled(False)
	    QtGui.QMessageBox.information(self, 'Update Completed', 'New version list is ready to use.', QtGui.QMessageBox.Ok)
	else:
	    self.gui.btnUpdate.setText('Update Failed')
	    QtGui.QMessageBox.warning(self, 'Error in Update', self.mainEngine.versionManager.err, QtGui.QMessageBox.Ok)

    def checkCompatibility(self):
	report = ''

	totalMemory = self.mainEngine.compatibility.totalMemory
	minmemory = long(self.version.minmemory)
	memory = long(self.version.memory)

	report += 'Memory (RAM):\n'
	report += 'You have %s memory. ' % hrS(totalMemory)
	report += '%s requires at least %s of memory. Recommended is %s.\n\n' % (self.version.name, hrS(minmemory), hrS(memory))

	if totalMemory < minmemory:
	    report += '!!! '
	    report += 'YOU DO NOT HAVE ENOUGH MEMORY. (%s) It is strongly recommended not to install.' % hrS(totalMemory)
	elif totalMemory > memory:
	    report += 'It is OK to use %s safely.' % self.version.name
	else:
	    report += 'You have enough memory to run under minimal conditions but you may have problems during your usage. It is recommended to add memory to your computer.'
	report += '\n------------------------------------\n'

	archBit = self.mainEngine.compatibility.architectureBit
	archType = self.mainEngine.compatibility.architectureName
	
	report += 'CPU Architecture:\n'
	report += 'Your CPU has %d-bit (%s) architecture. ' % (archBit, archType)
	report += '%s is prepared for %s architectures.\n\n' % (self.version.name, self.version.type)

	if self.version.type=='64-bit':
	    if archBit==32:
		report += '!!! '
		report += 'Your architecture is NOT COMPATIBLE with %s. It is STRONGLY recommended NOT to install.' % self.version.name
	    elif archBit==64:
		report += 'It is safe to use %s with your computer.'  % self.version.name
	elif self.version.type == '32-bit':
	    # reserved for future architecture designs.
	    report += 'It is safe to use %s with your computer.'  % self.version.name
	report += '\n------------------------------------\n'

	minspace = long(self.version.minspace)
	space = long(self.version.space)
	size = self.mainEngine.config.size

	report += 'Free Space:\n'
	report += 'Your have reserved %s of free space for installation. ' % hrS(size)
	report += '%s requires %s of free space (recommended %s).\n\n' % (self.version.name, hrS(minspace), hrS(space))

	if size < minspace:
	    report += '!!! '
	    report += 'You DO NOT HAVE ENOUGH free space reserved. (%s) It is strongly recommended not to install if you do not have any free space.' % hrS(size)
	elif size > space:
	    report += 'It is OK to use %s safely.' % self.version.name
	else:
	    report += 'It is OK to use %s. However it is better to reserve more free space for future usage.'
	
	if report:
	    QtGui.QMessageBox.information(self, 'Compatibility Report', report, QtGui.QMessageBox.Ok)

    def nextIndex(self):
	return 7

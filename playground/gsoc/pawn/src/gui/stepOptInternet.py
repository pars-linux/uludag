from gui.widgetOptInternet import Ui_widgetOptInternet
from gui.stepTemplate import StepWidget
from PyQt4 import QtGui,QtCore
from utils import humanReadableSize
from gui.widgetOptInternet import Ui_widgetOptInternet

class Widget(QtGui.QWidget, StepWidget):
    heading = "Download Your Pardus"

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_widgetOptInternet()
	self.gui.setupUi(self)
	self.mainEngine.versionManager.connectGui(self.slotUpdateDone)

	self.connect(self.gui.comboVersion, QtCore.SIGNAL('currentIndexChanged(int)'), self.versionChanged)
	self.connect(self.gui.comboMirror, QtCore.SIGNAL('currentIndexChanged(int)'), self.mirrorChanged)
	self.connect(self.gui.btnProxy1, QtCore.SIGNAL('clicked()'), self.setUpdateProxy)
	self.connect(self.gui.btnProxy2, QtCore.SIGNAL('clicked()'), self.setDownloadProxy)
	self.connect(self.gui.btnUpdate, QtCore.SIGNAL('clicked()'), self.updateVersions)

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
	    self.gui.lblSize.setText('%s' % humanReadableSize(int(self.version.size)))
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
		warning = QtGui.QMessageBox.warning(self, 'Error', 'Proxy could not be set. Invalid proxy format. i.e 4.4.4.4:4444', QtGui.QMessageBox.Ok)

    def mirrorChanged(self):
	self.mirror = self.getMirrorByName(self.gui.comboMirror.currentText().split(' ')[0])
	
    def nextIndex(self):
	return 6 # TODO: implement

    def onSubmit(self):
	errorText=''
	
	if not self.version:  # TODO: other limitations?
	    errorText += 'Please choose a version.\n'

	if not self.mirror:
	    errorText += 'Please choose a mirror.\n'

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
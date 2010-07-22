import math
from utils import *
from PyQt4 import QtGui,QtCore
from ui.controller.stepTemplate import StepWidget
from ui.gui.downloading import Ui_downloading

class Widget(QtGui.QWidget, StepWidget):
    heading = "Downloading Pardus"

    downloaded = False
    counter = 0
    
    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_downloading()
	self.gui.setupUi(self)
	self.mainEngine.ftpDownloader.connectGui(self)

	QtCore.QObject.connect(self.gui.btnCheck, QtCore.SIGNAL('clicked()'), self.validateFile)

    def onEnter(self):
	self.gui.progressBar.setValue(0)
	self.gui.status.setText('Preparing to download...')
	self.gui.speed.setText('N/A')
	self.gui.completed.setText('N/A')
	self.gui.ETA.setText('N/A')
	self.gui.percentage.setText('N/A')

	self.gui.version.setText(self.mainEngine.version.name)

	self.downloaded = False
	self.updateButtons()

	mirror = self.mainEngine.ftpDownloader.mirror
	if mirror:
	    self.mainEngine.ftpDownloader.startTransfer()
	    self.gui.mirror.setText('%s (%s)'% (mirror.hostname, mirror.country))
	else:
	    log.warning('Mirror not found on download stage.')

    def slotStateChange(self, state):
	statusText = ''
	if state==1:
	    statusText = 'Looking up hostname.'
	elif state==2:
	    statusText = 'An attempt to connect to the host is in progress.'
	elif state==3:
	    statusText = 'Connection to the host is done.'
	elif state==4:
	    if (self.mainEngine.ftpDownloader.downloading):
		statusText = 'Downloading in progress.'
	    else:
		statusText = 'Connection and login is done.'

	if(statusText):
	    self.gui.status.setText(statusText)

    def updateButtons(self):
	if self.downloaded:
	    self.mainEngine.gui.btnNext.setEnabled(True)
	    self.gui.btnCheck.setVisible(True)
	else:
	    self.mainEngine.gui.btnNext.setEnabled(False)
	    self.gui.btnCheck.setVisible(False)

    def validateFile(self):
	computed = self.mainEngine.md5sum.encryptFile(self.mainEngine.ftpDownloader.filePath).lower()
	original = self.mainEngine.version.md5sum.lower()

	if computed==original:
	    title = 'Validated'
	    msg = 'Downloaded file is valid. You can proceed installation safely.'
	    method = QtGui.QMessageBox.information
	else:
	    title = 'Invalid File'
	    msg = 'Downloaded file is INVALID. It is STRONGLY recommended not to continue installation. Please retry downloading.'
	    method = QtGui.QMessageBox.information

	method(self, title, msg, QtGui.QMessageBox.Ok)

    def slotProcessDone(self):
	if self.mainEngine.ftpDownloader.errorMessage:
	    self.downloaded  = False
	    msg = self.mainEngine.ftpDownloader.errorMessage
	else:
	    self.downloaded = True
	    msg = 'Download completed!'

	self.updateButtons()

	self.gui.status.setText(str(msg))
	self.gui.progressBar.setValue(100)
	self.gui.speed.setText('N/A')
	self.gui.completed.setText('Finished!')
	self.gui.ETA.setText('N/A')
	self.gui.percentage.setText('100%')
	
    def slotStatsChange(self, percentageCompleted, downloadSpeed, ETA):

	self.gui.speed.setText('%s/s' % humanReadableSize(downloadSpeed))
	self.gui.progressBar.setValue(int(math.floor(percentageCompleted/100.0)))
	self.gui.percentage.setText('%.2f %%' % (percentageCompleted/100.0))
	self.gui.ETA.setText(humanReadableTime(ETA))

    def slotTransferProgress(self, transferredSize, totalSize):
	self.counter += 1
	if self.counter % 20 == 0:
	    self.gui.status.setText('Download in progress...')
	    self.gui.completed.setText('%s of %s' % (humanReadableSize(transferredSize), humanReadableSize(totalSize)))
	    self.counter = 0

    def onRollback(self):
	reply = QtGui.QMessageBox.warning(self, 'Warning', 'Are you sure to cancel? If you go back, downloading will be cancelled and you will be have to start over again.', QtGui.QMessageBox.Yes, QtGui.QMessageBox.Cancel)

	if reply == QtGui.QMessageBox.Yes:
	    self.mainEngine.ftpDownloader = None
	    self.mainEngine.initFTP()
	    self.mainEngine.ftpDownloader.connectGui(self)

	    self.downloaded = True
	    self.updateButtons()

	    return True
	else:
	    return False

    def onSubmit(self):
	if self.downloaded:
            self.mainEngine.config.isoPath = self.mainEngine.ftpDownloader.filePath
            return True
        else:
            QtGui.QMessageBox.error(self, 'Error', 'ISO File is not downloaded or the downloaded file is corrupt. Try again.', QtGui.QMessageBox.OK)
            return False

    def nextIndex(self):
	return 8
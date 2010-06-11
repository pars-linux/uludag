import math
from gui.stepTemplate import StepWidget
from PyQt4 import QtGui
from utils import *

from gui.widgetDownloading import Ui_widgetDownloading

class Widget(QtGui.QWidget, StepWidget):
    heading = "Downloading Pardus"
    
    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_widgetDownloading()
	self.gui.setupUi(self)
	self.mainEngine.ftpDownloader.connectGui(self)

    def onEnter(self):
	self.gui.progressBar.setValue(0)
	self.gui.status.setText('Preparing to download...')
	self.gui.speed.setText('N/A')
	self.gui.completed.setText('N/A')
	self.gui.ETA.setText('N/A')
	self.gui.percentage.setText('N/A')

	self.gui.version.setText(self.mainEngine.version.name)

	mirror = self.mainEngine.ftpDownloader.mirror
	if mirror:
	    self.mainEngine.ftpDownloader.startTransfer()
	    self.gui.mirror.setText('%s (%s)'% (mirror.hostname, mirror.country))
	else:
	    log.warning('Mirror not found on download stage.')

    def onSubmit(self):
	return False
    
    def nextIndex(self):
	return 0

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

    def slotProcessDone(self):
	if self.mainEngine.ftpDownloader.errorMessage:
	    msg = self.mainEngine.ftpDownloader.errorMessage
	else:
	    msg = 'Download completed!'

	self.gui.status.setText(str(msg))
	self.gui.progressBar.setValue(100)
	
    def slotStatsChange(self, percentageCompleted, downloadSpeed, ETA):

	self.gui.speed.setText('%s/s' % humanReadableSize(downloadSpeed))
	self.gui.progressBar.setValue(int(math.floor(percentageCompleted/100.0)))
	self.gui.percentage.setText('%.2f %%' % (percentageCompleted/100.0))
	self.gui.ETA.setText(humanReadableTime(ETA))

    def slotTransferProgress(self, transferredSize, totalSize):
        self.gui.status.setText('Download in progress...')
	self.gui.completed.setText('%s of %s' % (humanReadableSize(transferredSize), humanReadableSize(totalSize)))

    def onRollback(self):
	reply = QtGui.QMessageBox.warning(self, 'Are you sure to cancel?', 'If you go back, downloading will be cancelled and you will be have to start over again.', QtGui.QMessageBox.Yes, QtGui.QMessageBox.Cancel)

	if reply == QtGui.QMessageBox.Yes:
	    self.mainEngine.ftpDownloader = None
	    self.mainEngine.initFTP()
	    self.mainEngine.ftpDownloader.connectGui(self)
	    return True
	else:
	    return False
	
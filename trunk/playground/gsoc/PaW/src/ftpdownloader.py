import os
import time
import math
from PyQt4.QtNetwork import QFtp
from PyQt4 import QtCore

import logger
log = logger.getLogger("FTPDownloader")

class FTPDownloader(QFtp):
    '''ISO downloader via ftp protocol specialized for
    Mirror object -- a QFtp instance. Transfers files
    in Binary and PASV mode.'''

    speedCalculateInterval = 3.0 # seconds
    proxyHost, proxyIP, fsock = None,None,None
    errorMessage = ''

    statsChanged = QtCore.pyqtSignal(int, int, int, name='statsChanged') # percentageCompleted, downloadSpeed, ETA

    def __init__(self, destinationFile=None, mirror=None):
	QFtp.__init__(self) # TODO: or parent? solve this.
	self.updateProxy()

	self.mirror = mirror
	self.filePath = destinationFile
	self.downloading = False

	QtCore.QObject.connect(self, QtCore.SIGNAL('commandFinished(int,bool)'), self.logCommandFinished)
	QtCore.QObject.connect(self, QtCore.SIGNAL('stateChanged(int)'), self.logChangeState)
	QtCore.QObject.connect(self, QtCore.SIGNAL('done(bool)'), self.processDone)
	QtCore.QObject.connect(self, QtCore.SIGNAL('dataTransferProgress(qint64,qint64)'), self.traceTransferProgress)
	QtCore.QObject.connect(self, QtCore.SIGNAL('readyRead()'), self.writeBack)

    def setMirror(self, mirror):
	self.mirror = mirror

    def updateProxy(self, host=None, ip=None):
	if host: self.proxyHost = host
	if ip: self.proxyIP = ip
	
    def setDestinationPath(self, destinationFile):
	self.filePath = destinationFile

    def startTransfer(self):
	log.debug("Starting transfer...")

	if self.downloading:
	    return

        self.connectToHost(self.mirror.hostname, long(self.mirror.port))
        if (self.mirror.login=='true'):
            self.login(self.mirror.username, self.mirror.password)

        self.cd(self.mirror.path)

	self.initializeDownload()

	if self.proxyHost and self.proxyIP:
	    self.setProxy(self.proxyHost, long(self.proxyIP)) #QFtp method
	    
	self.initializeFile()

        self.get(self.mirror.filename) #start the transfer
        self.close()

    def initializeDownload(self):
	self.downloadSpeed = 0
	self.averageSpeed = 0
	self.initialBytes = 0
	self.totalBytes = 0
	self.timeCounter = time.time()
	self.timeStart = time.time()
	self.timeCompleted = 0
	self.ETA = 0
	self.percentageCompleted = 0
	self.packetCounter = 0
	self.downloading = False

    def initializeFile(self):
	self.fsock = open(self.filePath, 'wb') # TODO: decide to use buffering
	# TODO: decide binary mode
	# TODO: decide to use os.tmpfile, os.tmpname etc. consider vulnerabilitiesfsock

    def logCommandFinished(self, id, error):
	if error:
	    self.errorMessage = "FTP Error: "+self.errorString().replace('\n', '')
	    log.error(self.errorMessage)
	else:
	    log.debug('Command finished: %d' % id)

    def traceTransferProgress(self, transferredSize, totalSize):
	self.downloading = True
	self.percentageCompleted = 100.0*transferredSize/totalSize

	if self.packetCounter == 0:
	    self.totalBytes = totalSize # TODO: Discuss is it faster w/o 'if'?

	if(time.time() - self.timeCounter > self.speedCalculateInterval):
	    self.downloadSpeed = (transferredSize-self.initialBytes) / (time.time()-self.timeCounter)
	    self.timeCounter = time.time()
	    self.initialBytes = transferredSize

	    self.statsChanged.emit(int(self.percentageCompleted*100),
		int(math.floor(self.downloadSpeed)), int(self.ETA))

	try:
	    self.ETA = (totalSize-transferredSize)/self.downloadSpeed #seconds
	except ZeroDivisionError:
	    self.ETA = 0

	self.packetCounter += 1 # TODO: redundant?
	
    def processDone(self, error):
	self.downloading = False
	self.timeCompleted = time.time()-self.timeStart
	
	if self.timeCompleted:
	    self.averageSpeed = self.totalBytes/self.timeCompleted
	else:
	    self.averageSpeed = 0 #ZeroDivisionError
	
	if error:
	    self.errorMessage = "Interrupted. "+self.errorString().replace('\n', '')
	    log.error(self.errorMessage)
	    self.cleanCorruptFile()
	else:
	    log.debug("FTP transfer completed in %s seconds. (%f kb/s) %d packets."  % (self.timeCompleted, self.averageSpeed/1024.0, self.packetCounter))

	if self.fsock and (not self.fsock.closed):
	    self.fsock.close()

    def logChangeState(self, changed):
	log.debug("FTP state changed to "+str(changed))

    def writeBack(self):
	socketData = self.readAll()
	self.fsock.write(socketData)
	socketData = None

    def cleanCorruptFile(self):
	"Removes partially completed local file after a bad transfer."
	log.debug('Corrupt file has been deleted.')
	os.remove(self.filePath)

    def connectGui(self, gui):
	QtCore.QObject.connect(self, QtCore.SIGNAL('stateChanged(int)'), gui.slotStateChange)
	QtCore.QObject.connect(self, QtCore.SIGNAL('done(bool)'), gui.slotProcessDone)
	QtCore.QObject.connect(self, QtCore.SIGNAL('statsChanged(int, int, int)'), gui.slotStatsChange)
	QtCore.QObject.connect(self, QtCore.SIGNAL('dataTransferProgress(qint64,qint64)'), gui.slotTransferProgress)

	QtCore.QObject.connect(self, QtCore.SIGNAL('dataTransferProgress(qint64,qint64)'), self.traceTransferProgress)
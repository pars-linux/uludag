import sys, os, time
from PyQt4.QtNetwork import QFtp
from PyQt4 import QtCore, QtGui
from logger import getLogger
log = getLogger("FTPDownloader")

class FTPDownloader(QFtp):
    '''ISO downloader via ftp protocol specialized for
    Mirror object -- a QFtp instance. Transfers files
    in Binary and PASV mode.'''

    speedCalculateInterval = 5.0 # seconds

    def __init__(self, mirror=None, destinationFile=None):
	QFtp.__init__(self) # TODO: or parent? solve this.

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

    def setDestinationPath(self, destinationFile):
	self.filePath = destinationFile

    def startTransfer(self):
	if self.downloading:
	    return

        self.connectToHost(self.mirror.hostname, long(self.mirror.port))
        if (self.mirror.login=='true'):
            self.login(self.mirror.username, self.mirror.password)

        self.cd(self.mirror.path)

	self.initializeDownload()
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
	    log.error("FTP Error in command "+str(id)+". "+self.errorString())

    def traceTransferProgress(self, transferredSize, totalSize):
	self.downloading = True

	if self.packetCounter == 0:
	    self.totalBytes = totalSize # TODO: Discuss is it faster w/o 'if'?

	if(time.time() - self.timeCounter > self.speedCalculateInterval):
	    self.downloadSpeed = (transferredSize-self.initialBytes) / (time.time()-self.timeCounter)
	    self.timeCounter = time.time()
	    self.initialBytes = transferredSize
	    #print self.downloadSpeed/1024, 'kilobytes/sec --', self.percentageCompleted, '%--', 'ETA:%d sec (%d min).'% (self.ETA, self.ETA/60)

	self.percentageCompleted = 100.0*transferredSize/totalSize
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
	    log.error("FTP transfer completed with errors: "+self.errorString())
	    self.cleanCorruptFile()
	else:
	    log.info("FTP transfer completed in %s seconds. (%f kb/s) %d packets."  % (self.timeCompleted, self.averageSpeed/1024.0, self.packetCounter))

	if not self.fsock.closed:
	    self.fsock.close()

    def logChangeState(self, changed):
	log.debug("FTP state changed to "+str(changed))

    def writeBack(self):
	socketData = self.readAll()
	self.fsock.write(socketData)

    def cleanCorruptFile(self):
	"Removes partially completed local file after a bad transfer."
	os.remove(self.filePath)
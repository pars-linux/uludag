import sys, time
from PyQt4.QtNetwork import QFtp
from PyQt4 import QtCore, QtGui
from logger import getLogger
log = getLogger("FTPDownloader")

class FTPDownloader(QFtp):
    '''
    ISO downloader via ftp protocol specialized for
    Mirror object -- a QFtp instance.
    '''
    
    def __init__(self, mirror, destinationFile):
	QFtp.__init__(self) # TODO: or parent? solve this.
	self.mirror = mirror
	self.filePath = destinationFile
	self.speedCalculateInterval = 1.0 #seconds

    def startTransfer(self):
	print 'Start'
        self.connectToHost(self.mirror.hostname, self.mirror.port)
        if (self.mirror.login=='true'):
            self.login(self.mirror.username, self.mirror.password)
        self.cd(self.mirror.path)

	# prepare tests
	self.downloadSpeed = 0
	self.averageSpeed = 0
	self.initialBytes = 0
	self.timeCounter = time.time()
	self.timeStart = time.time()
	self.timeCompleted = 0
	self.ETA = 0
	self.percentageCompleted = 0
	self.packetCounter = 0

        self.get(self.mirror.filename) #start the transfer
        self.close()

    def logCommandFinished(self, id, error):
	if error:
	    log.error("FTP Error in command "+str(id)+". "+self.errorString())

    def traceTransferProgress(self, transferredSize, totalSize):
	if self.packetCounter == 0:
	    self.totalBytes = totalSize

	if(time.time() - self.timeCounter > self.speedCalculateInterval):
	    self.downloadSpeed = (transferredSize-self.initialBytes) / (time.time()-self.timeCounter)
	    self.timeCounter = time.time()
	    self.initialBytes = transferredSize
	    print self.downloadSpeed/1024, 'kilobytes/sec', self.percentageCompleted, '%', 'ETA:%d sec (%d min).'% (self.ETA, self.ETA/60)

	self.percentageCompleted = 100.0*transferredSize/totalSize
	try:
	    self.ETA = (totalSize-transferredSize)/self.downloadSpeed #seconds
	except ZeroDivisionError:
	    self.ETA = 0

	self.packetCounter += 1
	
    def processDone(self, error):
	print 'done'
	self.timeCompleted = time.time()-self.timeStart
	self.averageSpeed = self.totalBytes/self.timeCompleted
	
	if error:
	    log.error("FTP transfer completed with errors: "+self.errorString())
	else:
	    log.info("FTP transfer completed in %s seconds. (%f kb/s)"  % (self.timeCompleted, self.averageSpeed/1024.0))

    def logChangeState(self, changed):
	log.info("FTP state changed to "+str(changed))
import os
import sys
import shutil
import tempfile
from PyQt4 import QtGui

import logger
if __name__=='__main__':
    tmpDir = tempfile.mkdtemp()
    logfile = os.path.join(tmpDir, 'paw.log')
    logger.destination = logfile
    print 'Logging file is in %s.' % logger.destination
    log = logger.getLogger('PaW (main)')
    log.info('Hi!')

from guicontroller import PaWGui
from ftpdownloader import FTPDownloader
from versionmanager import VersionManager
from compatibility import Compatibility
from md5sum import MD5sum
from installer import Installer

class Config(object):
    def __repr__(self, repr = ''):
	for key,value in self.__dict__.iteritems():
	    repr += "->  %s=%s\n"%(key,value)
	return repr

class PaW():
    application = 'Pardus (Paw)' # ASCII, please.
    appid = 'Pardus' # ASCII, please.
    appversion = '0.2'
    publisher = 'Pardus-Linux (TM)'
    home = 'http://www.pardus.org.tr'
    
    executable = 'PaW.exe'

    logfile = ''

    def __init__(self):
	self.config = Config()
        self.setTempFolder()
        self.setTempFile() # should be after setTempFolder

	self.compatibility = Compatibility()
	self.versionManager = VersionManager()
	self.md5sum = MD5sum()
        self.installer = Installer(self)
        self.initFTP()      # should be after installer
        self.initLogger()
        
	self.gui = PaWGui(self)

    def initFTP(self):
        log.info('FTP Downloader inited for %s.' % self.config.tmpFile)
        self.ftpDownloader = FTPDownloader(self.config.tmpFile)


    def initLogger(self):
        global logfile
        self.logfile = logfile

    def setTempFolder(self):
        """
        Create a folder on temp folder of operating system to save
        downloaded ISO and other files.
        """
        global tmpDir
        self.config.tmpDir = tmpDir

    def setTempFile(self):
        "Request a filename to save downloaded ISO"
        self.config.tmpFile = \
            os.path.join(self.config.tmpDir, 'downloaded.iso')
            # TODO: Rename downloaded file path.

    def cleanup(self):
        """
        Cleans temporary files on demand. Should be called upon exit.
        """
        try:
            shutil.rmtree(self.config.tmpDir, ignore_errors = True)
            log.info('Cleanup done.')
            return True
        except:
            log.error('Could not remove tmp directory at %s ' % self.config.tmpDir)
            return False

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    paw = PaW()
    sys.exit(app.exec_())
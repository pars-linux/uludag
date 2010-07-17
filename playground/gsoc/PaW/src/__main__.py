import sys
from PyQt4 import QtGui

from guicontroller import PaWnGui
from ftpdownloader import FTPDownloader
from versionmanager import VersionManager
from compatibility import Compatibility
from md5sum import MD5sum
from installer import Installer

from logger import getLogger
log = getLogger('PaWn')

class Config(object):
    def __repr__(self, repr = ''):
	for key,value in self.__dict__.iteritems():
	    repr += "->  %s=%s\n"%(key,value)
	return repr

class PaWn():
    application = 'Pardus (Paw)' # ASCII, please.
    appid = 'Pardus' # ASCII, please.
    appversion = '0.2'
    publisher = 'TUBITAK/UEKAE'
    home = 'http://www.pardus.org.tr'

    def __init__(self):
	self.config = Config()
	self.compatibility = Compatibility()
	self.versionManager = VersionManager()
	self.md5sum = MD5sum()
        self.installer = Installer(self)
        self.initFTP()
        
	self.gui = PaWnGui(self)

    def initFTP(self):
        log.info('FTP Downloader inited for %s.' % self.config.tmpFile)
        self.ftpDownloader = FTPDownloader(self.config.tmpFile)

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    pawn = PaWn()
    sys.exit(app.exec_())
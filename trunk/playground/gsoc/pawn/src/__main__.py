import sys
from PyQt4 import QtGui

from guicontroller import PaWnGui
from ftpdownloader import FTPDownloader
from versionmanager import VersionManager

class Config(object):
    def __repr__(self, repr = ''):
	for key,value in self.__dict__.iteritems():
	    repr += "->  %s=%s\n"%(key,value)
	return repr

class PaWn():
    def __init__(self):
	self.config = Config()
	self.versionManager = VersionManager()
	self.initFTP()

	self.gui = PaWnGui(self)

    def initFTP(self):
	self.ftpDownloader = FTPDownloader('test.iso')

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    pawn = PaWn()
    sys.exit(app.exec_())
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

from guicontroller import PaWnGui
from ftpdownloader import FTPDownloader

class PaWn():
    def __init__(self):
	self.gui = PaWnGui(self)	

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    pawn = PaWn()
    sys.exit(app.exec_())
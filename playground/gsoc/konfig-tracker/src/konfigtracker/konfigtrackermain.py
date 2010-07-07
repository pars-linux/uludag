#===============================================================================
# konfigtracker
#===============================================================================


#necessary modules
import os
from operations import *

#Qt modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#PyKDE4 modules
from PyKDE4.kdeui import *

#KonfigTracker Modules
from monitor import Monitor

#KonfigTracker Gui
from gui.ui_mainwindow import Ui_MainWindow

class KonfigTracker(KXmlGuiWindow, Ui_MainWindow):

	def __init__(self,app):
        	KXmlGuiWindow.__init__(self)
		self.setupUi(self)
		self.setFixedSize(self.width(), self.height())
        	self.app = app
		self.connectMainSignals()


		#Backend Initializations
        	self.InitApplication()
		self.monitor = Monitor(app)
		self.monitor.start()
		

	def InitApplication(self):
        	""" If there exist no database in this path, this function will create
        	one, and initialize a git repository there.
        	"""
        	path = GetLocalDir()  + "/KonfigTrackerDB"

        	if not os.access(path,os.F_OK):
			os.mkdir(path)
			CreateDB(path)
			Backup()
			
	def connectMainSignals(self):
		pass

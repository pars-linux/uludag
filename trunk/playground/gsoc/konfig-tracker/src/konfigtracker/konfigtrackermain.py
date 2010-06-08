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

class KonfigTracker(KMainWindow):

	def __init__(self,app):
        	KMainWindow.__init__(self)
        	self.resize (640, 480)
        	self.app = app
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

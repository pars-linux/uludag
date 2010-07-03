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
		#this function is to be removed, once the gui is developed.

	def InitApplication(self):
        	""" If there exist no database in this path, this function will create
        	one, and initialize a git repository there.
        	"""
        	path = GetLocalDir()  + "/KonfigTrackerDB"

        	if not os.access(path,os.F_OK):
			os.mkdir(path)
			CreateDB(path)
			Backup()
			
	def showMenu(self):
		while True:
			print "This is a retro style menu, just to confirm that backend works properly"
			print 80*"*"
			
			print "1. Backups <to be shown in gui>"
			print "2. Restore to selected backup"
			print "3. Restore"
			print "4. Export current backup"
			print "Choice : "
			ch = raw_input()
			if ch == 1:
				showCommit()
			if ch == 2:
				pass
			if ch == 3:
				pass	

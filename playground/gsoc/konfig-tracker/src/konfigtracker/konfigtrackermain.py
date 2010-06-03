#===============================================================================
# konfigtracker
#===============================================================================


#necessary modules
import os,git
from time import strftime,localtime
import distutils.dir_util as DirUtil

#Qt modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#PyKDE4 modules
from PyKDE4.kio import KIO, KDirWatch
from PyKDE4.kdecore import KUrl, KStandardDirs
from PyKDE4.kdeui import *

class KonfigTracker(KMainWindow):

	def __init__(self,app):
        	KMainWindow.__init__(self)
        	self.resize (640, 480)
        	self.app = app
        	self.dw = None
        	self.initialize()
        	self.Monitor()
        
	def getLocalDir(self):
        	"""
        	Return the path to local kde directory, which may change depending upon
        	the distros. In fedora 13, it is $HOME/.kde whereas it is $HOME/.kde4 in Pardus
        	"""
        	kdir = KStandardDirs()
        	return kdir.localkdedir()
        
	def initialize(self):
        	''' If there exist no database in this path, this function will create
        	one, and initialize a git repository there.
        	'''
        	path = self.getLocalDir()  + "/konfigtracker-repo"

        	if not os.access(path,os.F_OK):
			os.mkdir(path)
			self.createRepo(path)
			self.performImport()
            
	def createRepo(self,path):
        	'''
        	Initialize a git repository in path.
        	'''
        	gitRepo = git.Git(path)
        	gitRepo.init()
            
	def addToRepo(self):
        	"""
        	Add blobs into the repository
        	"""
        	repo = git.Git( self.getLocalDir()+ "/konfigtracker-repo/")
        	repo.execute(["git","add","."])
        	self.commit()

	def commit(self):
        	backupTime = strftime("%a, %d %b %Y %H:%M:%S", localtime())
        	repo = git.Git(self.getLocalDir() + "/konfigtracker-repo/")
        	message = "Backup on "+ backupTime
		try:
        		repo.execute(["git","commit","-a","-m",message])
		except git.errors.GitCommandError:
			pass
        	print message
        
	def performImport(self):
        	"""
        	This will perform the initial import of config files from
        	.kde4/share/config to .kde4/konfigtracker-repo.
        	"""
        	srcPath = str(self.getLocalDir() + "/share/config")
        	destPath = str(self.getLocalDir() + "/konfigtracker-repo/config")
        
        	if DirUtil.copy_tree(srcPath,destPath,update=1):
			self.addToRepo()
	
	def Monitor(self):
        	"""
        	Setting up a KDirWatch in the source directory
        	"""
        	app=self.app
        	self.dw = KDirWatch()
        	path = self.getLocalDir() + "share/config"
        	print path
        	(self.dw).addDir(path)
        	app.connect(self.dw, SIGNAL("dirty(QString)"), self.performImport)

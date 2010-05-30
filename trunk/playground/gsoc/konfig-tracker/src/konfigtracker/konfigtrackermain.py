#===============================================================================
# konfigtracker
#===============================================================================


#necessary modules
import os,git
from time import strftime,localtime

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
            
    def slotMessage(self):
        """
        Perform the commit to repository
        """
        repo = git.Git( self.getLocalDir()+ "/konfigtracker-repo/")
        repo.execute(["git","add","."])
        self.commit()
        
    def commit(self):
        backupTime = strftime("%a, %d %b %Y %H:%M:%S", localtime())
        repo = git.Git(self.getLocalDir() + "/konfigtracker-repo/")
        message = "Backup on "+ backupTime
        repo.execute(["git","commit","-a","-m",message])
        print message
        
    def performImport(self):
        """
        This will perform the initial import of config files from
        .kde4/share/config to .kde4/konfigtracker-repo.
        """
        srcPath = self.getLocalDir() + "/share/config/"
        destPath = self.getLocalDir() + "/konfigtracker-repo/"
        dir = QDir(self.getLocalDir() + "/share/config/")
        entryList = dir.entryList()
        
        #copying the files from source to destination.
        app = self.app
        srcList = QStringList()
        for i in entryList:
            if not i in [".","..",]:
                srcList.append(srcPath + i)
        
        src = KUrl.List(srcList)
        dest = KUrl(destPath)
        job = KIO.copy(src, dest, KIO.Overwrite)
        app.connect(job, SIGNAL("finished(KJob*)"),self.slotMessage)
        
    def Monitor(self):
        """
        Setting up a KDirWatch in the source directory
        """
        app=self.app
        dw = KDirWatch()
        path = self.getLocalDir() + "share/config/"
        print path
        dw.addDir(path)
        print dw.isStopped()
        app.connect(dw, SIGNAL("dirty(QString)"), self.performImport)    
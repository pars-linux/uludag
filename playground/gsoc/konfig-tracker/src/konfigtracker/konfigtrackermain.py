#===============================================================================
# konfigtracker
#===============================================================================




#necessary modules
import os,git
from time import strftime,localtime

#Qt modules
from PyQt4.QtCore import QDir, SIGNAL, QStringList

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
            self.performInitImport()
            
        else:
            print "Database Exists!"
            
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
        
    def performInitImport(self):
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
        job = KIO.copy(src, dest, KIO.HideProgressInfo)
        app.connect(job, SIGNAL("finished(KJob*)"),self.slotMessage)
        
    def Monitor(self):
        """
        Setting up a KDirWatch in the source directory
        """
        print "I am here"
        monitor = KDirWatch()
        path = self.getLocalDir() + "/share/config/"
        monitor.addDir(path, KDirWatch.WatchFiles)
        app = self.app
        app.connect(monitor, SIGNAL("dirty(QString)"), self.slotprintme)
        
    def slotprintme(self):
        print "Changed"
        
        
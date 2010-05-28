#necessary modules
import os
import git

#Qt modules
from PyQt4.QtCore import QDir, SIGNAL, QStringList

#PyKDE4 modules
from PyKDE4.kio import KIO
from PyKDE4.kdecore import KUrl
from PyKDE4.kdeui import *

class KonfigTracker(KMainWindow):
    
    def __init__(self,app):
        KMainWindow.__init__(self)
        self.resize (640, 480)
        self.app = app
        self.initialize()
            
        
    def initialize(self):
        ''' if there exist no path, it will create
        a directory using this path, and initialize a git repository there
        '''
        #path is hardcoded. remember to change it.
        path = os.environ['HOME'] + "/konfigtracker-repo"

        if not os.access(path,os.F_OK):
            os.mkdir(path)
            self.createRepo(path)
            self.performInitImport(path)
        return True
            
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
        repo = git.Git(os.environ['HOME'] + "/konfigtracker-repo/")
        repo.execute(["git","add","."])
        self.commit()
        print "Initial Backup done."
        
    def commit(self):
        repo = git.Git(os.environ['HOME'] + "/konfigtracker-repo/")
        repo.execute(["git","commit","-a","-m","Initial Backup"])   
        
    def performInitImport(self,path):
        """
        This will perform the initial import of config files from
        .kde4/share/config to .kde4/konfigtracker-repo.
        """
        srcPath = os.environ['HOME'] + "/.kde/share/config/"
        destPath = os.environ['HOME'] + "/konfigtracker-repo/"
        dir = QDir(os.environ['HOME'] + "/.kde/share/config/")
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
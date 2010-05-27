#necessary modules
import os
import git

#Qt modules
from PyQt4.QtCore import QDir, SIGNAL

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
        #path is hardcoded for fedora 13. remember to change it.
        path = os.environ['HOME'] + "/konfigtracker-repo"

        if not os.access(path,os.F_OK):
            os.mkdir(path)
            self.createRepo(path)
            self.performInitImport(path)
            
    def createRepo(self,path):
        '''
        this will initialize a git repository in path.
        '''
        gitRepo = git.Git(path)
        gitRepo.init()
            
    def slotMessage(self):
        print "Copied!"
        repo = git.Git(os.environ['HOME'] + "/konfigtracker-repo/")
        result = repo.execute(["git","add","."])
        self.commit()

    def commit(self):
        rep = git.Git(os.environ['HOME'] + "/konfigtracker-repo/")
        res = rep.execute(["git","commit","-a","-m","Root Backup"])
    
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
        for i in entryList:
            if not i in [".","..",]:
                i = srcPath + i
                src = KUrl(i)
                dest = KUrl(destPath)
                job = KIO.copy(src, dest)
                app.connect(job, SIGNAL("finished(KJob*)"),self.slotMessage)
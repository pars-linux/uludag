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
        path = os.environ['HOME'] + "/.kde/konfigtracker-repo"

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

    def performInitImport(self,path):
        """
        This will perform the initial import of config files from
        .kde4/share/config to .kde4/konfigtracker-repo.
        """
        srcPath = "file://" + os.environ['HOME'] + "/.kde/share/config/"
        destPath = KUrl("file://" + os.environ['HOME'] + "/.kde/konfigtracker-repo/")
        dir = QDir(os.environ['HOME'] + "/.kde/share/config/")
        entryList = dir.entryList()
        for i in entryList:
            i = srcPath+i
            print i
        #copying the files from source to destination.
        app = self.app
        for i in entryList:
            src = KUrl(i)
            job = KIO.copy(src, destPath)
            app.connect(app, SIGNAL("result(KJob*)"),self.slotMessage)
            
    
        
        
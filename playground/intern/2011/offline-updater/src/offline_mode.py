#!/usr/bin/python
# -*- coding: utf-8 -*-


import pisi.db
import cPickle
from PyQt4 import QtCore, QtGui

from ui_offline import Ui_Offline 

class Offline(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_Offline()
        self.ui.setupUi(self)
        
        self.ui.pb_action.clicked.connect(self.createFiles)
        self.ui.pb_close.clicked.connect(self.close)
        
    def createFiles(self):
       
        import math
        print "pisi connection"
        installdb = pisi.db.installdb.InstallDB()
        repodb = pisi.db.repodb.RepoDB()
        repo_urls = repodb.list_repo_urls()
        repos = repodb.list_repos()
        packagedb = pisi.db.packagedb.PackageDB()
        listPackages = installdb.list_installed()
        #print int((len(listPackages)+len(repos))/100)
        cnt = 0
        packages = {}
        for i in listPackages:
            packages[installdb.get_package(i).name] = (installdb.get_package(i).release, 
                                                       packagedb.get_package_repo(installdb.get_package(i).name)[1], installdb.get_package(i).version)
            if cnt == len(listPackages)/100:
                self.ui.progressBar.setValue(self.ui.progressBar.value()+math.ceil(100/float(len(listPackages))))
                cnt = 0
                print self.ui.progressBar.value()
            cnt +=1
            QtGui.QApplication.processEvents()
           
        #print packages
        
        filePackages = open("packageList.ofu","w")
        cPickle.dump(packages, filePackages, protocol=0)
        filePackages.close()
       
        repo_list = {}
        i = 0
        cnt = 0
        #print "repo başlar"
        for repo in repos:
            repo_list[repo] = repo_urls[i]
            i += 1
            if cnt == len(repos)/100:
                self.ui.progressBar.setValue(self.ui.progressBar.value()+math.ceil(100/float(len(repos))))
                cnt=0
            cnt += 1
            QtGui.QApplication.processEvents()
        
        
        fileRepos = open("repoList.ofu","w")
        cPickle.dump(repo_list, fileRepos, protocol = 0)
        fileRepos.close()
            
        print repo_list
        self.ui.progressBar.setValue(100)
        
            

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    OfflineMode = Offline()
    OfflineMode.show()
    sys.exit(app.exec_())
    
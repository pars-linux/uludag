#!/usr/bin/python
# -*- coding: utf-8 -*-


import pisi.db
import cPickle
import os
from PyQt4 import QtCore, QtGui

from ui_offline import Ui_Offline 

class Offline(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_Offline()
        self.ui.setupUi(self)
        
        self.ui.pb_close.clicked.connect(self.close)
        self.ui.rb_export.setChecked(True)
        self.mode = 1 #Program has two modes; 1: Export , 2:Setup 
        
        self.ui.rb_export.clicked.connect(self.rbExportClickedAction)
        self.ui.rb_setup.clicked.connect(self.rbSetupClickedAction)
        self.ui.le_path_export.setText(os.getenv('USERPROFILE') or os.getenv('HOME'))
        self.ui.le_path_setup.setText(os.getenv('USERPROFILE') or os.getenv('HOME'))
        self.ui.pb_path_export.clicked.connect(self.setExportPath)
        self.ui.pb_path_setup.clicked.connect(self.setSetupPath)
        self.ui.pb_action.clicked.connect(self.startProgress)
        
        self.rbExportClickedAction()
        
        
    def createFiles(self):
       
        import math
        #print "pisi connection"
        #self.ui.updateListWidget("PiSi baglantisi saglaniyor")
        installdb = pisi.db.installdb.InstallDB()
        repodb = pisi.db.repodb.RepoDB()
        repo_urls = repodb.list_repo_urls()
        repos = repodb.list_repos()
        packagedb = pisi.db.packagedb.PackageDB()
        listPackages = installdb.list_installed()
        #print int((len(listPackages)+len(repos))/100)
        cnt = 0
        
        packages = {}
        #self.ui.updateListWidget("Paket listesi olusturuluyor")
        for i in listPackages:
            packages[installdb.get_package(i).name] = (installdb.get_package(i).release, 
                                                       packagedb.get_package_repo(installdb.get_package(i).name)[1], 
                                                       installdb.get_package(i).version)
            if cnt == len(listPackages)/100:
                self.ui.progressBar.setValue(self.ui.progressBar.value()+math.ceil(100/float(len(listPackages))))
                cnt = 0
                print self.ui.progressBar.value()
            cnt +=1
            QtGui.QApplication.processEvents()
           
        filePackages = open("packageList.ofu","w")
        cPickle.dump(packages, filePackages, protocol=0)
        filePackages.close()
       
        repo_list = {}
        i = 0
        cnt = 0
        #self.ui.updateListWidget("Depo listesi olusturuluyor")
        for repo in repos:
            repo_list[repo] = repo_urls[i]
            i += 1
            if cnt == len(repos)/100:
                self.ui.progressBar.setValue(self.ui.progressBar.value()+math.ceil(100/float(len(repos))))
                cnt=0
            cnt += 1
            QtGui.QApplication.processEvents()
        
        #self.ui.updateListWidget("Depo listesi kaydediliyor")
        fileRepos = open("repoList.ofu","w")
        cPickle.dump(repo_list, fileRepos, protocol = 0)
        fileRepos.close()
            
        #print repo_list
        self.ui.progressBar.setValue(100)
        #self.ui.updateListWidget("Islem tamamlandi")
        
        
    def setupPackages(self):
        packageList = []
        for dirname, dirnames, filenames in os.walk('packages'):
            for filename in filenames:
                if filename.split(".")[-1] == "pisi":
                    packageList.append("packages/"+filename)
                    
        if len(packageList) == 0:
            self.errorMessage("Paket Bulunamadi", "Belirttiginiz dizinde kurulacak PiSi paketi bulunamdi!")
            return
        
        command = "pm-install "
        for i in packageList:
            command+= i+" " 
            
        print command 
        os.system(command)
        
        
    def rbExportClickedAction(self):
        self.ui.le_path_setup.setEnabled(False)
        self.ui.pb_path_setup.setEnabled(False)
        
        self.ui.le_path_export.setEnabled(True)
        self.ui.pb_path_export.setEnabled(True)
        self.mode = 1
        
    def rbSetupClickedAction(self):
        self.ui.le_path_setup.setEnabled(True)
        self.ui.pb_path_setup.setEnabled(True)
        
        self.ui.le_path_export.setEnabled(False)
        self.ui.pb_path_export.setEnabled(False)
        self.mode = 2
        
        
    def startProgress(self):
        if self.mode == 1:
            self.createFiles()
        elif self.mode == 2:
            self.setupPackages()
            
            
    def setExportPath(self):
        fd = QtGui.QFileDialog(self)
        self.path_export = fd.getExistingDirectory(parent=None, caption="Klasor sec", directory=self.ui.le_path_export.text(), options=QtGui.QFileDialog.ShowDirsOnly)
        self.ui.le_path_export.setText(self.path_export)
    
    def setSetupPath(self):
        fd = QtGui.QFileDialog(self)
        self.path_setup = fd.getExistingDirectory(parent=None, caption="Klasor sec", directory=self.ui.le_path_setup.text(), options=QtGui.QFileDialog.ShowDirsOnly)
        self.ui.le_path_setup.setText(self.path_setup)
            
            
    def errorMessage(self, header, message):
        QtGui.QMessageBox.critical(self,
                                        header,
                                        message)
        return False
        
            

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    OfflineMode = Offline()
    OfflineMode.show()
    sys.exit(app.exec_())
    
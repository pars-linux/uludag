#ifndef MAIN.PY
#define MAIN.PY
#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmlrpclib
from BugReporterUI import Ui_BugReporter
from BugReporter import Bugs
import sys,os,subprocess
from PyQt4 import QtCore, QtGui
import tempfile

class Main:
    def __init__(self):
        # Bug Data
        self.productList = []
        self.ui = None
        self.app = None
        self.bugs = Bugs()
        self.bugid= -1
        self.buginfo = []
        self.selectedindex = -1
        self.sysInfo = None
        self.userInfo = None



	    #create temporary directory for generic and specific command outpus
        self.tmpDir = tempfile.mkdtemp()

        self.genericCmdList = list()

        self.genericCmdList.append(['dmesg','dmesg.txt'])
        self.genericCmdList.append(['lspci -nnvv','lspci-nnvv.txt'])
        self.genericCmdList.append(['lsusb','lsusb.txt'])
        self.genericCmdList.append(['lsmod','lsmod.txt'])
        self.genericCmdList.append(['uname -a','uname-a.txt'])
        self.genericCmdList.append(['free -m','free-m.txt'])
        self.genericCmdList.append(['pisi lr','pisi-lr.txt'])

        self.genericLogList = list()

        self.genericLogList.append(['/proc/cmdline','proc-cmdline'])

        self.buginfo = list()
        self.buginfo.append({'productname':'Display','commandlist':self.genericCmdList[:],'loglist':self.genericLogList[:]})
        self.buginfo.append({'productname':'Storage','commandlist':self.genericCmdList[:],'loglist':self.genericLogList[:]})
        self.buginfo.append({'productname':'Sound/Audio','commandlist':self.genericCmdList[:],'loglist':self.genericLogList[:]})
        self.buginfo.append({'productname':'Other','commandlist':self.genericCmdList[:],'loglist':self.genericLogList[:]})

        #Display specific log and commands
        if os.path.exists('/var/log/Xorg.0.log'):
            self.buginfo[0]['loglist'].append(['/var/log/Xorg.0.log','var-log-xorg-0-log.txt'])

        if os.path.exists('/var/log/Xorg.0.log.old'):
            self.buginfo[0]['loglist'].append(['/var/log/Xorg.0.log.old','var-log-xorg-0-log-old.txt'])

        if os.path.exists('/var/log/Xorg.1.log'):
            self.buginfo[0]['loglist'].append(['/var/log/Xorg.1.log','var-log-xorg-1-log.txt'])

        if os.path.exists('/var/log/Xorg.1.log.old'):
            self.buginfo[0]['loglist'].append(['/var/log/Xorg.1.log.old','var-log-xorg-1-log-old.txt'])

        if os.path.exists(os.getenv('HOME')+'/.xsession-errors'):
            self.buginfo[0]['loglist'].append([os.getenv('HOME')+'/.xsession-errors','xsession-errors.txt'])


        #Storage specific log and commands
        self.buginfo[1]['commandlist'].append(['blkid','blkid.txt'])
        self.buginfo[1]['commandlist'].append(['fdisk -l','fdisk-l.txt'])

        if os.path.exists('/boot/grub/grub.conf'):
            self.buginfo[1]['loglist'].append(['/boot/grub/grub.conf','boot-grub-grub-conf.txt'])
        if os.path.exists('/proc/mounts'):
            self.buginfo[1]['loglist'].append(['/proc/mounts','proc-mounts.txt'])

        print 'tempdir = ' + self.tmpDir

    def getLogsIntoTempDir(self,bugtype):
        for log in self.buginfo[bugtype]['loglist']:
            print log
            subprocess.call('cp '+log[0]+' '+self.tmpDir+'/'+log[1],shell=True)

        for cmd in self.buginfo[bugtype]['commandlist']:
            print cmd
            subprocess.call(cmd[0]+' > '+self.tmpDir+'/'+cmd[1],shell=True)


    def goto_next_page(self):
        index = self.ui.stackedWidget.currentIndex()
        index = index + 1
        if index == 3:
            self.previewBug()
        self.ui.stackedWidget.setCurrentIndex(index)

    def goto_prev_page(self):
        index = self.ui.stackedWidget.currentIndex()
        if index==5:
            index = index-2
        else:
            index = index - 1
        self.ui.stackedWidget.setCurrentIndex(index)

    def create_actions(self):
        self.ui.btnNextPage1.clicked.connect(self.goto_next_page)
        self.ui.btnNextPage2.clicked.connect(self.goto_next_page)
        self.ui.btnNextPage3.clicked.connect(self.goto_next_page)
        self.ui.btnBackPage2.clicked.connect(self.goto_prev_page)
        self.ui.btnBackPage3.clicked.connect(self.goto_prev_page)
        self.ui.btnBackPage4.clicked.connect(self.goto_prev_page)
        self.ui.btnBackPage6.clicked.connect(self.goto_prev_page)
        self.ui.btnCancelPage1.clicked.connect(self.quit_window)
        self.ui.btnSendPage4.clicked.connect(self.sendBug)
    def quit_window(self):
        sys.exit()

    def show(self):
        # Creates actions by assigning signals to slots
        self.app = QtGui.QApplication(sys.argv)
        BugReporter = QtGui.QMainWindow()
        self.ui = Ui_BugReporter()
        self.ui.setupUi(BugReporter)
        self.create_actions()
        self.createProducts()
        BugReporter.show()
        sys.exit(self.app.exec_())

    def createProducts(self):
        # Produce info about bugs
        self.productList.append(self.ui.rbDisplay)
        self.productList.append(self.ui.rbStorage)
        self.productList.append(self.ui.rbSoundAudio)
        self.productList.append(self.ui.rbOthers)

    def setProduct(self):
        '''
        sets selected product
        '''
        for but in self.productList:
            if but.isChecked():
               self.selectedindex = self.productList.index(but)
    def getProduct(self):
        '''
        returns selected product name
        '''
        product = self.buginfo[self.selectedindex]['productname']
        return product
    
    def get_sys_info(self):
        '''
        returns a data type of dict containing system information to be sent to the bug
        platform 
        '''
        import platform
        data = {}
        #find component
        component = "unspecified"
        data['component'] = component

        # find version
        version = platform.dist()[1]
        if "Kurumsal" in version or "Corporate" in version:
            substr = version.split(" ")
            version = "Corporate"+substr[1]
        else :
            substr = version.split(".")
            version = substr[0]
        data['version'] = version

        #find platform
        plat = platform.uname()[4]
        data['platform'] = plat

        return data

    def previewBug(self):
        '''
        Preview the bug information
        '''
        # set User Info
        self.setProduct()
        self.userInfo= {}
        self.userInfo['product'] = self.getProduct()
        self.userInfo['summary'] = str(self.ui.txtSummary.toPlainText())
        self.userInfo['description'] = str(self.ui.txtDetails.toPlainText()) +  "\n" + str(self.ui.txtSteps.toPlainText())
        # set system Info
        self.sysInfo = {} 
        self.sysInfo = self.get_sys_info()
	
	# run commands and copy outputs to temp directory
	self.getLogsIntoTempDir(self.selectedindex)



        self.ui.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("BugReporter", "Fields", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.treeWidget.headerItem().setText(1, QtGui.QApplication.translate("BugReporter", "Data", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.ui.treeWidget.isSortingEnabled()
        self.ui.treeWidget.setSortingEnabled(False)
        self.ui.treeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("BugReporter", "Architecture", None, QtGui.QApplication.UnicodeUTF8))


        self.ui.treeWidget.topLevelItem(0).child(0).setText(0, QtGui.QApplication.translate("BugReporter", "OS", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.treeWidget.topLevelItem(0).child(0).setText(1, QtGui.QApplication.translate("BugReporter", "Pardus " + self.sysInfo['version'], None, QtGui.QApplication.UnicodeUTF8))
       
       
       
        self.ui.treeWidget.topLevelItem(0).child(1).setText(0, QtGui.QApplication.translate("BugReporter", "Platform", None , QtGui.QApplication.UnicodeUTF8))
        
        self.ui.treeWidget.topLevelItem(0).child(1).setText(1, QtGui.QApplication.translate("BugReporter", self.sysInfo['platform'], None , QtGui.QApplication.UnicodeUTF8))



        self.ui.treeWidget.topLevelItem(1).setText(0, QtGui.QApplication.translate("BugReporter", "User Data", None, QtGui.QApplication.UnicodeUTF8))


        self.ui.treeWidget.topLevelItem(1).child(0).setText(0, QtGui.QApplication.translate("BugReporter", "Problem Type", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.treeWidget.topLevelItem(1).child(0).setText(1, QtGui.QApplication.translate("BugReporter", self.userInfo['product'], None, QtGui.QApplication.UnicodeUTF8))


        self.ui.treeWidget.topLevelItem(1).child(1).setText(0, QtGui.QApplication.translate("BugReporter", "Summary", None, QtGui.QApplication.UnicodeUTF8)) 

        self.ui.treeWidget.topLevelItem(1).child(1).setText(1, QtGui.QApplication.translate("BugReporter", self.userInfo['summary'], None, QtGui.QApplication.UnicodeUTF8))

        
        self.ui.treeWidget.topLevelItem(1).child(2).setText(0, QtGui.QApplication.translate("BugReporter", "Description", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.treeWidget.topLevelItem(1).child(2).setText(1, QtGui.QApplication.translate("BugReporter", self.userInfo['description'], None, QtGui.QApplication.UnicodeUTF8))
       
        self.ui.treeWidget.topLevelItem(2).setText(0, QtGui.QApplication.translate("BugReporter", "System Data", None, QtGui.QApplication.UnicodeUTF8))
	self.ui.treeWidget.topLevelItem(2).child(0).setText(0, QtGui.QApplication.translate("BugReporter", "Command Outputs", None, QtGui.QApplication.UnicodeUTF8))    
	
	i=0
	for elem in self.buginfo[self.selectedindex]['commandlist']:
	    item_0 = QtGui.QTreeWidgetItem(self.ui.treeWidget.topLevelItem(2).child(0))
	    item_0.setText(0, QtGui.QApplication.translate("BugReporter", elem[0] , None, QtGui.QApplication.UnicodeUTF8))
	    item_0.setText(1, QtGui.QApplication.translate("BugReporter", self.tmpDir + '/' + elem[1], None, QtGui.QApplication.UnicodeUTF8))
        i += 1


	self.ui.treeWidget.topLevelItem(2).child(1).setText(0, QtGui.QApplication.translate("BugReporter", "Log Files", None, QtGui.QApplication.UnicodeUTF8))    
	i=0
	for elem in self.buginfo[self.selectedindex]['loglist']:
	    item_1 = QtGui.QTreeWidgetItem(self.ui.treeWidget.topLevelItem(2).child(1))
	    item_1.setText(0, QtGui.QApplication.translate("BugReporter", elem[0] , None, QtGui.QApplication.UnicodeUTF8))    
	    item_1.setText(1, QtGui.QApplication.translate("BugReporter", self.tmpDir + '/' + elem[1], None, QtGui.QApplication.UnicodeUTF8))
        i += 1
       
       
        self.ui.treeWidget.setSortingEnabled(__sortingEnabled)
   def isLoggedIn(self):
       bz_url = self.bugs.getBuzillaURL()
       if os.path.exists(os.getenv('HOME')+'/.bugzillacookies'):
           cookieFile = open(os.getenv('HOME')+'/.bugzillacookies')
           content = cookieFile.read()
           domain = bz_url.split('/')[2]
           if content.contains('domain="'+domain+'"') == -1 :
               #not logged in
               return False
           else:
               return True
        else:
            return False

    def sendBug(self):
        if isLoggedIn() == False :
            #skip to login screen

        try:
            r = self.bugs.createbug(self.userInfo,self.sysInfo)
            self.bugid = str(r).split(' ')[0].split('#')[1]
        except xmlrpclib.Fault,e:
            print str(e)
            self.bugid=-1
        self.attachbug()

    def run(self, cmd, logfile):
        '''
        Execute given commands and redirect them to a file named as 'commandname' + '.txt'
        File name is given as a parameter to the function 
        '''
        import os
        cmd = cmd + " > " + logfile
        os.system(cmd)
    def attachbug(self):
        '''
        '''
        import dircache
        if self.bugid and self.bugid < 0:
            return
        for fname in dircache.listdir(self.tmpDir):
            fdesc = fname
            self.bugs.attach_file(self.bugid,self.tmpDir + "/" + fname,fdesc)
if __name__ == "__main__":
    m=Main()
    m.show()

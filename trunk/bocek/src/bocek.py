#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# Python Modules
import os
import sys
import time
import consts
import subprocess
import mail
import bugzilla

# GUI
from gui import *
from khtml import *

version = '0.2'

def AboutData():
    about_data = KAboutData('bocek',
                            'Bocek',
                            version,
                            'Bocek Bug Report Interface',
                            KAboutData.License_GPL,
                            '(C) 2007 UEKAE/TÜBİTAK',
                            None, None,
                            'gokmen@pardus.org.tr')
    about_data.addAuthor('Gökmen GÖKSEL', None, 'gokmen@pardus.org.tr')
    return about_data

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(i18n('Bocek Bug Report Interface'))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 300)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)
        if os.environ['LANG'].startswith('tr_TR'):
            self.htmlPart.openURL(KURL(locate('data', 'bocek/help/tr/main_help.html')))
        else:
            self.htmlPart.openURL(KURL(locate('data', 'bocek/help/en/main_help.html')))

class Bocek(BocekForm):
    def __init__(self, parent=None, name=None):
        BocekForm.__init__(self, parent, name)
        self.connect(self.buttonSave, SIGNAL('clicked()'), self.buildReport)
        self.connect(self.buttonSend, SIGNAL('clicked()'), self.sendReport)
        self.connect(self.buttonHelp, SIGNAL('clicked()'), self.slotHelp)
        self.connect(guiApp, SIGNAL("shutDown()"), self.slotQuit)
        os.environ['LC_ALL'] = 'C'
        self.lastReportFile=''
        self.bugzilla = bugzilla.bugzilla()
        
    def slotQuit(self):
        self.deleteLater()
        guiApp.quit()

    def buildReport(self):
        if (self.checkNeeds()) and (len(self.getCheckedLogs())>0):
            self.setCursor(Qt.waitCursor)
            self.output=""
            self.updateInfo("Please wait while collecting informations ..")
            checkedLogs = self.getCheckedLogs()
            self.output+="Summary : %s \n" % self.lineSummary.text()
            self.output+="Details : %s \n" % self.lineDetails.text()
            self.output+="\nAdditional Files : \n%s\n"%("*"*40)
            self.progressBar.show()
            size=0
            for logs in checkedLogs:
                size+=len(logs)
            per = 100 / size
            for logs in checkedLogs:
                for log in logs:
                    self.output+="\n========» %s «========\n" % log
                    self.updateInfo("Now getting : %s"%log)
                    if logs[log]==1:
                        self.output+=self.getStaticOutput(log)
                    elif logs[log]==2:
                        self.output+=self.getCommandOutput(log)
                    self.output+="\n"
                    self.updateProgress(per)
            self.progressBar.setProgress(100)
            self.lastReportFile = self.writeReport()
            self.updateInfo("Report saved as %s "%self.lastReportFile)
            self.setCursor(Qt.arrowCursor)
        elif not len(self.getCheckedLogs())>0:
            self.showInfo("Nothing to save")

    def updateInfo(self,msg):
        self.labelStatus.setText(msg)
        guiApp.processEvents(QEventLoop.ExcludeUserInput)

    def updateProgress(self,percent):
        self.progressBar.setProgress(self.progressBar.progress()+percent)
        self.progressBar.update()
        guiApp.processEvents(QEventLoop.ExcludeUserInput)

    def sendReport(self):
        if self.checkNeeds():
            self.setCursor(Qt.waitCursor)
            files=[]
            if (not self.lastReportFile) and (len(self.getCheckedLogs())>0):
                self.buildReport()
            """
            picPath = str(self.picturePath.lineEdit().text())
            if not picPath=="":
                if os.path.exists(picPath):
                    if os.stat(picPath).st_size < (consts.pictureMaxSize * 1000):
                        files.append(picPath)
            """
            if not self.lastReportFile=="":
                files.append(self.lastReportFile)
            self.updateInfo("Sending bug report... Please wait.")
            # we will use bugzilla instead of mail way..
            result = self.bugzilla.sendBug(str(self.lineEmail.text()),
                                           str(self.linePassword.text()),
                                           str(self.lineSummary.text()),
                                           str(self.lineDetails.text()))
            self.showInfo(result)
            self.updateInfo(result)

            self.lastReportFile=""
        self.setCursor(Qt.arrowCursor)

    def writeReport(self):
        now = time.localtime()
        filename = '/tmp/BugReport.%s-%s-%s.txt' % (now[2],now[3],now[4])
        link = file(filename,'w')
        link.writelines(self.output)
        link.close()
        return filename

    def takeScreen(self):
        self.updateInfo("Taking screenshot...")
        now = time.localtime()
        filename = '/tmp/BugScreenShot.%s-%s-%s.png' % (now[2],now[3],now[4])
        if os.system("import -window root -colors 8 +dither %s" % filename) == 0:
            self.showInfo("Screenshot saved")
            self.picturePath.lineEdit().setText(filename)
            self.updateInfo("Screenshot saved as %s"%filename)

    def checkNeeds(self):
        if (self.lineSummary.text()=="") or (self.lineDetails.text()==""):
            self.showError("Bug reports must have Summary and Details")
            return False
        return True

    def showError(self,msg):
        KMessageBox.sorry(self,msg,"Error")

    def showInfo(self,msg):
        KMessageBox.information(self,msg,"Info")

    def getStaticOutput(self,filename):
        try:
            ret=file(filename,'r').read()
        except:
            ret="»ERR» FILE NOT FOUND !!\n"
        return ret

    def getCommandOutput(self,cmd):
        a = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "".join(a.communicate())

    def getCheckedLogs(self):
        ret=[]
        if self.checkBoxPackages.isChecked():
            ret.append(consts.packageInfo)
        if self.checkBoxConfig.isChecked():
            ret.append(consts.configFiles)
        if self.checkBoxHardware.isChecked():
            ret.append(consts.hardwareInfo)
        if self.checkBoxStandartLogs.isChecked():
            ret.append(consts.standartLogs)
        return ret

    def slotHelp(self):
        self.helpwin = HelpDialog(self)
        self.helpwin.show()

if __name__=="__main__":
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    guiApp = KApplication(sys.argv,"")
    mainForm = Bocek()
    guiApp.setMainWidget(mainForm)
    sys.exit(mainForm.exec_loop())

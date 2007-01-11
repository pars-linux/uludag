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

# GUI
from gui import *
from khtml import *

version = '0.1'

def AboutData():
    about_data = KAboutData('bocek',
                            'Bocek',
                            version,
                            'Bocek Bug Repoert Interface',
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
        self.connect(self.buttonTakScr, SIGNAL('clicked()'), self.takeScreen)
        self.connect(guiApp, SIGNAL("shutDown()"), self.slotQuit)
        os.environ['LC_ALL'] = 'C'
        self.lastReportFile=''

    def slotQuit(self):
        self.deleteLater()
        guiApp.quit()

    def buildReport(self):
        self.output=""
        self.labelStatus.setText("Please wait while collecting informations ..")
        checkedLogs = self.getCheckedLogs()
        # self.output ="From : %s (%s) at %s\n"%(lineEmail.text(),getIp,time)
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
                if logs[log]==1:
                    self.output+=self.getStaticOutput(log)
                elif logs[log]==2:
                    self.output+=self.getCommandOutput(log)
                self.output+="\n"
                self.progressBar.setProgress(self.progressBar.progress()+per)
                self.progressBar.update()
        self.progressBar.setProgress(100)
        self.lastReportFile = self.writeReport()

    def sendReport(self):
        if not self.lastReportFile:
            self.buildReport()
        files = [self.lastReportFile]
        picPath = str(self.picturePath.lineEdit().text())
        if not picPath=="":
            if os.path.exists(picPath):
                if os.stat(picPath)[6] < (consts.pictureMaxSize * 1000):
                    files.append(picPath)
        if mail.send_mail(str(self.lineEmail.text()),
                          ["gokmen@pardus.org.tr"],
                          str(self.lineSummary.text()),
                          str(self.lineDetails.text()),
                          files):
            print "Message sent."
        else:
            print "Error on message sending"

        self.lastReportFile=""

    def writeReport(self):
        now = time.localtime()
        filename = '/tmp/BugReport.%s-%s-%s.txt' % (now[2],now[3],now[4])
        link = file(filename,'w')
        link.writelines(self.output)
        link.close()
        return filename

    def takeScreen(self):
        now = time.localtime()
        filename = '/tmp/BugScreenShot.%s-%s-%s.png' % (now[2],now[3],now[4])
        if os.system("import -window root -colors 8 +dither %s" % filename) == 0:
            print "screenshot saved."
            self.picturePath.lineEdit().setText(filename)

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

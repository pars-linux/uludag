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
        self.connect(self.buttonHelp, SIGNAL('clicked()'), self.slotHelp)
        self.connect(guiApp, SIGNAL("shutDown()"), self.slotQuit)

    def slotQuit(self):
        self.deleteLater()
        guiApp.quit()

    def buildReport(self):
        pass

    def writeReport(self):
        now = time.localtime()
        filename = '/tmp/BugReport.%s-%s-%s.txt' % (now[2],now[3],now[4])
        link = file(filename,'w')
        link.writelines(self.output)
        link.close()
        return filename

    def getStaticOutput(self,filename):
        link = file(filename,'r')
        ret = ''
        lines = link.readlines()
        for line in lines:
            ret+=line
        link.close()
        return ret

    def getCommandOutput(self,cmd):
        return subprocess.call(cmd)

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

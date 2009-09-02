#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009, Cihan Okyay
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# System
import sys
import os
import shutil
import subprocess

# Qt Stuff
from PyQt4 import QtGui
from PyQt4 import QtCore

# PyKDE4 Stuff
from PyKDE4.kdeui import KApplication, KAboutApplicationDialog, KSystemTrayIcon, KMessageBox
from PyKDE4.kdecore import KAboutData, KCmdLineArgs

from ui_mainwindow import Ui_MainWindow
from about import *


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowTitle('Puma')
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/manager.png"))

        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def connect(self):
        subprocess.call("/usr/sbin/br2684ctl -c 0 -b -a 8.35", shell=True)
        sonuc = os.popen("/usr/sbin/adsl-start")
        sonuc = sonuc.read().lower()
        if "connected" in sonuc:
            tray.showMessage((u"Puma Info"), (u"Connected"), QtGui.QSystemTrayIcon.Information, 3000)
        else:
            tray.showMessage((u"Puma Info"), (u"Connected failed"), QtGui.QSystemTrayIcon.Information, 3000)


    # for automatic connect
#    def localstart(self):
 #       file = open("/etc/conf.d/local.start", "a")
  #      file.write("br2684ctl -c 0 -b -a 8.35\n")
   #     file.write("adsl-start\n")
    #    file.write("/usr/sbin/br2684ctl -c 0 -b -a 8.35\n")
     #   file.write("/usr/sbin/adsl-start")
      #  file.close()

    def disconnect(self):
        result = os.popen("/usr/sbin/adsl-stop")
        result = result.read().lower()
        if "disconnected" in result:
            tray.showMessage((u"Puma Info"), (u"Disconnected"), QtGui.QSystemTrayIcon.Information, 3000)
        else:
            tray.showMessage((u"Puma Info"), (u"Disconnected failed. You not connect anyway!"), QtGui.QSystemTrayIcon.Information, 3000)


    # pppoe.conf, chap-secrets and pap-secrets files
    def save(self):
        username = str(self.lineEdit.text())
        password = str(self.lineEdit_2.text())
        shutil.copyfile("/etc/ppp/pppoe.conf", "/etc/ppp/pppoe.conf-backup")
        file = open("/etc/ppp/pppoe.conf", "w")
        file.write("ETH=nas0")
        file.write("\nUSER='" + username + "'")
        file.write("\nDEMAND=no")
        file.write("\nDNSTYPE=SERVER")
        file.write("\nPEERDNS=no")
        file.write("\nDNS1=")
        file.write("\nDNS2=")
        file.write("\nDEFAULTROUTE=yes")
        file.write("\nCONNECT_TIMEOUT=30")
        file.write("\nCONNECT_POLL=2")
        file.write("\nACNAME=")
        file.write("\nSERVICENAME=")
        file.write("\nPING=" + "\"" + "." + "\"")
        file.write("\nCF_BASE=`basename $CONFIG`")
        file.write("\nPIDFILE=" +"\"" + "/var/run/$CF_BASE-pppoe.pid" +"\"")
        file.write("\nSYNCHRONOUS=no")
        file.write("\nCLAMPMSS=1412")
        file.write("\nLCP_INTERVAL=20")
        file.write("\nLCP_FAILURE=3")
        file.write("\nPPPOE_TIMEOUT=80")
        file.write("\nFIREWALL=NONE")
        file.write("\nLINUX_PLUGIN=")
        file.write("\nPPPOE_EXTRA=" + "\"" + "\"")
        file.write("\nPPPD_EXTRA=" + "\"" + "\"")
        file.close()
        shutil.copyfile("/etc/ppp/pap-secrets", "/etc/ppp/pap-secrets-backup")
        file = open("/etc/ppp/pap-secrets", "w")
        file.write("# Secrets for authentication using PAP")
        file.write("\n# client server secret IP adresses\n")
        file.write("\"" + username + "\"" + " * " + "\"" + password + "\"")
        file.close()
        shutil.copyfile("/etc/ppp/chap-secrets", "/etc/ppp/chap-secrets-backup")
        file = open("/etc/ppp/chap-secrets", "w")
        file.write("# Secrets for authentication using CHAP")
        file.write("\n# client server secret IP adresses\n")
        file.write("\"" + username + "\"" + " * " + "\"" + password + "\"")
        file.close()


    @QtCore.pyqtSignature("bool")
    def on_actionQt_About_triggered(self):
        QtGui.QMessageBox.aboutQt(self)

    @QtCore.pyqtSignature("bool")
    def on_pushButton_clicked(self):
        self.connect()

    @QtCore.pyqtSignature("bool")
    def on_actionExit_triggered(self):
        app.exit()

    @QtCore.pyqtSignature("bool")
    def on_actionAbout_triggered(self):
        KAboutApplicationDialog(aboutData, self).show()

    @QtCore.pyqtSignature("bool")
    def on_actionpushButton_2_clicked(self):
        self.close()

    @QtCore.pyqtSignature("bool")
    def on_actionSave_triggered(self):
        self.save()

    @QtCore.pyqtSignature("bool")
    def on_actionHelp_triggered(self):
        QtGui.QMessageBox.question(self,
                QtGui.QApplication.translate("MainWindow", "Help Puma"),
                QtGui.QApplication.translate("MainWindow", "Authors :\n Cihan Okyay <okyaycihan@gmail.com>\n\n Project page :\n https://sourceforge.net/projects/pumaproject/\n\n Source code : https://pumaproject.svn.sourceforge.net/svnroot/pumaproject/\n\n  Usage :\n http://pumaproject.sourceforge.net/"),
                )

    @QtCore.pyqtSignature("bool")
    def on_actionDisconnect_triggered(self):
        self.disconnect()

aboutData = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

KCmdLineArgs.init(sys.argv, aboutData)
app = KApplication()
app.setQuitOnLastWindowClosed(False)
mw = MainWindow()
mw.show()


aboutData.setProgramIconName(":/icons/icons/manager.png")
aboutData.addAuthor(ki18n("Cihan Okyay"), ki18n("Current Maintainer"), "okyaycihan@gmail.com")

def showw(event):
    if event == QtGui.QSystemTrayIcon.Trigger:
        if not mw.isVisible():
            mw.show()
        else:
            mw.hide()


from icon import *
tray = KSystemTrayIcon(QtGui.QIcon(":/icons/icons/manager.png"))
tray.show()

QtCore.QObject.connect(tray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), showw)

import pumaicons_rc

app.exec_()


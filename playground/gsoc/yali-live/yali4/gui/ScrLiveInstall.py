# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
# Copyright (C) 2010, Sarath Lakshman
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import time
import glob
import zipfile
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import pisi.ui

import yali4.fstab
import yali4.sysutils
import yali4.pisiiface
import yali4.postinstall
import yali4.localeutils

import yali4.gui.context as ctx
import yali4.partitionrequest as request
from yali4.constants import consts
from yali4.gui.descSlide import slideDesc
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.YaliDialog import QuestionDialog, EjectAndRetryDialog
from yali4.gui.Ui.installwidget import Ui_InstallWidget

EventCopy, EventSetProgress, EventError, EventAllFinished, EventPackageInstallFinished, EventRetry = range(1001,1007)

def iter_slide_pics():
    def pat(pic):
        return "%s/%s.png" % (ctx.consts.slidepics_dir, pic)

    # load all pics
    pics = []

    for slide in slideDesc:
        pic, desc = slide.items()[0]
        pics.append({"pic":QtGui.QPixmap(pat(pic)),"desc":desc})

    while True:
        for pic in pics:
            yield pic

def objectSender(pack):
    global currentObject
    QCoreApplication.postEvent(currentObject, pack)

##
# Partitioning screen.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Installing system...')
    desc = _('Installing takes approximately 20 minutes depending on your hardware...')
    icon = "iconInstall"
    help = _('''
<font size="+2">Installation started</font>

<font size="+1">

<p>
Pardus is now being installed on your hard disk. 
</p>

<p>
The duration of this operation depends on the 
capability and power of your system. Meanwhile,
you can enjoy some visual elements showing 
the distinctive properties of Pardus, your 
new operating system.
</p>

<p>
Have fun!
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_InstallWidget()
        self.ui.setupUi(self)

        self.timer = QTimer(self)
        self.timerProgress = QTimer(self)

        QObject.connect(self.timer, SIGNAL("timeout()"),self.slotChangePix)
        QObject.connect(self.timerProgress, SIGNAL("timeout()"),self.slotUpdateprogress)

        if ctx.consts.lang == "tr":
            self.ui.progress.setFormat("%%p")

        self.iter_pics = iter_slide_pics()

        # show first pic
        self.slotChangePix()

        self.total = 0
        self.cur = 0
        self.hasErrors = False

    def shown(self):
        # Disable mouse handler
        ctx.mainScreen.dontAskCmbAgain = True
        ctx.mainScreen.themeShortCut.setEnabled(False)

        # Thread object
        global currentObject
        currentObject = self

        # start installer thread
        ctx.debugger.log("LiveInstaller is creating...")
        self.live_installer = LiveInstaller()
        ctx.debugger.log("Calling LiveInstaller.start...")
        self.live_installer.start()
        ctx.yali.info.updateAndShow(_("Copying files..."))

        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()

        # start 30 seconds
        self.timer.start(1000 * 30)


    def slotUpdateprogress(self):

        current_size= int(yali4.sysutils.execWithCapture("du", ["-sc",consts.target_dir]).split()[-2])
        ctx.debugger.log("Progress: %d / %d" %(current_size, self.total))
        qevent = InstallEvent(QEvent.User, EventCopy)
        qevent.setData(current_size)
        objectSender(qevent)    

        if current_size >= self.total:

            self.timerProgress.stop()


    def customEvent(self, qevent):

        # EventCopy
        if qevent.eventType() == EventCopy:
            progress = qevent.data()
            self.ui.progress.setValue(progress)
            ctx.debugger.log("LiveInstall: Copying files")
            self.ui.info.setText(_("Copying files..."))

        # EventSetProgress
        elif qevent.eventType() == EventSetProgress:
            total = qevent.data()
            self.total = total
            self.ui.progress.setMaximum(total)
            ctx.debugger.log("Progress reporter is running.")
            self.timerProgress.start(1000 * 5)

        # EventPackageInstallFinished
        elif qevent.eventType() == EventPackageInstallFinished:
            self.packageInstallFinished()

        # EventError
        elif qevent.eventType() == EventError:
            err = qevent.data()
            self.installError(err)

        # EventRetry
        elif qevent.eventType() == EventRetry:
            package = qevent.data()
            self.timer.stop()
            ctx.yali.retryAnswer = EjectAndRetryDialog(_("Warning"),
                                                       _("Package install failed : <b>%s</b>") % package,
                                                       _("Do you want to retry ?"))

            self.timer.start(1000 * 30)
            ctx.yali.waitCondition.wakeAll()

        # EventAllFinished
        elif qevent.eventType() == EventAllFinished:
            self.finished()

    def slotChangePix(self):
        slide = self.iter_pics.next()
        self.ui.pix.setPixmap(slide["pic"])
        self.ui.desc.setText(slide["desc"])

    def packageInstallFinished(self):

        ctx.yali.fillFstab()

        # Configure Pending...
        # run baselayout's postinstall first

        ctx.yali.info.updateAndShow(_("Creating baselayout for your system!"))
        yali4.postinstall.initbaselayout()

        # postscripts depend on 03locale...
        yali4.localeutils.writeLocaleFromCmdline()

        #Write InitramfsConf
        yali4.postinstall.writeInitramfsConf()

        # run dbus in chroot
        yali4.sysutils.chrootDbus()

        #Remove Autologin for default Live user pars
        pars=yali4.users.User("pars")
        pars.setAutoLogin(False)

        #Remove autologin as root for virtual terminals
        inittablive = os.path.join(consts.target_dir,"etc/inittab")
        inittab = file(inittablive).read()
        inittab = inittab.replace("--autologin root ","")
        f = file(inittablive,"w")
        f.write(inittab)
        f.close()
    

        ctx.yali.info.updateMessage(_("Configuring packages.."))
        qevent = InstallEvent(QEvent.User, EventAllFinished)
        objectSender(qevent)


    def execute(self):
        # stop slide show
        self.timer.stop()
        return True

    def finished(self):
        if self.hasErrors:
            return
        ctx.yali.info.hide()
        # trigger next screen. will activate execute()
        ctx.mainScreen.slotNext()

    def installError(self, e):
        import yali4
        import yali4.gui.runner

        self.hasErrors = True
        err_str = _('''An error during the installation of packages occured.

This is possibly a broken Pardus CD or CD-ROM drive.

Error:
%s
''') % str(e)

        yali4.gui.runner.showException(yali4.exception_fatal, err_str)

class LiveInstaller(QThread):

    def __init__(self):
        ctx.debugger.log("LiveInstaller started.")
        QThread.__init__(self)

        self.symlink_dirs = ["bin","sbin","lib","boot","usr","opt","dev","tmp"]
        self.copy_dirs = ["etc","var","root"]
        self.empty_dirs = ["mnt","sys","proc","media","home"]
        self.symlink_basepath = os.readlink("/usr").replace("/usr","")

    def run(self):
        append_base = lambda x : self.symlink_basepath + "/"+x
        ctx.debugger.log("LiveInstaller is running.")
        self.copy_dirs.extend(map(append_base,self.symlink_dirs))


        #Calculate total size to be copied
        
        total = yali4.sysutils.execWithCapture("du", ["-sc"] + self.copy_dirs).split()[-2]
        ctx.debugger.log("Calculating total size")

        qevent = InstallEvent(QEvent.User, EventSetProgress)
        qevent.setData(int(total))
        objectSender(qevent)

        ctx.yali.mutex.lock()

        for dir in self.empty_dirs:
            yali4.sysutils.run("mkdir %s/%s" %(consts.target_dir, dir))

        for dir in self.copy_dirs:
            yali4.sysutils.run("cp -Rp /%s %s" %(dir,consts.target_dir))
        qevent = InstallEvent(QEvent.User, EventPackageInstallFinished)
        objectSender(qevent)


class InstallEvent(QEvent):

    def __init__(self, _, event):
        QEvent.__init__(self, _)
        self.event = event

    def eventType(self):
        return self.event

    def setData(self,data):
        self._data = data

    def data(self):
        return self._data


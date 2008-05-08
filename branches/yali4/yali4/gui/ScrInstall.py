# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import glob

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import pisi.ui

import yali4.pisiiface
import yali4.fstab
import yali4.postinstall
import yali4.sysutils
import yali4.localeutils
import yali4.partitionrequest as request
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.installwidget import Ui_InstallWidget
import yali4.gui.context as ctx

EventPisi, EventSetProgress, EventError, EventAllFinished, EventPackageInstallFinished = range(1001,1006)

def iter_slide_pics():
    # load all pics
    pics = []
    g = glob.glob(ctx.consts.slidepics_dir + "/*.png")
    g.sort()
    for p in g:
        pics.append(QtGui.QPixmap(p))

    while True:
        for pic in pics:
            yield pic

##
# Partitioning screen.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Installing system..')
    desc = _('Installing approximately 30 minutes depending on hardware..')
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
        QObject.connect(self.timer, SIGNAL("timeout()"),self.slotChangePix)

        self.iter_pics = iter_slide_pics()

        # show first pic
        self.slotChangePix()

        self.total = 0
        self.cur = 0
        self.hasErrors = False

    def shown(self):
        # start installer thread
        ctx.debugger.log("PkgInstaller is creating...")
        self.pkg_installer = PkgInstaller(self)
        ctx.debugger.log("Calling PkgInstaller.start...")
        self.pkg_installer.start()
        ctx.yali.info.updateAndShow(_("Packages are installing.."), True)

        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()

        # start 30 seconds
        self.timer.start(1000 * 30)

    def customEvent(self, qevent):

        # EventPisi
        if qevent.eventType() == EventPisi:
            p, event = qevent.data()

            if event == pisi.ui.installing:
                self.ui.info.setText(_("Installing: %s<br>%s") % (p.name, p.summary))
                ctx.debugger.log("Pisi : %s installing" % p.name)
                self.cur += 1
                self.ui.progress.setValue(self.cur)
            elif event == pisi.ui.configuring:
                self.ui.info.setText(_("Configuring package: %s") % p.name)
                ctx.debugger.log("Pisi : %s configuring" % p.name)
                self.cur += 1
                self.ui.progress.setValue(self.cur)

        # EventSetProgress
        elif qevent.eventType() == EventSetProgress:
            total = qevent.data()
            self.ui.progress.setMaximum(total)

        # EventPackageInstallFinished
        elif qevent.eventType() == EventPackageInstallFinished:
            self.packageInstallFinished()

        # EventError
        elif qevent.eventType() == EventError:
            err = qevent.data()
            self.installError(err)

        # EventAllFinished
        elif qevent.eventType() == EventAllFinished:
            self.finished()

    def slotChangePix(self):
        self.ui.pix.setPixmap(self.iter_pics.next())

    def packageInstallFinished(self):

        self.cur = 0
        ctx.yali.fillFstab()

        # Configure Pending...
        # run baselayout's postinstall first

        ctx.yali.info.updateAndShow(_("Creating baselayout for your system!"))
        yali4.postinstall.initbaselayout()

        # postscripts depend on 03locale...
        yali4.localeutils.write_locale_from_cmdline()

        # run dbus in chroot
        yali4.sysutils.chroot_dbus()

        ctx.yali.info.updateMessage(_("Configuring packages.."), True)

        # start configurator thread
        self.pkg_configurator = PkgConfigurator(self)
        self.pkg_configurator.start()

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

class PkgInstaller(QThread):

    def __init__(self, widget):
        ctx.debugger.log("PkgInstaller started.")
        QThread.__init__(self)
        self._widget = widget

    def run(self):
        ctx.debugger.log("PkgInstaller is running.")
        ui = PisiUI(self._widget)

        yali4.pisiiface.initialize(ui)

        # if exists use remote source repo
        # otherwise use cd as repo
        ctx.debugger.log("CD Repo adding..")
        if ctx.installData.repoAddr:
            yali4.pisiiface.add_remote_repo(ctx.installData.repoName,ctx.installData.repoAddr)
        else:
            yali4.pisiiface.add_cd_repo()

        # show progress
        total = yali4.pisiiface.get_available_len()
        ctx.debugger.log("Creating PisiEvent..")
        qevent = PisiEvent(QEvent.User, EventSetProgress)
        ctx.debugger.log("Setting data on just created PisiEvent (EventSetProgress)..")
        qevent.setData(total)
        ctx.debugger.log("Posting PisiEvent to the widget..")
        QCoreApplication.postEvent(self._widget, qevent)
        ctx.debugger.log("Found %d packages in repo.." % total)

        try:
            yali4.pisiiface.install_all()
        except Exception, e:
            # User+10: error
            qevent = PisiEvent(QEvent.User, EventError)
            qevent.setData(e)
            QCoreApplication.postEvent(self._widget, qevent)

        # Package Install finished lets configure them
        qevent = PisiEvent(QEvent.User, EventPackageInstallFinished)
        QCoreApplication.postEvent(self._widget, qevent)

class PkgConfigurator(QThread):

    def __init__(self, widget):
        ctx.debugger.log("PkgConfigurator started.")
        QThread.__init__(self)
        self._widget = widget

    def run(self):
        ctx.debugger.log("PkgConfigurator is running.")
        ui = PisiUI(self._widget)

        yali4.pisiiface.initialize(ui=ui, with_comar=True)

        total = yali4.pisiiface.get_pending_len()
        qevent = PisiEvent(QEvent.User, EventSetProgress)
        qevent.setData(total)
        QCoreApplication.postEvent(self._widget, qevent)

        try:
            # run all pending...
            ctx.debugger.log("exec : yali4.pisiiface.configure_pending() called")
            yali4.pisiiface.configure_pending()
        except Exception, e:
            # User+10: error
            qevent = PisiEvent(QEvent.User, EventError)
            qevent.setData(e)
            QCoreApplication.postEvent(self._widget, qevent)

        # Remove cd repository and install add real
        yali4.pisiiface.switch_to_pardus_repo()

        qevent = PisiEvent(QEvent.User, EventAllFinished)
        QCoreApplication.postEvent(self._widget, qevent)

class PisiUI(QObject,pisi.ui.UI):

    def __init__(self, widget, *args):
        pisi.ui.UI.__init__(self)
        apply(QObject.__init__, (self,) + args)
        self.w = widget

    def notify(self, event, **keywords):
        if event == pisi.ui.installing or event == pisi.ui.configuring:
            qevent = PisiEvent(QEvent.User, EventPisi)
            data = [keywords['package'], event]
            qevent.setData(data)
            QCoreApplication.postEvent(self.w, qevent)

    def display_progress(self, operation, percent, info, **keywords):
        pass

class PisiEvent(QEvent):

    def __init__(self, _, event):
        QEvent.__init__(self, _)
        self.event = event

    def eventType(self):
        return self.event

    def setData(self,data):
        self._data = data

    def data(self):
        return self._data


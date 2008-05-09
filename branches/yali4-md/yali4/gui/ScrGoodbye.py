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

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import dbus
import time
import yali4.sysutils
import yali4.users
import yali4.localeutils
import yali4.postinstall
import yali4.bootloader
import yali4.storage
import yali4.partitionrequest as partrequest
import yali4.partitiontype as parttype
from os.path import basename
from yali4.sysutils import is_windows_boot
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.YaliDialog import WarningDialog
from yali4.gui.YaliSteps import YaliSteps
from yali4.gui.Ui.goodbyewidget import Ui_GoodByeWidget
import yali4.gui.context as ctx

YALI_INSTALL, YALI_FIRSTBOOT, YALI_OEMINSTALL, YALI_PARTITIONER = range(4)

##
# Goodbye screen
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Goodbye from YALI')
    desc = _('Enjoy your freash Pardus !..')
    help = _('''
<font size="+2">Congratulations</font>


<font size="+1">
<p>
You have successfully installed Pardus, a very easy to use desktop system on
your machine. Now you can start playing with your system and stay productive
all the time.
</p>
<P>
Click on the Next button to proceed. One note: You remember your password,
don't you?
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_GoodByeWidget()
        self.ui.setupUi(self)

        self.steps = YaliSteps()

    def shown(self):
        ctx.mainScreen.disableBack()
        ctx.yali.processPendingActions(self)
        self.steps.slotRunOperations()

    def execute(self):
        ctx.mainScreen.disableNext()

        if not ctx.yali.install_type == YALI_FIRSTBOOT:
            try:
                ctx.debugger.log("Trying to umount %s" % (ctx.consts.target_dir + "/home"))
                yali4.sysutils.umount(ctx.consts.target_dir + "/home")
                ctx.debugger.log("Trying to umount %s" % (ctx.consts.target_dir))
                yali4.sysutils.umount(ctx.consts.target_dir)
            except:
                ctx.debugger.log("Umount Failed.")
                pass

        w = RebootWidget(self)

        ctx.debugger.log("Show reboot dialog.")
        self.dialog = WarningDialog(w, self)
        self.dialog.exec_()
        ctx.mainScreen.processEvents()
        ctx.yali.info.updateAndShow(_('<b>Rebooting system. Please wait!</b>'))

        # remove cd...
        if not ctx.yali.install_type == YALI_FIRSTBOOT:
            ctx.debugger.log("Trying to eject the CD.")
            yali4.sysutils.eject_cdrom()

        ctx.debugger.log("Yali, fastreboot calling..")

        # store log content
        if ctx.debugEnabled:
            open(ctx.consts.log_file,"w").write(str(ctx.debugger.traceback.plainLogs))

        ctx.mainScreen.processEvents()
        time.sleep(4)
        yali4.sysutils.fastreboot()

class RebootWidget(QtGui.QWidget):

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)

        l = QtGui.QVBoxLayout(self)
        l.setSpacing(20)
        l.setMargin(10)

        warning = QtGui.QLabel(self)
        warning.setText(_('''<b>
<p>Press Reboot button to restart your system.</p>
</b>
'''))

        self.reboot = QtGui.QPushButton(self)
        self.reboot.setText(_("Reboot"))

        buttons = QtGui.QHBoxLayout(self)
        buttons.setSpacing(10)
        buttons.addStretch(1)
        buttons.addWidget(self.reboot)

        l.addWidget(warning)
        l.addLayout(buttons)

        self.connect(self.reboot, SIGNAL("clicked()"),
                     self.slotReboot)

    def slotReboot(self):
        self.emit(SIGNAL("signalOK"), ())


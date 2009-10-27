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

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import yali4.sysutils
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.kickerwidget import Ui_KickerWidget
import yali4.gui.context as ctx
from yali4.gui.YaliDialog import Dialog
from yali4.kahya import kahya
import yali4.storage

def loadFile(path):
    """Read contents of a file"""
    f = file(path)
    data = f.read()
    f.close()
    return data

def get_kernel_opt(cmdopt):
    cmdline = loadFile("/proc/cmdline").split()
    for cmd in cmdline:
        pos = len(cmdopt)
        if cmd == cmdopt:
            return cmd
        if cmd.startswith(cmdopt) and cmd[pos] == '=':
            return cmd[pos+1:]
    return ''

def kahyaExists():
    if get_kernel_opt(ctx.consts.kahyaParam) or ctx.options.kahyaFile:
        return True
    return False

##
# Welcome screen is the first screen to be shown.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Kahya is working...')
    desc = _('Kahya will automatically install your system..')
    help = _('''
<font size="+2">Kicker Check !</font>
<p> Some help messages </p>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_KickerWidget()
        self.ui.setupUi(self)

    def shown(self):
        ctx.mainScreen.slotNext()

    def execute(self):
        if not kahyaExists():
            ctx.debugger.log("There is no kahya jumps to the next screen.")
            return True

        ctx.autoInstall = True
        yaliKahya = kahya()
        print "...",ctx.options.kahyaFile

        kahyaOpt = get_kernel_opt(ctx.consts.kahyaParam)

        if kahyaOpt:
            ctx.debugger.log("KAHYA-PARAMS:: %s" % kahyaOpt)
            kahyaFile = kahyaOpt.split(',')[1]
        else:
            kahyaFile = ctx.options.kahyaFile

        if kahyaFile:
            ctx.debugger.log("Reading kahya from file %s" % kahyaFile)
            yaliKahya.readData(kahyaFile)
            if yaliKahya.checkFileValidity()==True:
                ctx.debugger.log("File is ok")

                # find usable storage devices
                # initialize all storage devices
                if not yali4.storage.init_devices():
                    raise GUIException, _("Can't find a storage device!")

                devices = []
                for dev in yali4.storage.devices:
                    if dev.getTotalMB() >= ctx.consts.min_root_size:
                        devices.append(dev)

                correctData = yaliKahya.getValues()
                ctx.debugger.log("Given Kahya Values :")

                # single types
                ctx.installData.keyData = correctData.keyData
                ctx.installData.rootPassword = correctData.rootPassword
                ctx.installData.hostName = correctData.hostname
                ctx.installData.autoLoginUser = correctData.autoLoginUser
                ctx.installData.autoPartDev = devices[int(correctData.partitioning[0].disk[-1])]
                ctx.installData.useYaliFirstBoot = correctData.useYaliFirstBoot

                # if exists use different source repo
                ctx.installData.repoAddr = correctData.repoAddr
                ctx.installData.repoName = correctData.repoName

                ctx.debugger.log("HOSTNAME : %s " % ctx.installData.hostName)
                ctx.debugger.log("KEYDATA  : %s " % ctx.installData.keyData.X)

                if ctx.installData.repoAddr:
                    ctx.debugger.log("REPOADDR : %s " % ctx.installData.repoAddr)
                    ctx.debugger.log("REPONAME : %s " % ctx.installData.repoName)

                # multi types
                for user in correctData.users:
                    ctx.installData.users.append(user)
                    yali4.users.pending_users.append(user)
                    ctx.debugger.log("USER    : %s " % user.username)

                if ctx.options.dryRun == True:
                    ctx.debugger.log("dryRun activated Yali stopped")
                else:
                    # Bootloader Screen is 9
                    ctx.mainScreen.setCurrent(9)
            else:
                ctx.debugger.log("This kahya file is not correct !!")
                wrongData = yaliKahya.getValues()
                ctx.debugger.log("".join(wrongData))

        ctx.mainScreen.disableBack()
        ctx.mainScreen.disableNext()


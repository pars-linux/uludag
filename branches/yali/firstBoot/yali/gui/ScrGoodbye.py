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
from qt import *

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext

import comar
import time
import yali.users
#import yali.localeutils
from os.path import basename
from yali.gui.ScreenWidget import ScreenWidget
from yali.gui.YaliDialog import WarningDialog
from yali.gui.YaliSteps import YaliSteps
from yali.constants import consts
import yali.gui.context as ctx

##
# Goodbye screen
class Widget(QWidget, ScreenWidget):

    help = _('''
<font size="+2">Congratulations</font>
<font size="+1">
<p>
You have successfully setup your Pardus, a very easy to use desktop system on
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
        apply(QWidget.__init__, (self,) + args)

        img = QLabel(self)
        img.setPixmap(ctx.iconfactory.newPixmap("goodbye"))

        self.steps = YaliSteps(self)

        self.info = QLabel(self)
        self.info.setText(
            _('<b><font size="+2" color="#FF6D19">Rebooting system. Please wait!</font></b>'))
        self.info.hide()
        self.info.setAlignment(QLabel.AlignCenter|QLabel.AlignTop)
        self.info.setMinimumSize(QSize(0,50))

        vbox = QVBoxLayout(self)
        vbox.addStretch(1)

        hbox = QHBoxLayout(vbox)
        hbox.addStretch(1)
        #FIXME Where is the steps layout ??
        hbox.addWidget(img)
        hbox.addStretch(1)

        vbox.addStretch(1)
        vbox.addWidget(self.info)

    def shown(self):
        ctx.debugger.log("%s loaded" % basename(__file__))
        ctx.screens.disablePrev()
        self.processPendingActions()
        self.steps.slotRunOperations()

    def execute(self):
        ctx.screens.disableNext()

        self.info.show()
        self.info.setAlignment(QLabel.AlignCenter)

        ctx.debugger.log("Yali, fastreboot calling..")
        time.sleep(2)
        os.system("/sbin/reboot")

    # process pending actions defined in other screens.
    def processPendingActions(self):
        comarLink = None

        def connectToComar():
            global comarLink
            for i in range(20):
                try:
                    ctx.debugger.log("trying to start comar..")
                    comarLink = comar.Link(sockname=consts.comar_socket_file)
                    break
                except comar.CannotConnect:
                    time.sleep(1)
                    ctx.debugger.log("wait comar for 1 second...")
            if comarLink:
                return True
            return False

        def setHostName():
            global comarLink
            comarLink.Net.Stack.setHostNames(hostnames=ctx.installData.hostName)
            reply = comarLink.read_cmd()
            ctx.debugger.log("Hostname set as %s" % ctx.installData.hostName)
            return True

        def addUsers():
            global comarLink
            for u in yali.users.pending_users:
                ctx.debugger.log("User %s adding to system" % u.username)
                comarLink.User.Manager.addUser(name=u.username,
                                               password=u.passwd,
                                               realname=u.realname,
                                               groups=','.join(u.groups))
                ctx.debugger.log("RESULT :: %s" % str(comarLink.read_cmd()))

                # Enable auto-login
                if u.username == ctx.installData.autoLoginUser:
                    u.setAutoLogin()
            return True

        def setKdeBase():
            global comarLink
            comarLink.System.Service["kdebase"].setState(state="on")
            comarLink.System.Service["yali"].setState(state="off")

        def setRootPassword():
            global comarLink
            comarLink.User.Manager.setUser(uid=0,
                                           password=ctx.installData.rootPassword)
            ctx.debugger.log("RESULT :: %s" % str(comarLink.read_cmd()))
            return True

        # def writeConsoleData():
        #     yali.localeutils.write_keymap(ctx.installData.keyData.console)
        #     ctx.debugger.log("Keymap stored.")
        #     return True

        steps = [{"text":_("Trying to connect COMAR Daemon..."),"operation":connectToComar},
                 {"text":_("Setting Hostname..."),"operation":setHostName},
                 {"text":_("Setting Root Password..."),"operation":setRootPassword},
                 {"text":_("Adding Users..."),"operation":addUsers},
                 {"text":_("Setting up KdeBase..."),"operation":setKdeBase}]
                 # {"text":_("Writing Console Data..."),"operation":writeConsoleData},
        self.steps.setOperations(steps)


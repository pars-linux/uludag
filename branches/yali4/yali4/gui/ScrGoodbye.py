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

        self.ui.info.setText(_('<b><font size="+2" color="#FFFFFF">Rebooting system. Please wait!</font></b>'))
        self.ui.info.hide()

    def shown(self):
        ctx.mainScreen.disableBack()
        self.processPendingActions()
        self.steps.slotRunOperations()

    def execute(self):
        ctx.mainScreen.disableNext()
        self.ui.info.show()

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

        # remove cd...
        ctx.debugger.log("Trying to eject the CD.")
        yali4.sysutils.eject_cdrom()

        ctx.debugger.log("Yali, fastreboot calling..")

        # store log content
        if ctx.debugEnabled:
            open(ctx.consts.log_file,"w").write(str(ctx.debugger.traceback.plainLogs))

        time.sleep(4)
        yali4.sysutils.fastreboot()

    # process pending actions defined in other screens.
    def processPendingActions(self):
        global bus
        bus = None
        def connectToDBus():
            global bus
            for i in range(20):
                try:
                    ctx.debugger.log("trying to start dbus..")
                    bus = dbus.bus.BusConnection(address_or_type="unix:path=%s" % ctx.consts.dbus_socket_file)
                    break
                except dbus.DBusException:
                    time.sleep(1)
                    ctx.debugger.log("wait dbus for 1 second...")
            if bus:
                return True
            return False

        def setHostName():
            global bus
            obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")
            obj.setHostName(str(ctx.installData.hostName), dbus_interface="tr.org.pardus.comar.Net.Stack")
            ctx.debugger.log("Hostname set as %s" % ctx.installData.hostName)
            return True

        def addUsers():
            global bus
            obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")
            for u in yali4.users.pending_users:
                ctx.debugger.log("User %s adding to system" % u.username)
                obj.addUser("auto", u.username, u.realname, "", "", u.passwd, u.groups, dbus_interface="tr.org.pardus.comar.User.Manager")
                # Enable auto-login
                if u.username == ctx.installData.autoLoginUser:
                    u.setAutoLogin()
            return True

        def setRootPassword():
            if not ctx.installData.useYaliFirstBoot:
                global bus
                obj = bus.get_object("tr.org.pardus.comar", "/package/baselayout")
                obj.setUser(0, "", "", "", str(ctx.installData.rootPassword), "", dbus_interface="tr.org.pardus.comar.User.Manager")
            return True

        def writeConsoleData():
            yali4.localeutils.write_keymap(ctx.installData.keyData.console)
            ctx.debugger.log("Keymap stored.")
            return True

        def migrateXorgConf():
            yali4.postinstall.migrate_xorg_conf(ctx.installData.keyData.X)
            ctx.debugger.log("xorg.conf merged.")
            return True

        def setPackages():
            global bus
            if yali4.sysutils.checkYaliParams(param=ctx.consts.firstBootParam):
                ctx.debugger.log("OemInstall selected.")
                obj = bus.get_object("tr.org.pardus.comar", "/package/kdebase")
                obj.setState("off", dbus_interface="tr.org.pardus.comar.System.Service")
                obj = bus.get_object("tr.org.pardus.comar", "/package/yali_firstBoot")
                obj.setState("on", dbus_interface="tr.org.pardus.comar.System.Service")
            return True

        steps = [{"text":"Trying to connect DBUS...","operation":connectToDBus},
                 {"text":"Setting Hostname...","operation":setHostName},
                 {"text":"Setting TimeZone...","operation":yali4.postinstall.setTimeZone},
                 {"text":"Setting Root Password...","operation":setRootPassword},
                 {"text":"Adding Users...","operation":addUsers},
                 {"text":"Writing Console Data...","operation":writeConsoleData},
                 {"text":"Migrating X.org Configuration...","operation":migrateXorgConf},
                 {"text":"Setting misc. package configurations...","operation":setPackages},
                 {"text":"Installing BootLoader...","operation":self.installBootloader}]

        self.steps.setOperations(steps)

    def installBootloader(self):
        if not ctx.installData.bootLoaderDev:
            ctx.debugger.log("Dont install bootloader selected; skipping.")
            return

        ctx.debugger.log("Bootloader is installing...")
        loader = yali4.bootloader.BootLoader()
        root_part_req = ctx.partrequests.searchPartTypeAndReqType(parttype.root,
                                                                  partrequest.mountRequestType)
        _ins_part = root_part_req.partition().getPath()
        loader.write_grub_conf(_ins_part,ctx.installData.bootLoaderDev)

        # Check for windows partitions.
        for d in yali4.storage.devices:
            for p in d.getPartitions():
                fs = p.getFSName()
                if fs in ("ntfs", "fat32"):
                    if is_windows_boot(p.getPath(), fs):
                        win_fs = fs
                        win_dev = basename(p.getDevicePath())
                        win_root = basename(p.getPath())
                        loader.grub_conf_append_win(ctx.installData.bootLoaderDev,
                                                    win_dev,
                                                    win_root,
                                                    win_fs)
                        continue

        # finally install it
        loader.install_grub(ctx.installData.bootLoaderDev)
        ctx.debugger.log("Bootloader installed.")

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


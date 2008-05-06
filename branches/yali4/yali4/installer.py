# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# linux ?
import os

# we need i18n
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

# PyQt4 Rocks
from PyQt4 import QtGui
from PyQt4.QtCore import *

# yali base
from yali4.exception import *
from yali4.constants import consts
import yali4.gui.context as ctx
import yali4.localeutils
import yali4.sysutils

# pisi base
import pisi.ui
import yali4.pisiiface

# partitioning
import yali4.partitiontype as parttype
import yali4.partitionrequest as request
from yali4.partitionrequest import partrequests

# gui
from yali4.gui.YaliDialog import Dialog

# debugger
from yali4.gui.debugger import Debugger
from yali4.gui.debugger import DebuggerAspect

# screens
import yali4.gui.ScrKahyaCheck
import yali4.gui.ScrWelcome
import yali4.gui.ScrCheckCD
import yali4.gui.ScrKeyboard
import yali4.gui.ScrDateTime
import yali4.gui.ScrAdmin
import yali4.gui.ScrUsers
import yali4.gui.ScrPartitionAuto
import yali4.gui.ScrPartitionManual
import yali4.gui.ScrBootloader
import yali4.gui.ScrInstall
import yali4.gui.ScrGoodbye

PARTITION_ERASE_ALL, PARTITION_USE_AVAIL, PARTITION_USE_OLD = range(3)
YALI_INSTALL, YALI_FIRSTBOOT, YALI_OEMINSTALL, YALI_PARTITIONER = range(4)

class Yali:
    def __init__(self, install_type=YALI_INSTALL):

        self._screens = {}

        # Normal Installation process
        self._screens[YALI_INSTALL] = [                                  # Numbers can be used with -s paramter
                                       yali4.gui.ScrKahyaCheck,          # 00
                                       yali4.gui.ScrWelcome,             # 01
                                       yali4.gui.ScrCheckCD,             # 02
                                       yali4.gui.ScrKeyboard,            # 03
                                       yali4.gui.ScrDateTime,            # 04
                                       yali4.gui.ScrUsers,               # 05
                                       yali4.gui.ScrAdmin,               # 06
                                       yali4.gui.ScrPartitionAuto,       # 07
                                       yali4.gui.ScrPartitionManual,     # 08
                                       yali4.gui.ScrBootloader,          # 09
                                       yali4.gui.ScrInstall,             # 10
                                       yali4.gui.ScrGoodbye              # 11
                                      ]

        # FirstBoot Installation process
        self._screens[YALI_FIRSTBOOT] = [                                # Numbers can be used with -s paramter
                                         yali4.gui.ScrWelcome,           # 00
                                         yali4.gui.ScrKeyboard,          # 01
                                         yali4.gui.ScrDateTime,          # 02
                                         yali4.gui.ScrUsers,             # 03
                                         yali4.gui.ScrAdmin,             # 04
                                         yali4.gui.ScrGoodbye            # 05
                                        ]

        # Oem Installation process
        self._screens[YALI_OEMINSTALL] = [                                  # Numbers can be used with -s paramter
                                          yali4.gui.ScrWelcome,             # 00
                                          yali4.gui.ScrCheckCD,             # 01
                                          yali4.gui.ScrPartitionAuto,       # 02
                                          yali4.gui.ScrPartitionManual,     # 03
                                          yali4.gui.ScrBootloader,          # 04
                                          yali4.gui.ScrInstall,             # 05
                                          yali4.gui.ScrGoodbye              # 06
                                         ]

        # Use YALI just for partitioning
        self._screens[YALI_PARTITIONER] = [
                                           yali4.gui.ScrPartitionManual  # Manual Partitioning
                                          ]

        # Let the show begin..
        self.screens = self._screens[install_type]
        self.install_type = install_type

    def checkCD(self, rootWidget):
        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()

        class PisiUI(pisi.ui.UI):
            def notify(self, event, **keywords):
                pass
            def display_progress(self, operation, percent, info, **keywords):
                pass

        yali4.pisiiface.initialize(ui = PisiUI(), with_comar = False, nodestDir = True)
        yali4.pisiiface.add_cd_repo()
        ctx.mainScreen.processEvents()
        pkg_names = yali4.pisiiface.get_available()

        rootWidget.progressBar.setMaximum(len(pkg_names))

        cur = 0
        for pkg_name in pkg_names:
            cur += 1
            ctx.debugger.log("Checking %s " % pkg_name)
            if yali4.pisiiface.check_package_hash(pkg_name):
                rootWidget.progressBar.setValue(cur)
            else:
                self.showError(_("Check Failed"),
                               _("<b><p>Integrity check for packages failed.\
                                  It seems that installation CD is broken.</p></b>"))

        rootWidget.checkLabel.setText(_('<font color="#257216">Check succeeded. You can proceed to the next screen.</font>'))

        yali4.pisiiface.remove_repo(ctx.consts.cd_repo_name)

        ctx.mainScreen.enableNext()
        ctx.mainScreen.enableBack()

    def setKeymap(self, keymap):
        yali4.localeutils.set_keymap(keymap["xkblayout"], keymap["xkbvariant"])
        ctx.installData.keyData = keymap

    def setTime(self, rootWidget):
        date = rootWidget.calendarWidget.selectedDate()
        args = "%02d%02d%02d%02d%04d.%02d" % (date.month(), date.day(),
                                              rootWidget.timeHours.time().hour(), rootWidget.timeMinutes.time().minute(),
                                              date.year(), rootWidget.timeSeconds.time().second())
        # Set current date and time
        ctx.debugger.log("Date/Time setting to %s" % args)
        os.system("date %s" % args)

        # Sync date time with hardware
        ctx.debugger.log("YALI's time is syncing with the system.")
        os.system("hwclock --systohc")

    def setTimeZone(self, rootWidget):
        # Store time zone selection we will set it in processPending actions.
        ctx.installData.timezone = rootWidget.timeZoneList.currentItem().text()
        ctx.debugger.log("Time zone selected as %s " % ctx.installData.timezone)

    def showError(self, title, message):
        r = ErrorWidget(self)
        r.label.setText(message)
        d = Dialog(title, r, self)
        d.resize(300,200)
        d.exec_()

class ErrorWidget(QtGui.QWidget):
    def __init__(self, *args):
        apply(QtGui.QWidget.__init__, (self,) + args)

        self.gridlayout = QtGui.QGridLayout(self)
        self.vboxlayout = QtGui.QVBoxLayout()

        self.label = QtGui.QLabel(self)
        self.vboxlayout.addWidget(self.label)

        self.hboxlayout = QtGui.QHBoxLayout()

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.reboot = QtGui.QPushButton(self)
        self.reboot.setFocusPolicy(Qt.NoFocus)
        self.reboot.setText(_("Reboot"))

        self.hboxlayout.addWidget(self.reboot)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.gridlayout.addLayout(self.vboxlayout,0,0,1,1)

        yali4.sysutils.eject_cdrom()

        self.connect(self.reboot, SIGNAL("clicked()"),self.slotReboot)

    def slotReboot(self):
        yali4.sysutils.reboot()


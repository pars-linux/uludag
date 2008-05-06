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

# yali base
from yali4.exception import *
from yali4.constants import consts
import yali4.localeutils
import yali4.sysutils

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
YALI_INSTALL, YALI_FIRSTBOOT, YALI_PARTITIONER = range(3)

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

        # This list will be used for yali4-firstBoot
        self._screens[YALI_FIRSTBOOT] = [                                # Numbers can be used with -s paramter
                                         yali4.gui.ScrWelcome,           # 01
                                         yali4.gui.ScrKeyboard,          # 02
                                         yali4.gui.ScrDateTime,          # 03
                                         yali4.gui.ScrUsers,             # 04
                                         yali4.gui.ScrAdmin,             # 05
                                         yali4.gui.ScrGoodbye            # 06
                                        ]

        # Use YALI just for partitioning
        self._screens[YALI_PARTITIONER] = [
                                           yali4.gui.ScrPartitionManual  # Manual Partitioning
                                          ]

        # Let the show begin..
        self.screens = self._screens[install_type]

    def setKeymap(self, keymap):
        yali4.localeutils.set_keymap(keymap["xkblayout"], keymap["xkbvariant"])
        self.keymap = keymap


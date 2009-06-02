# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import dbus
import pisi
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QEvent, QObject

import yali4.storage
import yali4.pisiiface
import yali4.postinstall
import yali4.sysutils

from yali4.gui.installdata import *
from yali4.gui.GUIAdditional import DeviceItem
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.rescuepasswordwidget import Ui_RescuePasswordWidget
from yali4.gui.YaliSteps import YaliSteps
from yali4.gui.GUIException import GUIException
from yali4.gui.GUIAdditional import ConnectionWidget
import yali4.gui.context as ctx

##
# BootLoader screen.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Rescue Mode for Password Recovery')
    desc = _('You can recover your password ...')
    icon = "iconInstall"
    help = _('''
<font size="+2">Password Recovery</font>
<font size="+1"></font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_RescuePasswordWidget()
        self.ui.setupUi(self)

    def fillUserList(self):
        pass
        """
        for hist in history:
            HistoryItem(self.ui.historyList, hist)
        """

    def execute(self):
        return True

    def backCheck(self):
        ctx.mainScreen.moveInc = 3
        return True

class UserItem(QtGui.QListWidgetItem):
    def __init__(self, parent, user):
        QtGui.QListWidgetItem.__init__(self, user, parent)
        self._user = user

    def getInfo(self):
        return self._user


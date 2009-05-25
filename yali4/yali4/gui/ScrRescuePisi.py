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
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

import yali4.storage
from yali4.gui.installdata import *
from yali4.gui.GUIAdditional import DeviceItem
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.rescuepisiwidget import Ui_RescuePisiWidget
from yali4.gui.GUIException import GUIException
import yali4.gui.context as ctx

##
# BootLoader screen.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Rescue Mode for Pisi History')
    desc = _('You can take back your system ...')
    icon = "iconInstall"
    help = _('''
<font size="+2">Pisi History</font>
<font size="+1"></font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_RescuePisiWidget()
        self.ui.setupUi(self)

    def shown(self):
        pass

    def execute(self):
        return True

    def backCheck(self):
        ctx.mainScreen.moveInc = 2
        return True


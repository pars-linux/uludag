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

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import pisi.ui
import yali4.pisiiface
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.datetimewidget import Ui_DateTimeWidget
import yali4.gui.context as ctx
from yali4.sysutils import TimeZoneList

from yali4.gui.YaliDialog import Dialog

class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Set your timezone')
    desc = _('You can change your timezone, time or date settings..')
    icon = "iconDate"
    help = _('''
<font size="+2">Time Zone settings</font>

<font size="+1">
<p>In this screen, you can set your timezone, time or date settings. 
It is important to use correct settings.
</p>

''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_DateTimeWidget()
        self.ui.setupUi(self)
        zom = TimeZoneList()
        zoneList = [ x.timeZone for x in zom.getEntries() ]
        for zone in zoneList:
            self.ui.timeZoneList.addItem(QString(zone))

    def shown(self):
        pass
        #from os.path import basename
        #ctx.debugger.log("%s loaded" % basename(__file__))


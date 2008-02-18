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

import os
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.datetimewidget import Ui_DateTimeWidget
import yali4.gui.context as ctx
from yali4.sysutils import TimeZoneList

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
        self.timer = QTimer(self)
        self.fromTimeUpdater = True

        # fill in the timezone list
        zom = TimeZoneList()
        zoneList = [ x.timeZone for x in zom.getEntries() ]
        zoneList.sort()
        for zone in zoneList:
            self.ui.timeZoneList.addItem(QString(zone))

        self.connect(self.ui.timeHours, SIGNAL("valueChanged(int)"),self.timerStop)
        self.connect(self.ui.timeMinutes, SIGNAL("valueChanged(int)"),self.timerStop)
        self.connect(self.ui.timeSeconds, SIGNAL("valueChanged(int)"),self.timerStop)
        self.connect(self.timer, SIGNAL("timeout()"),self.updateClock)

    def timerStop(self,i):
        if self.fromTimeUpdater:
            return
        self.ui.timeHours.setPrefix('')
        self.ui.timeMinutes.setPrefix('')
        self.ui.timeSeconds.setPrefix('')
        self.timer.stop()

    def updateClock(self):

        def sw(w,n):
            w.setValue(n)
            if n<10:
                w.setPrefix('0')
            else:
                w.setPrefix('')

        cur = QTime.currentTime()

        self.fromTimeUpdater = True
        sw(self.ui.timeHours,cur.hour())
        sw(self.ui.timeMinutes,cur.minute())
        sw(self.ui.timeSeconds,cur.second())
        self.fromTimeUpdater = False

    def shown(self):
        self.timer.start(1000)

    def execute(self):
        date = self.ui.calendarWidget.selectedDate()
        args = "%02d%02d%02d%02d%04d.%02d" % (date.month(), date.day(),
                                              self.ui.timeHours.value(), self.ui.timeMinutes.value(),
                                              date.year(), self.ui.timeSeconds.value())
        # Set current date and time
        os.system("date %s" % args)
        self.timer.stop()

        # Sync date time with hardware
        os.system("hwclock --systohc")


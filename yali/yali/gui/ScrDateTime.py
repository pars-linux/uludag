# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QTimer, QDate, QTime

import yali.localedata
import yali.context as ctx
import yali.postinstall
from yali.gui import ScreenWidget
from yali.gui.Ui.datetimewidget import Ui_DateTimeWidget
from yali.timezone import TimeZoneList

class Widget(QWidget, ScreenWidget):
    name = "timeSetup"

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_DateTimeWidget()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        self.from_time_updater = True
        self.is_date_changed = False

        self.current_zone = ""

        for country, data in yali.localedata.locales.items():
            if country == ctx.consts.lang:
                if data.has_key("timezone"):
                    ctx.installData.timezone = data["timezone"]

        # fill in the timezone list
        zom = TimeZoneList()
        zones = [ x.timeZone for x in zom.getEntries() ]
        zones.sort()
        for zone in zones:
            self.pretty_zone_name = "%s - %s" % (zone.split("/")[0], zone.split("/")[1])
            if zone == ctx.installData.timezone:
                self.current_zone = self.pretty_zone_name
            self.ui.timeZoneList.addItem(self.pretty_zone_name, zone)


        # Select the timeZone
        self.index = self.ui.timeZoneList.findText(self.current_zone)
        self.ui.timeZoneList.setCurrentIndex(self.index)

        # Widget connections
        self.connect(self.ui.timeEdit, SIGNAL("timeChanged(QTime)"), self.timerStop)
        self.connect(self.ui.calendarWidget, SIGNAL("selectionChanged()"), self.dateChanged)
        self.connect(self.timer, SIGNAL("timeout()"), self.updateClock)

        self.ui.calendarWidget.setDate(QDate.currentDate())

        self.timer.start(1000)

    def dateChanged(self):
        self.is_date_changed = True

    def timerStop(self):
        if self.from_time_updater:
            return
        # Human action detected; stop the timer.
        self.timer.stop()

    def updateClock(self):

        # What time is it ?
        cur = QTime.currentTime()

        self.from_time_updater = True
        self.ui.timeEdit.setTime(cur)
        self.from_time_updater = False

    def shown(self):
        self.timer.start(1000)

    def setTime(self):
        ctx.interface.informationWindow.update(_("Adjusting time settings"))
        date = self.ui.calendarWidget.date()
        time = self.ui.timeEdit.time()
        args = "%02d%02d%02d%02d%04d.%02d" % (date.month(), date.day(),
                                              time.hour(), time.minute(),
                                              date.year(), time.second())


        # Set current date and time
        ctx.logger.debug("Date/Time setting to %s" % args)
        yali.util.run_batch("date", [args])

        # Sync date time with hardware
        ctx.logger.debug("YALI's time is syncing with the system.")
        yali.util.run_batch("hwclock", ["--systohc"])
        ctx.interface.informationWindow.hide()

    def execute(self):
        if not self.timer.isActive() or self.is_date_changed:
            QTimer.singleShot(500, self.setTime)
            self.timer.stop()

        index = self.ui.timeZoneList.currentIndex()
        ctx.installData.timezone = self.ui.timeZoneList.itemData(index).toString()
        ctx.logger.debug("Time zone selected as %s " % ctx.installData.timezone)

        if ctx.flags.install_type == ctx.STEP_BASE:
            #FIXME:Refactor dirty code
            if ctx.storageInitialized:
                disks = filter(lambda d: not d.format.hidden, ctx.storage.disks)
                if len(disks) == 1:
                    ctx.storage.clearPartDisks = [disks[0].name]
                    ctx.mainScreen.step_increment = 2
                else:
                    ctx.mainScreen.step_increment = 1
            else:
                ctx.storageInitialized = yali.storage.initialize(ctx.storage, ctx.interface)
                if not ctx.storageInitialized:
                    return False
                else:
                    disks = filter(lambda d: not d.format.hidden, ctx.storage.disks)
                    if len(disks) == 1:
                        ctx.storage.clearPartDisks = [disks[0].name]
                        ctx.mainScreen.step_increment = 2
                    else:
                        ctx.mainScreen.step_increment = 1

        return True


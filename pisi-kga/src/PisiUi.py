# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>

from kdecore import i18n
from qt import *
from Enums import *
import pisi.ui
import time

class PisiUi(pisi.ui.UI,QObject):

    def __init__(self, parent):
        pisi.ui.UI.__init__(self)
        QObject.__init__(self)
        self.receiver = parent
        self.confirmed = None

    def customEvent(self, cEvent):
        if cEvent.type() == CustomEvent.UserConfirmed:
            self.confirmed = cEvent.data()
        
    def error(self, msg):
        cEvent = QCustomEvent(CustomEvent.PisiError)
        cEvent.setData(msg)
        QThread.postEvent(self.receiver,cEvent)

    def info(self, msg):
        cEvent = QCustomEvent(CustomEvent.PisiInfo)
        cEvent.setData(msg)
        QThread.postEvent(self.receiver,cEvent)
        # print the thing on stdout you don't lose a thing
        print msg

    def confirm(self, msg):
        cEvent = QCustomEvent(CustomEvent.AskConfirmation)
        cEvent.setData(msg)
        QThread.postEvent(self.receiver,cEvent)        
        
        if self.confirmed:
            self.confirmed = None
            return True
        else:
            self.confirmed = None
            return False

    def notify(self, event, **keywords):
        cEvent = QCustomEvent(CustomEvent.PisiNotify)
        data = None
        if event == pisi.ui.installing:
            data = i18n("installing")
        elif event == pisi.ui.configuring:
            data = i18n("configuring")
        elif event == pisi.ui.extracting:
            data = i18n("extracting")
        elif event == pisi.ui.removing:
            data = i18n("removing")
        elif event == pisi.ui.installed or event == pisi.ui.upgraded or event == pisi.ui.removed:
            cEvent = QCustomEvent(CustomEvent.Finished)

        if data:
            cEvent.setData(data)
        QThread.postEvent(self.receiver,cEvent)

    def display_progress(self, filename, percent, rate, symbol, eta):
        cEvent = QCustomEvent(CustomEvent.UpdateProgress)
        cEvent.setData(QString(filename)+QString(" ")+QString.number(percent)+QString(" ")+QString.number(rate)+QString(" ")+QString(symbol))
        QThread.postEvent(self.receiver,cEvent)

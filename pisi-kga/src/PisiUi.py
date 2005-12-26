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

import time

from kdecore import i18n
from qt import *
from kdeui import *

from Enums import *

import pisi.ui

class PisiUi(pisi.ui.UI,QObject):

    def __init__(self, parent):
        self.parent = parent
        pisi.ui.UI.__init__(self)
        QObject.__init__(self)
        self.receiver = parent
        self.confirmed = None

    def customEvent(self, cEvent):
        if cEvent.type() == CustomEvent.UserConfirmed:
            self.confirmed = cEvent.data()
        
    def warning(self, msg):
        cEvent = QCustomEvent(CustomEvent.PisiWarning)
        cEvent.setData(msg)
        QThread.postEvent(self.receiver,cEvent)
        
    def error(self, msg):
        cEvent = QCustomEvent(CustomEvent.PisiError)
        cEvent.setData(msg)
        QThread.postEvent(self.receiver,cEvent)
    
    def ack(self,msg):
        cEvent = QCustomEvent(CustomEvent.PisiAck)
        cEvent.setData(msg) 
        QThread.postEvent(self.receiver,cEvent)

    def info(self, msg):
        cEvent = QCustomEvent(CustomEvent.PisiInfo)
        cEvent.setData(msg)
        QThread.postEvent(self.receiver,cEvent)

    def confirm(self, msg):
        cEvent = QCustomEvent(CustomEvent.AskConfirmation)
        cEvent.setData(msg)
        QThread.postEvent(self.receiver,cEvent)        

        # You might be wondering how this code works, as we don't set self.confirmed here
        # Here is what happens, CustomEvent.AskConfirmation event is sent to main app,
        # it shows a KMessageBox and thread eventloop waits for it to finish, when the user
        # confirms it hits CustomEvent.UserConfirmed in customEvent and next we are here in
        # the Thread and self.confirmed is already set
       
        # This needs more work, check http://bugs.uludag.org.tr/show_bug.cgi?id=1258
        if self.confirmed:
            self.confirmed = None
            return True
        else:
            self.confirmed = None
            return False

    def notify(self, event, **keywords):
        cEvent = QCustomEvent(CustomEvent.PisiNotify)
        data = None
        
        if event == pisi.ui.downloading:
            data = i18n("downloading")
        elif event == pisi.ui.installing:
            data = i18n("installing")
        elif event == pisi.ui.configuring:
            data = i18n("configuring")
        elif event == pisi.ui.extracting:
            data = i18n("extracting")
        elif event == pisi.ui.removing:
            data = i18n("removing")
        else:
            return

        QThread.postEvent(self.receiver,cEvent)

    def display_progress(self, **kargs):
        cEvent = QCustomEvent(CustomEvent.UpdateProgress)
        cEvent.setData(QString(kargs["filename"])+QString(" ")+QString.number(kargs["percent"])+QString(" ")+
                        QString.number(kargs["rate"])+QString(" ")+QString(kargs["symbol"])+
                        QString(" ")+QString.number(kargs["downloaded_size"])+QString(" ")+QString.number(kargs["total_size"]))
        QThread.postEvent(self.receiver,cEvent)

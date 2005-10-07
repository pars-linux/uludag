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

from qt import *
from pisi.ui import UI

class PisiUi(UI):

    def __init__(self, parent):
        UI.__init__(self)
        self.receiver = parent

    def error(self, msg):
        event = QCustomEvent(QEvent.User+4)
        event.setData(msg)
        QThread.postEvent(self.receiver,event)
            
    def confirm(self, msg):
        return True

    def display_progress(self, pd):
        event = QCustomEvent(QEvent.User+5)
        event.setData(QString(pd['filename'])+QString(" ")+QString.number(pd['percent']))
        QThread.postEvent(self.receiver,event)

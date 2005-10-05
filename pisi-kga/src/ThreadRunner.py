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
# Authors: İsmail Dönmez <ismail@uludag.org.tr>

from qt import *
import pisi.api
from threading import *

class MyThread(Thread):
    def __init__(self, widget):
        Thread.__init__(self, group=None, target=None, name=None)
        self.receiver = widget
        self.installing = False
        self.upgrading = False
        self.removing = False
        self.updatingRepo = False

    def install(self,apps):
        self.installing = True
        self.appList = apps
        self.start()

    def upgrade(self,apps):
        self.upgrading = True
        self.appList = apps
        self.start()
    
    def remove(self,apps):
        self.removing = True
        self.appList = apps
        self.start()

    def updateRepo(self, repo):
        self.updatingRepo = True
        self.repo = repo
        self.start()
            
    def run(self):
        
        if self.installing:
            pisi.api.install(self.appList)
            self.installing = False

        elif self.upgrading:
            pisi.api.upgrade(appList)
            self.upgrading = False
                                                                
        elif self.removing:
            pisi.api.remove(self.appList)
            self.removing = False

        elif self.updatingRepo:
            event = QCustomEvent(QEvent.User+2)
            event.setData(self.repo)
            QThread.postEvent(self.receiver,event)
            pisi.api.update_repo(self.repo)
            self.updatingRepo = False
        else:
            pass

        event = QCustomEvent(QEvent.User+1)
        QThread.postEvent(self.receiver,event)

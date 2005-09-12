# -*- coding: utf-8 -*-
###########################################################################
# PiSi KGA - Threading Part                                               #
# ------------------------------                                          #
# begin     : Çrş Eyl  7 15:55:28 EEST 2005                               #
# copyright : (C) 2005 by UEKAE/TÜBİTAK                                   #
# email     : ismail@uludag.org.tr                                        #
#                                                                         #
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
###########################################################################

from qt import *
from kdecore import *

import pisi.api
import PisiKga

class Thread(QThread):
    def __init__(self, qObject):
        QThread.__init__(self)
        self.qObject = qObject
        self.installing = False
        self.upgrading = False
        self.removing = False

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
        
    def run(self):
        if self.installing:
            count = len(self.appList)
            for app in self.appList:
                list = []
                list.append(app)
                self.qObject.emit(PYSIGNAL("progress(str,str)"), (app, i18n("yüklenen")))

                if pisi.api.install(list):
                    self.qObject.emit(PYSIGNAL("incrementProgressBar(int)"), (100/count,))
                else:
                    self.qObject.emit(PYSIGNAL("error(str, str)"), (app, 'What?'))

            #self.qObject.emit(PYSIGNAL("finished()"), ('',))
            self.install = False

        elif self.upgrading:
            count = len(self.appList)
            for app in self.appList:
                list = []
                list.append(app)
                self.qObject.emit(PYSIGNAL("progress(str,str)"), (app, i18n("güncellenen")))

                if pisi.api.upgrade(list):
                    self.qObject.emit(PYSIGNAL("incrementProgressBar(int)"), (100/count,))
                else:
                    self.qObject.emit(PYSIGNAL("error(str, str)"), (app, 'What?'))
            
            #self.qObject.emit(PYSIGNAL("finished()"), ('',))
            self.upgrade = False
                                                                
        elif self.removing:
            count = len(self.appList)
            for app in self.appList:
                list = []
                list.append(app)
                self.qObject.emit(PYSIGNAL("progress(str,str)"), (app, i18n("kaldırılan")))

                if pisi.api.remove(list):
                    self.qObject.emit(PYSIGNAL("incrementProgressBar(int)"), (100/count,))
                else:
                    self.qObject.emit(PYSIGNAL("error(str, str)"), (app, 'What?'))

            #self.qObject.emit(PYSIGNAL("finished()"), ('',))
            self.remove = False
            
        else:
            # WTF?
            pass

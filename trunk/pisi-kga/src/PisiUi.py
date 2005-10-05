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

    def __init__(self, qObject):
        UI.__init__(self)
        self.qObject = qObject

    def error(self, msg):
        self.qObject.emit(PYSIGNAL("pisiError(str)"),(msg, ''))
            
    def confirm(self, msg):
        return True

    def display_progress(self, pd):
        #print 'Filename',pd['filename'],'Percent',pd['percent']
        self.qObject.emit(PYSIGNAL("updateProgressBar(str,str)"), (pd['filename'], pd['percent']))

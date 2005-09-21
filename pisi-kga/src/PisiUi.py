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

class PisiUi:

    def __init__(self, qObject):
        self.qObject = qObject

    def display(self, msg, color):
        pass
                
    def info(self, msg, verbose=False):
        pass
        
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        pass
    
    def error(self, msg):
        self.qObject.emit(PYSIGNAL("pisiError(str)"),(msg, ''))
            
    def action(self, msg):
        pass
            
    def confirm(self, msg):
        return True

    class Progress:
        def __init__(self, size):
            self.total = size
            self.percent = 0
            
        def update(self, size):
            if not self.total:
                return 100
                    
            percent = (size * 100) / self.total
            if percent and self.percent is not percent:
                self.percent = percent
                return percent
            else:
                return 0
            
    def display_progress(self, pd):
        self.qObject.emit(PYSIGNAL("updateProgressBar(str,str)"), (pd['filename'], pd['percent']))

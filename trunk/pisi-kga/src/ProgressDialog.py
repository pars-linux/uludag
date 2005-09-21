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

from Progress import *

class ProgressDialog(Progress):
    def __init__(self, Parent=None):
        Progress.__init__(self,Parent)
        self.forceClose = False
        self.setModal(True)
        self.progressBar.setTotalSteps(100)

    def forcedClose(self):
        self.forceClose = True
        self.close()
        self.forceClose = False

    def closeEvent(self, event):
        if self.forceClose:
            event.accept()
        else:
            event.ignore()

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

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

from screens.Screen import ScreenWidget
from screens.summarydlg import SummaryWidget
import screens.ScrMouse as ScrMouse
import screens.ScrWallpaper as ScrWallpaper

summaryScreens = [ScrMouse, ScrWallpaper]

class Widget(SummaryWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "You have finished !"
    desc = "See your summary.."

    def __init__(self, *args):
        apply(SummaryWidget.__init__, (self,) + args)
        for screen in summaryScreens:
            item = KListViewItem(self.listSummary,screen.summary["desc"])
            image =  QPixmap(locate("data",screen.summary["pic"]))
            item.setPixmap(0,image)

    def shown(self):
        item = self.listSummary.firstChild()
        for screen in summaryScreens:
            item.setText(1,screen.summary["sum"])
            item = item.nextSibling()

    def execute(self):
        return True


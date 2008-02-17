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
from screens.goodbyedlg import GoodbyeWidget

class Widget(GoodbyeWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Goodbye!"
    desc = "Enjoy with Pardus..."

    def __init__(self, *args):
        apply(GoodbyeWidget.__init__, (self,) + args)

    def shown(self):
        pass

    def execute(self):
        return True


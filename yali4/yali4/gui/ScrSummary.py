# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.summarywidget import Ui_SummaryWidget
import yali4.gui.context as ctx

##
# Summary screen
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('The last step before install')
    desc = _('Summary of your installation..')
    #icon = "iconKeyboard"
    help = _('''
<font size="+2">Install Summary</font>
<font size="+1">
<p>
Here you can see your install options and look at them again before installation starts.
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_SummaryWidget()
        self.ui.setupUi(self)

        #self.connect(self.ui.keyboard_list, SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"),
        #        self.slotLayoutChanged)

    def execute(self):
        ctx.debugger.log("Selected keymap is : %s" % ctx.installData.keyData["name"] )
        return True


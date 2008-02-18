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

import yali4.localedata
import yali4.localeutils
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.keyboardwidget import Ui_KeyboardWidget
import yali4.gui.context as ctx

##
# Keyboard setup screen
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Set your keyboard layout')
    desc = _('Use your keyboard layout..')
    icon = "iconKeyboard"
    help = _('''
<font size="+2">Keyboard Setup</font>

<font size="+1">
<p>
Depending on your hardware or choice select a keyboard layout from the list.
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_KeyboardWidget()
        self.ui.setupUi(self)

        # iterate over keyboard list and set default
        defaultitem = None
        for (lang, keymap) in yali4.localedata.getLangsWithKeymaps():
            if isinstance(keymap, list):
                for k in keymap:
                    ki = KeyboardItem(self.ui.keyboard_list, k)
                    if ctx.consts.lang == lang and not defaultitem:
                        defaultitem = ki
            else:
                ki = KeyboardItem(self.ui.keyboard_list, keymap)
                if ctx.consts.lang == lang and not defaultitem:
                    defaultitem = ki

        self.ui.keyboard_list.sortItems(Qt.AscendingOrder)
        self.ui.keyboard_list.setCurrentItem(defaultitem)
        self.slotLayoutChanged(defaultitem)

        self.connect(self.ui.keyboard_list, SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"),
                self.slotLayoutChanged)

    def execute(self):
        keydata = self.ui.keyboard_list.currentItem().getData()
        ctx.installData.keyData = keydata
        return True

    def slotLayoutChanged(self,i,y=None):
        if not i==y:
            keydata = i.getData()
            yali4.localeutils.set_keymap(keydata.X)

class KeyboardItem(QtGui.QListWidgetItem):

    def __init__(self, parent, keydata):
        text = "%s" %(keydata.translation)
        QtGui.QListWidgetItem.__init__(self,text,parent)
        self._keydata = keydata

    def getData(self):
        return self._keydata


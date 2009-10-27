# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
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
    desc = _('Use your keyboard layout...')
    icon = "iconKeyboard"
    help = _('''
<font size="+2">Keyboard Setup</font>
<font size="+1">
<p>
Here you can select the type of your keyboard and the language map you want to use. You can test your selection's result in the test box. 
Proceed with the installation after you make your selections.
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_KeyboardWidget()
        self.ui.setupUi(self)

        defaultitem = None
        for country,data in yali4.localedata.locales.items():
            if data["xkbvariant"]:
                i = 0
                for variant in data["xkbvariant"]:
                    _d = dict(data)
                    _d["xkbvariant"] = variant[0]
                    _d["name"] = variant[1]
                    _d["consolekeymap"] = data["consolekeymap"][i]
                    ki = KeyboardItem(self.ui.keyboard_list, _d)
                    i+=1
            else:
                ki = KeyboardItem(self.ui.keyboard_list, data)
            if ctx.consts.lang == country and not defaultitem:
                defaultitem = ki

        self.ui.keyboard_list.sortItems(Qt.AscendingOrder)
        self.ui.keyboard_list.setCurrentItem(defaultitem)
        self.slotLayoutChanged(defaultitem)

        self.connect(self.ui.keyboard_list, SIGNAL("currentItemChanged(QListWidgetItem*, QListWidgetItem*)"),
                self.slotLayoutChanged)

    def slotLayoutChanged(self, i, y=None):
        try:
            if not i==y:
                ctx.yali.setKeymap(i.getData())
        except:
            pass

    def execute(self):
        ctx.debugger.log("Selected keymap is : %s" % ctx.installData.keyData["name"] )
        return True

class KeyboardItem(QtGui.QListWidgetItem):

    def __init__(self, parent, keydata):
        text = "%s" %(keydata["name"])
        QtGui.QListWidgetItem.__init__(self, text, parent)
        self._keydata = keydata

    def getData(self):
        return self._keydata


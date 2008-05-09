# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import pisi.ui
import yali4.pisiiface
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.checkcdwidget import Ui_CheckCDWidget
import yali4.gui.context as ctx

from yali4.gui.YaliDialog import Dialog

class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Check your media')
    desc = _('To ignore media corruptions you can check your media integrity..')
    icon = "iconCD"
    help = _('''
<font size="+2">Check CD Integrity!</font>

<font size="+1">
<p>In this screen, you can check the integrity of the packages in installation CD.
</p>

''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_CheckCDWidget()
        self.ui.setupUi(self)

        self.connect(self.ui.checkButton, SIGNAL("clicked()"),
                     self.slotCheckCD)

    def slotCheckCD(self):
        self.ui.checkButton.setEnabled(False)
        self.ui.checkLabel.setText(_('<font color="#FF6D19">Please wait while checking CD.</font>'))

        # Check the CD
        ctx.yali.checkCD(self.ui)


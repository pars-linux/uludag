# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
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

from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.rescuewidget import Ui_RescueWidget
import yali4.gui.context as ctx

class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Rescue Mode')
    desc = _('You can reinstall your Grub or you can take back your system by using Pisi History...')
    icon = ""
    help = _('''
<font size="+2">Rescue Mode</font>
<font size="+1"><p>This is a rescue mode help document.</p></font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_RescueWidget()
        self.ui.setupUi(self)
        self.radios = [self.ui.useGrub, self.ui.usePisiHs]

        for radio in self.radios:
            self.connect(radio, SIGNAL("toggled(bool)"), ctx.mainScreen.enableNext)

    def updateNext(self):
        for radio in self.radios:
            if radio.isChecked():
                ctx.mainScreen.enableNext()
                return
        ctx.mainScreen.disableNext()
        ctx.mainScreen.processEvents()

    def shown(self):
        ctx.mainScreen.disableBack()
        self.updateNext()


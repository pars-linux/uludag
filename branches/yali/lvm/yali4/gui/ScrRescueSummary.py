# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# base
import os
import time
import yali4.sysutils
from yali4.gui.installdata import *

# multi language
import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

# PyQt4 Rocks
from PyQt4 import QtGui
from PyQt4.QtCore import *

# libParted
from yali4.parteddata import *
import yali4.partitionrequest as request
import yali4.partitiontype as parttype

# GUI Stuff
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.YaliDialog import WarningDialog, WarningWidget
from yali4.gui.Ui.summarywidget import Ui_SummaryWidget
import yali4.gui.context as ctx

##
# Summary screen
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('The last step before rescue')
    desc = _('Summary of your rescue operations...')
    #icon = "iconKeyboard"
    help = _('''
<font size="+2">Rescue Summary</font>
<font size="+1">
<p>
Here you can see your rescue options and look at them again before rescue operation starts.
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_SummaryWidget()
        self.ui.setupUi(self)

        self.ui.content.setText("")

        # Handle translators tool problems ..
        try:
            self.connect(self.ui.install, SIGNAL("clicked()"), ctx.mainScreen.slotNext)
            self.connect(self.ui.cancel, SIGNAL("clicked()"), self.slotReboot)
            self.connect(self.timer, SIGNAL("timeout()"), self.updateCounter)
        except:
            pass

    def slotReboot(self):
        w = WarningWidget(self)
        w.warning.setText(_('''<b><p>This action will reboot your system !</p></b>'''))
        w.ok.setText(_("Reboot"))
        dialog = WarningDialog(w, self)
        if dialog.exec_():
            yali4.sysutils.fastreboot()

    def backCheck(self):
        ctx.mainScreen.moveInc = 4
        ctx.yali.info.hide()
        return True

    def shown(self):
        ctx.mainScreen.disableNext()
        self.fillContent()

    def fillContent(self):
        subject = "<p><li><b>%s</b></li><ul>"
        item    = "<li>%s</li>"
        end     = "</ul></p>"
        content = QString("")

        content.append("""<html><body><ul>""")
        content.append("""</ul></body></html>""")

        self.ui.content.setHtml(content)

    def execute(self):
        return True


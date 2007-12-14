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
#from yali4.gui.YaliDialog import Dialog

class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Check your media')
    desc = _('To ignore media corruptions you can check your media integrity..')
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

    def showError(self):
        pass
        # make a release notes dialog
        # r = ErrorWidget(self)
        # d = Dialog(_("Check Failed"), r, self)
        # d.resize(300,200)
        # d.exec_loop()


    def slotCheckCD(self):
        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()
        self.ui.checkButton.setEnabled(False)
        self.ui.checkLabel.setText(_('<font color="#FF6D19">Please wait while checking CD.</font>'))
        yali4.pisiiface.initialize(ui=PisiUI())
        yali4.pisiiface.add_cd_repo()

        pkg_names = yali4.pisiiface.get_available()
        self.ui.progressBar.setTotalSteps(len(pkg_names))
        cur = 0
        for pkg_name in pkg_names:
            cur += 1
            if yali4.pisiiface.check_package_hash(pkg_name):
                self.ui.progressBar.setProgress(cur)
            else:
                yali4.pisiiface.finalize()
                #self.showError()
        yali4.pisiiface.finalize() 

        self.ui.checkLabel.setText(_('<font color="#257216">Check succeeded. You can proceed to the next screen.</font>'))
        ctx.mainScreen.enableNext()
        ctx.mainScreen.enableBack()

    def shown(self):
        pass
        #from os.path import basename
        #ctx.debugger.log("%s loaded" % basename(__file__))

class PisiUI(pisi.ui.UI):
    def notify(self, event, **keywords):
        pass
    def display_progress(self, operation, percent, info, **keywords):
        pass

"""
class ErrorWidget(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        l = QVBoxLayout(self)
        l.setSpacing(20)
        l.setMargin(10)

        warning = QLabel(self)
        warning.setText(_('''<b>
<p>Integrity check for packages failed. It seems that installation CD is broken.</p>
</b>
'''))

        self.reboot = QPushButton(self)
        self.reboot.setText(_("Reboot"))

        buttons = QHBoxLayout(self)
        buttons.setSpacing(10)
        buttons.addStretch(1)
        buttons.addWidget(self.reboot)

        l.addWidget(warning)
        l.addLayout(buttons)


        yali.sysutils.eject_cdrom()

        self.connect(self.reboot, SIGNAL("clicked()"),
                     self.slotReboot)

    def slotReboot(self):
        self.emit(PYSIGNAL("signalOK"), ())

"""


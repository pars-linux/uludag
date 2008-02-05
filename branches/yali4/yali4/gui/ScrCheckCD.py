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


    def showError(self):
        r = ErrorWidget(self)
        d = Dialog(_("Check Failed"), r, self)
        d.resize(300,200)
        d.exec_()

    def slotCheckCD(self):
        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()
        self.ui.checkButton.setEnabled(False)
        self.ui.checkLabel.setText(_('<font color="#FF6D19">Please wait while checking CD.</font>'))
        yali4.pisiiface.initialize(ui=PisiUI())
        yali4.pisiiface.add_cd_repo()
        ctx.mainScreen.proceesEvents()

        pkg_names = yali4.pisiiface.get_available()
        self.ui.progressBar.setMaximum(len(pkg_names))
        cur = 0
        for pkg_name in pkg_names:
            cur += 1
            if yali4.pisiiface.check_package_hash(pkg_name):
                self.ui.progressBar.setValue(cur)
            else:
                yali4.pisiiface.finalize()
                self.showError()
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

class ErrorWidget(QtGui.QWidget):
    def __init__(self, *args):
        apply(QtGui.QWidget.__init__, (self,) + args)

        self.gridlayout = QtGui.QGridLayout(self)

        self.vboxlayout = QtGui.QVBoxLayout()

        self.label = QtGui.QLabel(self)
        self.label.setText(_('''<b>
<p>Integrity check for packages failed. It seems that installation CD is broken.</p>
</b>
'''))
        self.vboxlayout.addWidget(self.label)
        self.hboxlayout = QtGui.QHBoxLayout()

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.reboot = QtGui.QPushButton(self)
        self.reboot.setFocusPolicy(Qt.NoFocus)
        self.reboot.setText(_("Reboot"))

        self.hboxlayout.addWidget(self.reboot)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.gridlayout.addLayout(self.vboxlayout,0,0,1,1)

        yali4.sysutils.eject_cdrom()

        self.connect(self.reboot, SIGNAL("clicked()"),self.slotReboot)

    def slotReboot(self):
        yali4.sysutils.reboot()


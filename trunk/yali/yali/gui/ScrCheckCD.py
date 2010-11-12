# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
_ = gettext.translation('yali', fallback=True).ugettext

from PyQt4.Qt import QWidget, SIGNAL, QIcon, QPixmap

import pisi.ui
import yali.context as ctx
import yali.pisiiface
from yali.gui import ScreenWidget
from yali.gui.Ui.checkcdwidget import Ui_CheckCDWidget

from yali.gui.YaliDialog import Dialog

class Widget(QWidget, ScreenWidget):
    name = "mediaCheck"
    title = _("Check the Integrity of Packages")
    icon = "media-optical-small"
    help = _("""Here you can validate the integrity of the installation packages. A failed validation usually is a sign of a badly mastered installation medium (CD, DVD or USB storage).
If you are using an optical installation medium, try burning the installation image using DAO (Disc-at-once) mode, at a lower speed (4x for DVD, 8-12x for CD).
""")

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_CheckCDWidget()
        self.ui.setupUi(self)

        self.check_media_stop = True

        self.connect(self.ui.checkButton, SIGNAL("clicked()"), self.slotCheckCD)
        if ctx.consts.lang == "tr":
            self.ui.progressBar.setFormat("%%p")

    def shown(self):
        self.ui.validationSucceedBox.hide()
        self.ui.validationFailBox.hide()
        self.ui.progressBar.hide()

    def slotCheckCD(self):
        if self.check_media_stop:
            self.check_media_stop = False
            self.ui.progressBar.show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/gui/pics/dialog-error.png"), QIcon.Normal, QIcon.Off)
            self.ui.checkButton.setIcon(icon)
            self.ui.checkButton.setText("")
            self.checkMedia()
        else:
            self.check_media_stop = True
            self.ui.progressBar.show()
            icon = QIcon()
            icon.addPixmap(QPixmap(":/gui/pics/task-accepted.png"), QIcon.Normal, QIcon.Off)
            self.ui.checkButton.setIcon(icon)
            self.ui.checkButton.setText(_("Validate"))

    def checkMedia(self):
        ctx.mainScreen.disableNext()
        ctx.mainScreen.disableBack()

        ctx.interface.informationWindow.update(_("Starting validation..."))
        class PisiUI(pisi.ui.UI):
            def notify(self, event, **keywords):
                pass
            def display_progress(self, operation, percent, info, **keywords):
                pass

        yali.pisiiface.initialize(ui=PisiUI(), with_comar=False, nodestDir=True)
        yali.pisiiface.addCdRepo()
        ctx.mainScreen.processEvents()
        pkg_names = yali.pisiiface.getAvailablePackages()

        self.ui.progressBar.setMaximum(len(pkg_names))

        cur = 0
        flag = 0
        for pkg_name in pkg_names:
            cur += 1
            ctx.logger.debug("Validating %s " % pkg_name)
            ctx.interface.informationWindow.update(_("Validating %s") % pkg_name)
            if self.check_media_stop:
                continue
            try:
                yali.pisiiface.checkPackageHash(pkg_name)
                self.ui.progressBar.setValue(cur)
            except:
                rc  = ctx.interface.messageWindow(_("Warning"),
                                                  _("Validation of %s package failed."
                                                    "Please remaster your installation medium and"
                                                    "reboot.") % pkg_name,
                                                  type="custom", customIcon="error",
                                                  customButtons=[_("Skip Validation"), _("Skip Package"), _("Reboot")],
                                                  default=0)
                flag = 1
                if not rc:
                    self.ui.validationBox.hide()
                    self.ui.validationFailBox.show()
                    ctx.mainScreen.enableNext()
                    break
                elif rc == 1:
                    continue
                else:
                    yali.util.reboot()


        if not self.check_media_stop and flag == 0:
            ctx.interface.informationWindow.update(_('<font color="#FFF"><b>Validation succeeded. You can proceed with the installation.</b></font>'))
            self.ui.validationSucceedBox.show()
            self.ui.validationBox.hide()
        else:
            ctx.interface.informationWindow.hide()
            self.ui.progressBar.setValue(0)

        yali.pisiiface.removeRepo(ctx.consts.cd_repo_name)

        ctx.mainScreen.enableNext()
        ctx.mainScreen.enableBack()

        ctx.interface.informationWindow.hide()



#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

# Edit widget
from diskmanager.edit import EditWidget


class PageDialog(kdeui.KPageDialog):
    def __init__(self, parent):
        kdeui.KPageDialog.__init__(self, parent)

        self.setFaceType(kdeui.KPageDialog.Tabbed)
        self.setCaption(kdecore.i18n("Settings"))

        self.page_widget = EditWidget(self)
        self.page_item = kdeui.KPageWidgetItem(self.page_widget, kdecore.i18n("Settings"))

        self.addPage(self.page_item)

        self.edit = self.page_widget

    def slotButtonClicked(self, button):
        if button == kdeui.KPageDialog.Ok:
            if self.validate():
                kdeui.KPageDialog.slotButtonClicked(self, button)
        else:
            kdeui.KPageDialog.slotButtonClicked(self, button)

    def validate(self):
        if self.page_widget.getAutoMount():
            if not self.page_widget.getMountPoint():
                QtGui.QMessageBox.information(self, kdecore.i18n('Error'), kdecore.i18n("Mount point is required"))
                return False
        return True


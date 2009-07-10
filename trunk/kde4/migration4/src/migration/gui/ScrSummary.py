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

import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n ,i18n


from migration.gui.ScreenWidget import ScreenWidget
from migration.gui.ui.summaryWidget import Ui_summaryWidget
from migration.gui import context as ctx

class Widget(QtGui.QWidget, ScreenWidget):
    title = i18n("Summary")
    desc = i18n("Welcome to Migration Tool Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_summaryWidget()
        self.ui.setupUi(self)

    def shown(self):
        subject = "<p><li><b>%s</b></li><ul>"
        item    = "<li>%s</li>"
        end     = "</ul></p>"
        content = QString("")

        content.append("""<html><body><ul>""")

        # Selected User
        content.append(subject % ki18n("User Settings").toString())
        content.append(item % ki18n("Selected User: <b>%s</b>").toString() % ctx.user[2])
        content.append(end)

        # Selected Options
        content.append(subject % ki18n("Options Settings").toString())
        for option in ctx.options:
            content.append(item % ki18n("Selected Options: <b>%s</b>").toString() % option)
        content.append(end)

        #Selected Files Destinations
        content.append(subject % ki18n("Destination Settings").toString())
        if ctx.fileOptions.has_key("links"):
            for link in ctx.fileOptions["links"]:
                content.append(item % ki18n("Selected Destination: <b>Copy Link to %s</b>").toString() % link)
        elif ctx.fileOptions.has_key("copy destination"):
            content.append(item % ki18n("Selected Destination: <b>Copy Destination to %s</b>").toString() % ctx.fileOptions["copy destination"])

        content.append(end)

        content.append("""</ul></body></html>""")
        self.ui.textSummary.setHtml(content)

    def execute(self):
        return True

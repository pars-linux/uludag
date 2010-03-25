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
#from PyKDE4.kdecore import i18n ,i18n


from migration.gui.ScreenWidget import ScreenWidget
from migration.gui.ui.summaryWidget import Ui_summaryWidget

from migration.gui.context import *

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
        content.append(subject % i18n("User Settings"))
        content.append(item % i18n("Selected User: <b>%s</b>") % user[2])
        content.append(end)

        # Selected Options
        content.append(subject % i18n("Options Settings"))
        for key,value in context.options.items():
            content.append(item % i18n("Option %1 : <b>%2</b>") % (key, value))
        content.append(end)

        if context.filesOptions:
            #Selected Files Destinations
            content.append(subject % i18n("Destination Settings"))
            if context.filesOptions.has_key("links"):
                for link in context.filesOptions["links"]:
                    content.append(item % i18n("Linked Destination to: <b> %s </b>") % link)
            elif context.filesOptions.has_key("copy destination"):
                content.append(item % i18n("Copied Destination to: <b> %s </b>") % filesOptions["copy destination"])

            content.append(end)

        content.append("""</ul></body></html>""")
        self.ui.textSummary.setHtml(content)

    def execute(self):
        return (True, None)

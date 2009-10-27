#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import dbus

from PyKDE4.kdeui import KCModule, KIcon
from PyKDE4.kdecore import KGlobal

from displaysettings.about import catalog
from displaysettings.deviceswidget import MainWidget


class Module(KCModule):
    def __init__(self, component_data, parent):
        KCModule.__init__(self, component_data, parent)

        KGlobal.locale().insertCatalog(catalog)
        self.setButtons(KCModule.Apply)

        if not dbus.get_default_main_loop():
            from dbus.mainloop.qt import DBusQtMainLoop
            DBusQtMainLoop(set_as_default=True)

        mw = MainWidget(self, embed=True)
        self.load = mw.load
        self.save = mw.save
        self.defaults = mw.defaults

        def configChanged():
            self.changed.emit(True)

        mw.configChanged.connect(configChanged)


def CreatePlugin(widget_parent, parent, component_data):
    return Module(component_data, parent)

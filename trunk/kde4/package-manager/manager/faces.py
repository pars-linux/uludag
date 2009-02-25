#!/usr/bin/python
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

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from uimain import Ui_MainManager
from uiitem import Ui_PackageWidget

import pmtools

class PackageWidgetItem(QtGui.QListWidgetItem):
    def __init__(self, parent):
        QtGui.QListWidgetItem.__init__(self, parent)

class PackageWidget(QtGui.QWidget):
    def __init__(self, parent, name, summary):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_PackageWidget()
        self.ui.setupUi(self)

        self.ui.labelName.setText(name)
        self.ui.labelSummary.setText(unicode(summary))

class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_MainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        # Init pm
        self.iface = pmtools.Iface()

        # Initialize
        self.initialize()

    def initialize(self):
        packages = self.iface.getPackageList()
        for name in packages:
            package = self.iface.getPackage(name)
            widget = PackageWidget(self, package.name, unicode(package.summary))
            widget_item = PackageWidgetItem(self.ui.packageList)
            self.ui.packageList.setItemWidget(widget_item, widget)
            widget_item.setSizeHint(QSize(100, 48))

    def addComponent(self, name, icon, no_of_pkgs):
        item = QtGui.QListWidgetItem(self.ui.componentList)
        item.setText("%s (%s)" % (i18n(name), no_of_pkgs))
        item.setIcon(KIconLoader().loadIcon(icon, KIconLoader.Desktop, KIconLoader.SizeMedium))

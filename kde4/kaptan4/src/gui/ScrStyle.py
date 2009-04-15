# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n, KStandardDirs, KGlobal

import os, sys, Image

from gui.ScreenWidget import ScreenWidget
from gui.styleWidget import Ui_styleWidget
from stylewidget import StyleItemWidget

from desktopparser import DesktopParser
from ConfigParser import ConfigParser

class Widget(QtGui.QWidget, ScreenWidget):
    # Set title and description for the information widget
    title = ki18n("Some catchy title about styles")
    desc = ki18n("Some catchy description about styles")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_styleWidget()
        self.ui.setupUi(self)

        """
        # TODO: Add styles as a resource type. It doesn't work, though.
        KGlobal.dirs().addResourceType("styles", "data", "/usr/kde/4/share/styles/")
        lst= KStandardDirs().findAllResources("styles")
        """

        lst= KStandardDirs().findAllResources("wallpaper", "sample*.desktop", KStandardDirs.Recursive)

        for desktopFiles in lst:
            parser = DesktopParser()
            parser.read(str(desktopFiles))

            try:
                styleName = parser.get_locale('Style', 'Name', '')
                styleDesc = parser.get_locale('Style', 'Description', '')
                styleTheme = parser.get_locale('Style', 'Style', '')
                styleApplet = parser.get_locale('Style', 'Applets', '')
                styleColorScheme = parser.get_locale('Style', 'ColorScheme', '')
                styleWindowDecoration = parser.get_locale('Style', 'WindowDecoration', '')
                styleThumb = os.path.join(os.path.split(str(desktopFiles))[0],  parser.get_locale('Style', 'Thumbnail',''))

                item = QtGui.QListWidgetItem(self.ui.listStyles)
                widget = StyleItemWidget(unicode(styleName), unicode(styleDesc), styleThumb, self.ui.listStyles)
                self.ui.listStyles.setItemWidget(item, widget)
                item.setSizeHint(QSize(38,110))
            except:
                print "Warning! Invalid syntax in ", desktopFiles

        self.ui.listStyles.connect(self.ui.listStyles, SIGNAL("itemSelectionChanged()"), self.setStyle)

    def setStyle(self):
        # TODO: Use Gokmen's DBus call when it's ready
        pass

    def shown(self):
        pass

    def execute(self):
        return True



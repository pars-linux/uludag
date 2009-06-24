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
from PyQt4.QtGui import QFileDialog

from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n, KStandardDirs, KGlobal, KConfig
import os, sys, subprocess

from gui.ScreenWidget import ScreenWidget
from gui.wallpaperWidget import Ui_wallpaperWidget
from widgets import WallpaperItemWidget

from desktopparser import DesktopParser
from ConfigParser import ConfigParser


class Widget(QtGui.QWidget, ScreenWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # title and description at the top of the dialog window
    title = ki18n("Insert some catchy title about wallpapers..")
    desc = ki18n("Wonderful, awesome, superb wallpapers! \m/")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_wallpaperWidget()
        self.ui.setupUi(self)
        # Get system locale
        self.catLang = KGlobal.locale().language()

        isWide = lambda x: float(x[0]) / float(x[1]) >= 1.6
        isSquare = lambda x: float(x[0]) / float(x[1]) < 1.6

        # Get screen resolution
        rect =  QtGui.QDesktopWidget().screenGeometry()

        # Get metadata.desktop files from shared wallpaper directory
        lst= KStandardDirs().findAllResources("wallpaper", "*metadata.desktop", KStandardDirs.Recursive)

        for desktopFiles in lst:
            parser = DesktopParser()
            parser.read(str(desktopFiles))

            try:
                wallpaperTitle = parser.get_locale('Desktop Entry', 'Name[%s]'%self.catLang, '')
            except:
                wallpaperTitle = parser.get_locale('Desktop Entry', 'Name', '')

            try:
                wallpaperDesc = parser.get_locale('Desktop Entry', 'X-KDE-PluginInfo-Author', '')
            except:
                wallpaperDesc = "Unknown"

            # Get all files in the wallpaper's directory
            l = os.listdir(os.path.join(os.path.split(str(desktopFiles))[0], "contents/images"))

            wallpaperFile = os.path.split(str(desktopFiles))[0]
            wallpaperThumb = os.path.join(os.path.split(str(desktopFiles))[0], "contents/screenshot.png")

            # Insert wallpapers to listWidget.
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            # Each wallpaper item is a widget. Look at widgets.py for more information.
            widget = WallpaperItemWidget(unicode(wallpaperTitle), unicode(wallpaperDesc), wallpaperThumb, self.ui.listWallpaper)
            item.setSizeHint(QSize(38,110))
            self.ui.listWallpaper.setItemWidget(item, widget)
            # Add a hidden value to each item for detecting selected wallpaper's path.
            item.setStatusTip(wallpaperFile)

        self.ui.listWallpaper.connect(self.ui.listWallpaper, SIGNAL("itemSelectionChanged()"), self.setWallpaper)
        self.ui.checkBox.connect(self.ui.checkBox, SIGNAL("stateChanged(int)"), self.disableWidgets)
        self.ui.buttonChooseWp.connect(self.ui.buttonChooseWp, SIGNAL("clicked()"), self.selectWallpaper)

    def disableWidgets(self, state):
        if state:
            self.__class__.screenSettings["hasChanged"] = False
            self.ui.buttonChooseWp.setDisabled(True)
            self.ui.listWallpaper.setDisabled(True)
        else:
            self.__class__.screenSettings["hasChanged"] = True
            self.ui.buttonChooseWp.setDisabled(False)
            self.ui.listWallpaper.setDisabled(False)

    def setWallpaper(self):
        self.__class__.screenSettings["selectedWallpaper"] =  self.ui.listWallpaper.currentItem().statusTip()
        self.__class__.screenSettings["hasChanged"] = True

    def selectWallpaper(self):
        selectedFile = QFileDialog.getOpenFileName(None,"Open Image", os.path.expanduser("~"), 'Image Files (*.png *.jpg *bmp)')

        if selectedFile.isNull():
            return
        else:
            item = QtGui.QListWidgetItem(self.ui.listWallpaper)
            wallpaperName = os.path.splitext(os.path.split(str(selectedFile))[1])[0]
            widget = WallpaperItemWidget(unicode(wallpaperName), unicode("Unknown"), selectedFile, self.ui.listWallpaper)
            self.ui.listWallpaper.setItemWidget(item, widget)
            item.setSizeHint(QSize(38,110))
            item.setStatusTip(selectedFile)

    def shown(self):
        pass

    def execute(self):
        return True



# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

import os
import kdecore
import dcopext
import sys

# parser for .desktop files
from desktopparser import DesktopParser
import ConfigParser

# import gui's
from screens.Screen import ScreenWidget
from screens.wallpaperdlg import WallpaperWidget

# set summary picture and description
summary = {"sum" : "",
           "pic" : "kaptan/pics/summary/wallpaperSummary.png",
           "desc": i18n("Wallpaper")}

# create a dcopclient for wallpaper
dcopclient = kdecore.KApplication.dcopClient()
dcopclient.registerAs("changewp")
dcopapp = dcopext.DCOPApp("kdesktop", dcopclient)
current =  dcopapp.KBackgroundIface.currentWallpaper(1)[1]

class Widget(WallpaperWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Set your Wallpaper !"
    desc = "Enjoy with wonderful backgrounds..."
    icon = summary["pic"]

    def __init__(self, *args):
        apply(WallpaperWidget.__init__, (self,) + args)

        self.listWallpaper.setSorting(-1)

        #set background image
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.wallpaperList = {}
        lst = {}


        # get .desktop files from global resources
        lst= KGlobal.dirs().findAllResources("wallpaper", "*.desktop", False , True )

        #TODO: maybe we can show wallpapers which haven't got .desktop files?
        #TODO: show wallpapers depend on resolution
        for desktopFiles in lst:
            #eliminate svgz files
            if not desktopFiles.endsWith(".svgz.desktop"):
                #parse .desktop file
                parser = DesktopParser()
                parser.read(str(desktopFiles))
                try:
                    wallpaperTitle = parser.get_locale('Wallpaper', 'Name', '')
                    #maybe show author too?
                    #wallpaperAuthor = parser.get_locale('Wallpaper', 'Author', '')
                    wallpaperFile = parser.get_locale('Wallpaper', 'File','')
                    #TODO: don't hardcode the path. strip or sth.
                    wallpaperFile = "/usr/kde/3.5/share/wallpapers/"+wallpaperFile
                    #dict titles and file names
                    self.wallpaperList[wallpaperTitle] = wallpaperFile
                    #self.listWallpaperItem(wallpaperTitle, QImage(wallpaperFile))
                except ConfigParser.NoOptionError:
                    #if option doesn't exist, skip.
                    pass

        self.sortedWallpapers = self.dictSort(self.wallpaperList)
        self.sortedWallpapers.reverse()

        for i in self.sortedWallpapers:
            self.listWallpaperItem(i, QImage(self.wallpaperList[i]))

        # set the wallpaper which has been using before kaptan started.
        if current:
            wallpaperTitle = "Current Wallpaper"
            wallpaperFile = current

            self.wallpaperList[wallpaperTitle]= wallpaperFile
            self.listWallpaperItem(wallpaperTitle, QImage(wallpaperFile))
        #if there's no wallpaper
        else:
            wallpaperTitle = "No Wallpaper"
            wallpaperFile = "kaptan/pics/no-wallpaper.png"

            self.wallpaperList[wallpaperTitle]= wallpaperFile

        self.listWallpaper.setSelected(self.listWallpaper.firstChild(),True)
        self.listWallpaper.connect(self.listWallpaper, SIGNAL("selectionChanged()"), self.setWallpaper)

    def dictSort(self, wallDict):
        keys = wallDict.keys()
        keys.sort()
        return keys

    def shown(self):
        pass

    def setWallpaper(self):
        #change wallpaper
        selectedWallpaper = self.wallpaperList[str(self.listWallpaper.currentItem().text(0))]
        dcopapp.KBackgroundIface.setWallpaper(selectedWallpaper, 6)

    def listWallpaperItem(self, itemText, file):
        item = KListViewItem(self.listWallpaper,"file")
        item.setText(0,i18n(itemText))
        item.setPixmap(0,QPixmap(QImage(file).smoothScale(150,150, QImage.ScaleMin)))

    def execute(self):
        summary["sum"] = self.listWallpaper.currentItem().text(0)


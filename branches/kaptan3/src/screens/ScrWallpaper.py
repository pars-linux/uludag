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

        #set background image
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.checkAllWallpapers.setText(i18n("Show all resolutions."))
        self.listWallpaper.setSorting(-1)

        self.currentText = QString(i18n("Old Wallpaper"))
        self.noneText = str(i18n("No Wallpaper"))
        self.nonePic = "kaptan/pics/no-wallpaper.png"
        self.wallpaperList = {}
        self.wideWallpapers = {}
        self.normalWallpapers = {}
        lst = {}

        #detect screen size
        self.isWide = False
        rect =  QApplication.desktop().screenGeometry()

        if float(rect.width())/float(rect.height()) >=  1.6:
            self.isWide = True

        # get .desktop files from global resources
        lst= KGlobal.dirs().findAllResources("wallpaper", "*.desktop", False , True )

        for desktopFiles in lst:
            #eliminate svgz files
            if not desktopFiles.endsWith(".svgz.desktop"):
                #parse .desktop file
                parser = DesktopParser()
                parser.read(str(desktopFiles))
                try:
                    #FYI: there must have been a Resolution=Wide tag in wallpaper file.
                    resolution =  parser.get_locale('Wallpaper', 'Resolution', '')
                except ConfigParser.NoOptionError:
                    resolution = False
                try:
                    wallpaperTitle = parser.get_locale('Wallpaper', 'Name', '')
                    wallpaperFile = parser.get_locale('Wallpaper', 'File','')

                    #TODO: don't hardcode the path. strip or sth.
                    wallpaperFile = "/usr/kde/3.5/share/wallpapers/"+wallpaperFile
                    #dict titles and file names
                    #get wide wallpapers
                    if self.isWide == True and resolution == "Wide":
                        self.wideWallpapers[wallpaperTitle] = wallpaperFile 
                    #get normal size wallpapers
                    elif self.isWide == False and not resolution:
                        self.normalWallpapers[wallpaperTitle] = wallpaperFile
                    #gather all wallpapers
                    self.wallpaperList[wallpaperTitle] = wallpaperFile
                except ConfigParser.NoOptionError:
                    #if option doesn't exist, skip.
                    pass

        if self.isWide == True:
            self.sortAndList(self.wideWallpapers)
        else:
            self.sortAndList(self.normalWallpapers)

        self.listWallpaper.setSelected(self.listWallpaper.firstChild(),True)
        self.listWallpaper.connect(self.listWallpaper, SIGNAL("selectionChanged()"), self.setWallpaper)
        self.checkAllWallpapers.connect(self.checkAllWallpapers, SIGNAL("toggled(bool)"), self.showAllWallpapers)

    def setCurrentWallpaper(self):
        if current:
            self.listWallpaperItem(self.currentText, QImage(current))
            self.wallpaperList["Current Wallpaper"] = current
            if "Current Wallpaper" in self.wallpaperList:
                self.wallpaperList.pop("Current Wallpaper")

        else:
            wallpaperFile = "kaptan/pics/no-wallpaper.png"
            self.listWallpaperItem("No Wallpaper", current)
            self.wallpaperList["No Wallpaper"]= wallpaperFile

    def sortAndList(self, specList):
        self.sortedWallpapers = self.dictSort(specList)
        self.sortedWallpapers.reverse()
        if current:
            specList[self.currentText] = current
            self.wallpaperList[self.currentText] = current
            if self.currentText in self.sortedWallpapers:
                self.sortedWallpapers.remove(self.currentText)
            self.sortedWallpapers.append(self.currentText)
        else:
            specList[self.noneText] = self.nonePic
            self.wallpaperList[self.noneText] = self.nonePic
            if self.noneText in self.sortedWallpapers:
                self.sortedWallpapers.remove(self.noneText)
            self.sortedWallpapers.append(self.noneText)

        for i in self.sortedWallpapers:
            self.listWallpaperItem(i, QImage(specList[i]))

    def showAllWallpapers(self):
        if self.checkAllWallpapers.isChecked():
            self.listWallpaper.clear()
            self.sortAndList(self.wallpaperList)
        else:
            self.listWallpaper.clear()
            if self.isWide:
                self.sortAndList(self.wideWallpapers)
            else:
                self.sortAndList(self.normalWallpapers)

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
        item.setText(0,itemText)
        item.setPixmap(0,QPixmap(QImage(file).smoothScale(150,150, QImage.ScaleMin)))

    def execute(self):
        summary["sum"] = self.listWallpaper.currentItem().text(0)


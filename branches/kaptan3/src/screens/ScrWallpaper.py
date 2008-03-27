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
import StringIO
import os
import kdecore
import dcopext
import sys
import Image
import glob

# parser for .desktop files
from desktopparser import DesktopParser
import ConfigParser

# import gui's
from screens.Screen import ScreenWidget
from screens.wallpaperdlg import WallpaperWidget

# create a dcopclient for wallpaper
dcopclient = kdecore.KApplication.dcopClient()
dcopclient.registerAs("changewp")
dcopapp = dcopext.DCOPApp("kdesktop", dcopclient)
current =  dcopapp.KBackgroundIface.currentWallpaper(1)[1]

class Widget(WallpaperWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Set your Wallpaper !"
    desc = "Enjoy with wonderful backgrounds..."
    icon = "kaptan/pics/icons/wallpaper.png"

    def __init__(self, *args):
        apply(WallpaperWidget.__init__, (self,) + args)

        #set background image
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.checkAllWallpapers.setText(i18n("Show all resolutions."))
        self.listWallpaper.setSorting(-1)

        self.currentText = QString(i18n("Old Wallpaper"))
        self.noneText = QString(i18n("No Wallpaper"))
        self.nonePic = "kaptan/pics/no-wallpaper.png"
        self.wallpaperList = {}
        self.ultimateList = []
        self.wideList = {}
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
                    if resolution == "Wide":
                        self.wideList[wallpaperFile] = wallpaperTitle
                    #get normal size wallpapers
                    self.wallpaperList[wallpaperFile] = wallpaperTitle

                except ConfigParser.NoOptionError:
                    #if option doesn't exist, skip.
                    pass

        self.sortedWallpaperList = self.dictSort(self.wallpaperList)
        self.resize_images()

        for i in self.sortedWallpaperList:
            for wallpaperFile, wallpaperTitle in self.wallpaperList.items():
                if wallpaperTitle == i:
                    item = KListViewItem(self.listWallpaper, "file", str(wallpaperFile))
                    item.setText(0,wallpaperTitle)
                    item.setPixmap(0,QPixmap(QImage("/tmp/"+ os.path.basename(wallpaperFile) +".thumbnail")))

                    if wallpaperFile in self.wallpaperList.keys():
                        if wallpaperFile in self.wideList.keys():
                            self.ultimateList.append({ "Wide": item })
                    #get normal size wallpapers
                        else:
                            self.ultimateList.append({"Normal": item})
        if current:
            self.wallpaperList[current] = self.currentText
            item = KListViewItem(self.listWallpaper, "file", str(current))
            item.setText(0,self.currentText)
            item.setPixmap(0,QPixmap(QImage(current+".thumbnail")))

        else:
            self.wallpaperList[self.nonePic] = self.noneText
            item = KListViewItem(self.listWallpaper, "file", str(self.nonePic))
            item.setText(0,self.noneText)
            #item.setPixmap(0,QPixmap(self.stretch(QImage(self.nonePic))))

        if self.isWide == True:
            self.hideNormals()
        else:
            self.hideWides()

        self.listWallpaper.setSelected(self.listWallpaper.firstChild(),True)
        self.listWallpaper.connect(self.listWallpaper, SIGNAL("selectionChanged()"), self.setWallpaper)
        self.checkAllWallpapers.connect(self.checkAllWallpapers, SIGNAL("toggled(bool)"), self.showAllWallpapers)

    def resize_images(self):
        size = 150, 150
        for infile in self.wallpaperList:
            hede =  "/tmp/" + os.path.splitext(os.path.basename(infile))[0]
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(hede + ".thumbnail", "PNG")
            

    def stretch(self,imo,filter=Image.NEAREST):
        im = Image.open(imo)
        im = im._new(im.stretch(150, filter))
        return im

    def showAllWallpapers(self):
        if self.checkAllWallpapers.isChecked():
            self.showAll()
        else:
            if self.isWide == True:
                self.hideNormals()
            else:
                self.hideWides()

    def showAll(self):
        for i in self.ultimateList:
            for p in i.values():
                p.setVisible(True)

    def hideNormals(self):
        for i in self.ultimateList:
            for p, s in  i.items():
                if p == "Normal":
                    s.setVisible(False)

    def hideWides(self):
        for i in self.ultimateList:
            for p, s in  i.items():
                if p == "Wide":
                    s.setVisible(False)

    def dictSort(self, wallDict):
        vals = wallDict.values()
        vals.sort()
        vals.reverse()
        return vals

    def shown(self):
        pass

    def setWallpaper(self):
        #change wallpaper
        for i in self.wallpaperList.values():
            if i == self.listWallpaper.currentItem().text(0):
                selectedWallpaper = self.listWallpaper.currentItem().key(1,True)
                dcopapp.KBackgroundIface.setWallpaper(selectedWallpaper, 6)

    def execute(self):
        pass


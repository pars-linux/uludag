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
import logging

from qt import QFileDialog

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
    desc = i18n("Enjoy with wonderful backgrounds...")
    icon = "kaptan/pics/icons/wallpaper.png"

    def __init__(self, *args):
        apply(WallpaperWidget.__init__, (self,) + args)

        # set texts 
        self.checkAllWallpapers.setText(i18n("Show all resolutions."))
        self.currentText = QString(i18n("Old Wallpaper"))
        self.noneText = QString(i18n("No Wallpaper"))

        # set images
        self.setPaletteBackgroundPixmap(QPixmap(locate("data", "kaptan/pics/middleWithCorner.png")))
        self.nonePic = "kaptan/pics/no-wallpaper.jpg"

        # reverse sorting
        self.listWallpaper.setSorting(-1)

        # set/create variables
        self.tmpThumbDir = os.path.join(os.path.expanduser("~"), ".kde/share/apps/kaptan/kaptan-thumbs")

        self.catLang = KGlobal.locale().language()

        self.thumbSize = 150, 150
        self.wallpaperList = {}
        self.ultimateList = []
        self.wideList = {}
        self.topList = {}
        lst = {}

        # create temp directory for wallpaper thumbnails
        if not os.path.exists(self.tmpThumbDir):
            os.makedirs(self.tmpThumbDir)

        # detect if screen is wide or not
        self.isWide = False
        rect =  QApplication.desktop().screenGeometry()

        if float(rect.width())/float(rect.height()) >=  1.6:
            self.isWide = True

        # get .desktop files from global resources
        lst= KGlobal.dirs().findAllResources("wallpaper", "*.desktop", False , True )

        for desktopFiles in lst:
            # eliminate svgz files
            if not desktopFiles.endsWith(".svgz.desktop"):
                # parse .desktop file
                parser = DesktopParser()
                parser.read(str(desktopFiles))

                try:
                    # FYI: there must have been a Resolution=Wide tag in wallpaper file.
                    resolution =  parser.get_locale('Wallpaper', 'Resolution', '')
                except ConfigParser.NoOptionError:
                    resolution = False

                try:
                    isOnTop = parser.get_locale('Wallpaper', 'OnTop', '')
                except ConfigParser.NoOptionError:
                    isOnTop = False

                try:
                    try:
                        wallpaperTitle = parser.get_locale('Wallpaper', 'Name[%s]'%self.catLang, '')
                    except:
                        wallpaperTitle = parser.get_locale('Wallpaper', 'Name', '')

                    wallpaperTitle = QString(i18n(wallpaperTitle))

                    wallpaperFile = "/usr/kde/3.5/share/wallpapers/" + parser.get_locale('Wallpaper', 'File','')

                    # get wide wallpapers
                    if resolution == "Wide":
                        self.wideList[wallpaperFile] = wallpaperTitle

                    # list the exclusive wallpapers
                    if isOnTop:
                        self.topList[wallpaperFile] = wallpaperTitle

                    # get normal size wallpapers
                    self.wallpaperList[wallpaperFile] = wallpaperTitle
                except ConfigParser.NoOptionError, e:
                    logging.debug("No Option Error: " + str(e))

        self.sortedWallpaperList = self.dictSort(self.wallpaperList)
        self.resizeImages(self.wallpaperList)

        for i in self.sortedWallpaperList:
            for wallpaperFile, wallpaperTitle in self.wallpaperList.items():
                if wallpaperTitle == i:
                    item = KListViewItem(self.listWallpaper, "file", str(wallpaperFile))
                    item.setText(0,wallpaperTitle)
                    wpCurrentThumbnail = os.path.join(self.tmpThumbDir,  os.path.basename(wallpaperFile) + ".thumbnail")
                    if os.path.exists(wpCurrentThumbnail):
                        item.setPixmap(0,QPixmap(QImage(wpCurrentThumbnail)))
                    elif os.path.exists(os.path.join(self.tmpThumbDir,  os.path.basename(wallpaperFile).replace("png", "jpg") + ".thumbnail")):
                        item.setPixmap(0,QPixmap(QImage(os.path.join(self.tmpThumbDir, os.path.basename(wallpaperFile).replace("png", "jpg") + ".thumbnail"))))
                    else:
                        item.setPixmap(0,QPixmap(QImage(locate("data", self.nonePic))))

                    if wallpaperFile in self.wallpaperList.keys():
                        if wallpaperFile in self.wideList.keys():
                            self.ultimateList.append({ "Wide": item })
                        # get normal size wallpapers
                        else:
                            self.ultimateList.append({"Normal": item})
        if current:
            self.wallpaperList[current] = self.currentText
            self.setWps(current,self.currentText)
        else:
            self.wallpaperList[self.nonePic] = self.noneText
            self.setWps(self.nonePic, self.noneText)

        if self.isWide == True:
            self.hideNormals()
        else:
            self.hideWides()

        self.listWallpaper.setSelected(self.listWallpaper.firstChild(),True)
        self.listWallpaper.connect(self.listWallpaper, SIGNAL("selectionChanged()"), self.setWallpaper)
        self.checkAllWallpapers.connect(self.checkAllWallpapers, SIGNAL("toggled(bool)"), self.showAllWallpapers)
        self.buttonChooseWp.connect(self.buttonChooseWp, SIGNAL("clicked()"), self.chooseWallpaper)

    def chooseWallpaper(self):
        prog = QFileDialog.getOpenFileName(os.path.expanduser("~") , self.trUtf8("Images (*.jpg *.png *.gif *.jpeg)"), )

        if prog.isNull():
            return

        item = KListViewItem(self.listWallpaper, "file", str(prog))
        wallName = str(prog).split("/")[-1]
        self.wallpaperList[prog] = wallName

        item.setText(0, wallName)
        eheh = QPixmap(QImage(locate("data", prog)).smoothScale(150,150, QImage.ScaleMin))
        item.setPixmap(0,eheh)

    def setWps(self, wpFile, wpTitle):
        item = KListViewItem(self.listWallpaper, "file", str(wpFile))
        item.setText(0,wpTitle)
        wpCurrentThumbnail = os.path.join(self.tmpThumbDir,  os.path.basename(wpFile) + ".thumbnail")

        if os.path.exists(wpCurrentThumbnail):
            item.setPixmap(0,QPixmap(QImage(wpCurrentThumbnail)))
        elif os.path.exists(os.path.join(self.tmpThumbDir,  os.path.basename(wpFile).replace("png", "jpg") + ".thumbnail")):
            item.setPixmap(0,QPixmap(QImage(os.path.join(self.tmpThumbDir, os.path.basename(wpFile).replace("png", "jpg") + ".thumbnail"))))
        else:
            item.setPixmap(0,QPixmap(QImage(locate("data", self.nonePic))))

    def resizeImages(self, resizeList):
        if current:
            resizeList[current] = self.currentText

        for infile in resizeList:
            tmpDir = os.path.join(self.tmpThumbDir, os.path.splitext(os.path.basename(infile))[0])
            try:
                im = Image.open(infile)
                im.thumbnail(self.thumbSize, Image.NEAREST)
                im.save(tmpDir + ".jpg.thumbnail", "PNG")
            except IOError, e:
                logging.debug("IO Error: " + str(e))

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

        # put the exclusive wallpapers on the top of the list
        tmpList = []

        for i in vals:
            for each in self.topList.values():
                if i == each:
                    vals.remove(each)
                    tmpList.append(each)

        for i in tmpList:
            vals.append(i)

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


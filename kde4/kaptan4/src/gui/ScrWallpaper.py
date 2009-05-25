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

            # Get the (Wide || Square) wallpaper with the highest available resolution
            if float(rect.width())/float(rect.height()) >=  1.6:
                self.screenRes = "x".join(sorted(filter(isWide, [os.path.splitext(x)[0].split("x") for x in l]))[-1])
            else:
                self.screenRes = "x".join(sorted(filter(isSquare, [os.path.splitext(x)[0].split("x") for x in l]))[-1])

            # Get wallpaper's path and thumbnail. Note that the thumbnail should be located at @wallpaper/contents/screenshot.png
            #wallpaperFile = glob.glob(os.path.join(os.path.split(str(desktopFiles))[0], "contents/images", self.screenRes + ".*"))[0]
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
        self.ui.buttonChooseWp.connect(self.ui.buttonChooseWp, SIGNAL("clicked()"), self.selectWallpaper)

    def setWallpaper(self):
        selectedWallpaper =  self.ui.listWallpaper.currentItem().statusTip()
        config =  KConfig("plasma-appletsrc")
        group = config.group("Containments")
        for each in list(group.groupList()):
            subgroup = group.group(each)
            subcomponent = subgroup.readEntry('plugin')
            if subcomponent == 'desktop' or subcomponent == 'folderview':
                subg = subgroup.group('Wallpaper')
                subg_2 = subg.group('image')
                subg_2.writeEntry("wallpaper", selectedWallpaper)

        self.killPlasma()

    def killPlasma(self):
        p = subprocess.Popen(["pidof", "-s", "plasma"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        pidOfPlasma = int(out)

        try:
            os.kill(pidOfPlasma, 15)
            self.startPlasma()
        except OSError, e:
            print 'WARNING: failed os.kill: %s' % e
            print "Trying SIGKILL"
            os.kill(pidOfPlasma, 9)
            self.startPlasma()

    def startPlasma(self):
        p = subprocess.Popen(["plasma"], stdout=subprocess.PIPE)

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



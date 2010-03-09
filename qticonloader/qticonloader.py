#!/usr/bin/python
# -*- coding: utf-8 -*-

# Qt IconLoader
# Copyright (C) 2010 - Gökmen Göksel
# Based on http://labs.trolltech.com/blogs/2009/02/13/freedesktop-icons-in-qt

from os.path import join
from os.path import exists
from os import getenv

# PyQt4 Core Libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QIconTheme:
    def __init__(self, dirList = [], parents = []):
        self.dirList = dirList
        self.parents = map(lambda x:str(x), list(parents))
        self.valid = False
        if len(dirList) > 0:
            self.valid = True

class QIconLoader:

    SizeSmall       = 16
    SizeSmallMedium = 22
    SizeMedium      = 32
    SizeLarge       = 48
    SizeHuge        = 64
    SizeEnormous    = 128

    def __init__(self, debug = False):

        self.iconSizes = (128, 64, 48, 32, 22, 16)
        self.pixmap = QPixmap()
        self.debug = debug
        self.desktopSession = getenv('DESKTOP_SESSION').replace('default','kde')
        self.userHome = userHome(self.desktopSession, None)

        # Get possible Data Directories
        dataDirs = QFile.decodeName(getenv("XDG_DATA_DIRS"))
        if dataDirs.isEmpty():
            dataDirs = QLatin1String("/usr/local/share/:/usr/share/")

        # for kde session
        if self.desktopSession == 'kde':
            self.desktopVersion = kdeVersion()

            dataDirs += ':' + self.userHome + "/share"
            dataDirs.prepend(QDir.homePath() + "/:")
            kdeDirs = QFile.decodeName(getenv("KDEDIRS")).split(':')
            for dirName in kdeDirs:
                dataDirs.append(':' + dirName + '/share')

            # Find default theme
            for _path in ("/usr/share/icons/default.kde4", 
                    "/usr/kde/3.5/share/icons/default.kde"):
                if exists(_path):
                    fileInfo = QFileInfo(_path)
                    break

            dir = QDir(fileInfo.canonicalFilePath())
            kdeDefault = "crystalsvg"
            if self.desktopVersion >= 4:
                kdeDefault = "oxygen"
            defaultTheme = kdeDefault
            if fileInfo.exists():
                defaultTheme = dir.dirName()

            # Find current theme
            settings = QSettings(join(self.userHome, "share/config/kdeglobals"),
                    QSettings.IniFormat)
            # Fallback to system default
            if self.desktopVersion < 4:
                if not 'Icons' in list(settings.childGroups()):
                    settings = QSettings('/usr/kde/3.5/share/config/kdeglobals',
                            QSettings.IniFormat)
            settings.beginGroup("Icons")
            self.themeName = unicode(
                    settings.value("Theme", defaultTheme).toString())
            # Get default theme
            if self.desktopVersion >= 3:
                if dir.exists():
                    defaultKDETheme = dir.dirName()
                elif self.desktopVersion == 3:
                    defaultKDETheme = "crystalsvg"
                else:
                    defaultKDETheme = "oxygen"

        elif self.desktopSession == 'xfce':
            self.desktopVersion = 'n/a'
            import piksemel
            configFile = join(self.userHome, 
                    'xfconf/xfce-perchannel-xml/xsettings.xml')
            piks = piksemel.parse(configFile).getTag('property')
            for tag in piks.tags():
                if tag.getAttribute('name') == 'IconThemeName':
                    self.themeName = tag.getAttribute('value')

        # Define icon directories
        self.iconDirs =  filter(lambda x: exists(x), 
                map(lambda x: join(unicode(x), 'icons'), dataDirs.split(':')))
        self.iconDirs = list(set(self.iconDirs))

        self.themeIndex = self.readThemeIndex(self.themeName)

    def readThemeIndex(self, themeName):

        dirList = []
        parents = []
        themeIndex = QFile()

        # Read theme index files
        for i in range(len(self.iconDirs)):
            themeIndex.setFileName(join(unicode(self.iconDirs[i]), 
                unicode(themeName), "index.theme"))
            if themeIndex.exists():
                indexReader = QSettings(themeIndex.fileName(), 
                        QSettings.IniFormat)
                for key in indexReader.allKeys():
                    if key.endsWith("/Size"):
                        size = indexReader.value(key).toInt()
                        dirList.append((size[0], 
                            unicode(key.left(key.size() - 5))))
                parents = indexReader.value('Icon Theme/Inherits').toStringList()
                break
        return QIconTheme(dirList, parents)

    def findIconHelper(self, size = int, themeName = str, iconName = str):
        pixmap = QPixmap()

        if iconName == '' or self.themeName == '':
            return pixmap

        if themeName == '':
            themeName = self.themeName

        if themeName == self.themeName:
            index = self.themeIndex
        else:
            index = self.readThemeIndex(themeName)

        subDirs = filter(lambda x:x[0] == size, index.dirList)
        for iconDir in self.iconDirs:
            if exists(join(iconDir, themeName)):
                for theme in subDirs:
                    fileName = join(iconDir, themeName, theme[1],
                            '%s.png' % str(iconName))
                    if self.debug: 
                        print "Looking for : ",fileName
                    if exists(fileName):
                        pixmap.load(fileName)
                        if self.debug: 
                            print 'Icon: %s found in theme %s' % \
                            (iconName, themeName)
                        return pixmap
        if len(self._themes) > 0:
            self._themes.pop(0)
            if not len(self._themes) == 0 and pixmap.isNull():
                pixmap = self.findIconHelper(size, self._themes[0], iconName)
        return pixmap

    def findIcon(self, name = str, size = int):
        pixmapName = ''.join(('$qt', str(name), str(size)))
        self._themes = []
        if (QPixmapCache.find(pixmapName, self.pixmap)):
            return self.pixmap;
        if not self.themeName == '':
            self._themes.append(self.themeName)
            for _name in name:
                self.pixmap = self.findIconHelper(int(size), 
                        self.themeName, _name)
                if not self.pixmap.isNull():
                    break
        if self.pixmap.isNull():
            self._themes.extend(self.themeIndex.parents)
            for _name in name:
                if len(self._themes) > 0:
                    self.pixmap = self.findIconHelper(int(size), 
                            self._themes[0] ,_name)
                    if not self.pixmap.isNull():
                        break
        if not self.pixmap.isNull():
            QPixmapCache.insert(pixmapName, self.pixmap)
        return self.pixmap

    def load(self, name, size = None):
        icon = QIcon()
        size = int(size)
        if not type(name) == list:
            name = [str(name)]
        for _size in self.iconSizes:
            pix = self.findIcon(name, _size)
            if not pix.isNull():
                icon.addPixmap(pix)
                if size == _size:
                    return pix
        if icon.isNull():
            return QPixmap()
        return icon.pixmap(QSize(size, size))

def kdeVersion():
    version = getenv("KDE_SESSION_VERSION")
    if not version:
        version = getenv("KDEDIR").split('/')[-1]
    if '.' in version:
        version = version[0]
    return int(version)

def userHome(de, version):
    if de == 'kde':
        if not version:
            version = kdeVersion()
        homePath = QFile.decodeName(getenv("KDEHOME"))
        if homePath.isEmpty():
            homeDir = QDir(QDir.homePath())
            kdeConfDir = '/.kde'
            if version == 4 and homeDir.exists('.kde4'):
                kdeConfDir = '/.kde4'
            elif version == 3 and homeDir.exists('.kde3.5'):
                kdeConfDir = '/.kde3.5'
            homePath = QDir.homePath() + kdeConfDir
    elif de == 'xfce':
        homePath = QDir.homePath() + '/.config/xfce4'
    return unicode(homePath)


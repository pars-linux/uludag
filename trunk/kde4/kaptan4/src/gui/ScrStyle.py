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
from PyKDE4.kdecore import ki18n, KStandardDirs, KGlobal, KConfig
from PyKDE4 import kdeui

import os, sys, Image, dbus, glob

from gui.ScreenWidget import ScreenWidget
from gui.styleWidget import Ui_styleWidget
from stylewidget import StyleItemWidget

from desktopparser import DesktopParser
from ConfigParser import ConfigParser

class Widget(QtGui.QWidget, ScreenWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # Set title and description for the information widget
    title = ki18n("Some catchy title about styles")
    desc = ki18n("Some catchy description about styles")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_styleWidget()
        self.ui.setupUi(self)

        self.styleDetails = {}

        config = KConfig("kwinrc")
        group = config.group("Desktops")
        defaultDesktopNumber = int(group.readEntry('Number'))

        self.ui.spinBoxDesktopNumbers.setValue(defaultDesktopNumber)
        lst2 = glob.glob1("/usr/kde/4/share/apps/kaptan/gui/styles", "*.style")

        for desktopFiles in lst2:
            parser = DesktopParser()
            parser.read("/usr/kde/4/share/apps/kaptan/gui/styles/" +str(desktopFiles))
            try:
                styleName = parser.get_locale('Style', 'name', '')
                styleDesc = parser.get_locale('Style', 'description', '')
                #styleApplet = parser.get_locale('Style', 'applets', '')
                panelPosition = parser.get_locale('Style', 'panelPosition', '')
                #styleColorScheme = parser.get_locale('Style', 'colorScheme', '')
                widgetStyle = parser.get_locale('Style', 'widgetStyle', '')
                desktopTheme = parser.get_locale('Style', 'desktopTheme', '')
                iconTheme = parser.get_locale('Style', 'iconTheme', '')
                windowDecoration = parser.get_locale('Style', 'windowDecoration', '')
                styleThumb = os.path.join("/usr/kde/4/share/apps/kaptan/gui/styles/",  parser.get_locale('Style', 'thumbnail',''))

                self.styleDetails[styleName] = {
                        "description": styleDesc, 
                        "widgetStyle": widgetStyle, 
                        "desktopTheme": desktopTheme, 
                        "iconTheme": iconTheme, 
                        "windowDecoration": windowDecoration, 
                        "panelPosition": panelPosition
                        }

                item = QtGui.QListWidgetItem(self.ui.listStyles)
                widget = StyleItemWidget(unicode(styleName), unicode(styleDesc), styleThumb, self.ui.listStyles)
                self.ui.listStyles.setItemWidget(item, widget)
                item.setSizeHint(QSize(38,110))
                item.setStatusTip(styleName)
            except:
                print "Warning! Invalid syntax in ", desktopFiles

        self.ui.listStyles.connect(self.ui.listStyles, SIGNAL("itemSelectionChanged()"), self.setStyle)
        self.ui.comboBoxDesktopType.connect(self.ui.comboBoxDesktopType, SIGNAL("activated(const QString &)"), self.setDesktopType)
        self.ui.spinBoxDesktopNumbers.connect(self.ui.spinBoxDesktopNumbers, SIGNAL("valueChanged(const QString &)"), self.addDesktop)

    def addDesktop(self, numberOfDesktop):
        config = KConfig("kwinrc")
        group = config.group("Desktops")
        group.writeEntry('Number', QString(numberOfDesktop))
        group.sync()

        info =  kdeui.NETRootInfo(QtGui.QX11Info.display(), kdeui.NET.NumberOfDesktops | kdeui.NET.DesktopNames)
        info.setNumberOfDesktops(int(numberOfDesktop))
        info.activate()

        session = dbus.SessionBus()
        proxy = session.get_object('org.kde.kwin', '/KWin')
        proxy.reconfigure()

    def setDesktopType(self):
        currentIndex = self.ui.comboBoxDesktopType.currentIndex()
        if currentIndex == 0:
            self.selectedType = 'desktop'
        else:
            self.selectedType = 'folderview'

        config =  KConfig("plasma-appletsrc")
        group = config.group("Containments")

        for each in list(group.groupList()):
            subgroup = group.group(each)
            subcomponent = subgroup.readEntry('plugin')
            subcomponent2 = subgroup.readEntry('screen')
            if subcomponent == 'desktop' or subcomponent == 'folderview':
                if int(subcomponent2) == 1:
                    subgroup.writeEntry('plugin', self.selectedType)

        config.sync()

    def setStyle(self):
        styleName =  str(self.ui.listStyles.currentItem().statusTip())
        self.__class__.screenSettings["summaryMessage"] = styleName  + " : " + self.styleDetails[styleName]["description"]
        self.__class__.screenSettings["hasChanged"] = True

        configKdeGlobals = KConfig("kdeglobals")
        group = configKdeGlobals.group("General")
        group.writeEntry("widgetStyle", self.styleDetails[styleName]["widgetStyle"])

        groupIconTheme = configKdeGlobals.group("Icons")
        groupIconTheme.writeEntry("Theme", self.styleDetails[styleName]["iconTheme"])

        configKdeGlobals.sync()

        # Change Icon theme
        kdeui.KIconTheme.reconfigure()
        kdeui.KIconCache.deleteCache()

        for i in range(kdeui.KIconLoader.LastGroup):
            kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.IconChanged, i)

        # Change widget style
        kdeui.KGlobalSettings.self().emitChange(kdeui.KGlobalSettings.StyleChanged)

        configPlasmaRc = KConfig("plasmarc")
        groupDesktopTheme = configPlasmaRc.group("Theme")
        groupDesktopTheme.writeEntry("name", self.styleDetails[styleName]["desktopTheme"])
        configPlasmaRc.sync()

        configPlasmaApplet = KConfig("plasma-appletsrc")
        group = configPlasmaApplet.group("Containments")
        for each in list(group.groupList()):
            subgroup = group.group(each)
            subcomponent = subgroup.readEntry('plugin')
            if subcomponent == 'panel':
                print subcomponent
                subgroup.writeEntry('location', self.styleDetails[styleName]["panelPosition"])

        configPlasmaApplet.sync()

        configKwinRc = KConfig("kwinrc")
        groupWindowDecoration = configKwinRc.group("Style")
        groupWindowDecoration.writeEntry("PluginLib", self.styleDetails[styleName]["windowDecoration"])
        configKwinRc.sync()

        session = dbus.SessionBus()
        proxy = session.get_object('org.kde.kwin', '/KWin')
        proxy.reconfigure()

    def shown(self):
        pass

    def execute(self):
        return True



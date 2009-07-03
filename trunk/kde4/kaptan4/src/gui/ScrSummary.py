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
from PyKDE4.kdecore import ki18n, KConfig
import subprocess,os, dbus
from gui.ScreenWidget import ScreenWidget
from gui.summaryWidget import Ui_summaryWidget
from PyKDE4 import kdeui
# import other widgets to get the latest configuration
import gui.ScrWallpaper as wallpaperWidget
import gui.ScrMouse as mouseWidget
import gui.ScrWallpaper  as wallpaperWidget
import gui.ScrStyle  as styleWidget
import gui.ScrMenu  as menuWidget
import gui.ScrSearch  as searchWidget
import gui.ScrSmolt  as smoltWidget

# Smolt related headers
import sys
sys.path.append('/usr/share/smolt/client')
import smolt
from urlparse import urljoin

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Welcome")
    desc = ki18n("Welcome to Kaptan Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_summaryWidget()
        self.ui.setupUi(self)

    def shown(self):
        self.wallpaperSettings = wallpaperWidget.Widget.screenSettings
        self.mouseSettings = mouseWidget.Widget.screenSettings
        self.menuSettings = menuWidget.Widget.screenSettings
        self.searchSettings = searchWidget.Widget.screenSettings
        self.styleSettings = styleWidget.Widget.screenSettings
        self.smoltSettings = smoltWidget.Widget.screenSettings

        subject = "<p><li><b>%s</b></li><ul>"
        item    = "<li>%s</li>"
        end     = "</ul></p>"
        content = QString("")

        content.append("""<html><body><ul>""")

        # Mouse Settings
        content.append(subject % ki18n("Mouse Settings").toString())

        content.append(item % ki18n("Selected Mouse configuration: <b>%s</b>").toString() % self.mouseSettings["summaryMessage"]["selectedMouse"].toString())
        content.append(item % ki18n("Selected clicking behaviour: <b>%s</b>").toString() % self.mouseSettings["summaryMessage"]["clickBehaviour"].toString())
        content.append(end)

        # Menu Settings
        content.append(subject % ki18n("Menu Settings").toString())
        content.append(item % ("Selected Menu: <b>%s</b>") % self.menuSettings["summaryMessage"].toString())
        content.append(end)

        # Wallpaper Settings
        content.append(subject % ki18n("Wallpaper Settings").toString())
        if self.wallpaperSettings["hasChanged"] == False:
            content.append(item % ki18n("You haven't selected any wallpaper.").toString())
        else:
            content.append(item % ki18n("Selected Wallpaper: <b>%s</b>").toString() % os.path.basename(str(self.wallpaperSettings["selectedWallpaper"])))
        content.append(end)

        # Style Settings
        content.append(subject % ki18n("Style Settings").toString())

        if self.styleSettings["hasChanged"] == False:
            content.append(item % ki18n("You haven't selected any style.").toString())
        else:
            content.append(item % ki18n("Selected Style: <b>%s</b>").toString() % self.styleSettings["summaryMessage"])

        content.append(end)


        # Search Settings
        content.append(subject %ki18n("Search Settings").toString())
        content.append(item % ki18n("Desktop search: <b>%s</b>").toString() % self.searchSettings["summaryMessage"].toString())
        content.append(end)

        # Smolt Settings
        """
        content.append(subject %ki18n("Smolt Settings").toString())
        content.append(item % ki18n("Send my profile: <b>%s</b>").toString() % QVariant(self.smoltSettings["profileSend"]).toString())
        content.append(ki18n("(<i><u>Warning:</u> Sending profile requires to set up communication with Smolt server and can take between 30 seconds to a minute. Kaptan may freeze during this time.</i>)").toString())
        content.append(end)
        """
        content.append("""</ul></body></html>""")
        self.ui.textSummary.setHtml(content)

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

    def execute(self):
        hasChanged = False

        # Wallpaper Settings
        if self.wallpaperSettings["hasChanged"] == True:
            hasChanged = True
            if self.wallpaperSettings["selectedWallpaper"]:
                config =  KConfig("plasma-appletsrc")
                group = config.group("Containments")
                for each in list(group.groupList()):
                    subgroup = group.group(each)
                    subcomponent = subgroup.readEntry('plugin')
                    if subcomponent == 'desktop' or subcomponent == 'folderview':
                        subg = subgroup.group('Wallpaper')
                        subg_2 = subg.group('image')
                        subg_2.writeEntry("wallpaper", self.wallpaperSettings["selectedWallpaper"])

        # Search Settings
        if self.searchSettings["hasChanged"] == True:
            config = KConfig("nepomukserverrc")
            group = config.group("Basic Settings")

            session = dbus.SessionBus()
            proxy = session.get_object( "org.kde.NepomukServer", "/nepomukserver")

            group.writeEntry('Start Nepomuk', str(self.searchSettings["state"]).lower())
            proxy.reconfigure()
            proxy.enableNepomuk(self.searchSettings["state"])

        # Menu Settings
        if self.menuSettings["hasChanged"] == True:
            hasChanged = True
            config = KConfig("plasma-appletsrc")
            group = config.group("Containments")

            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                if subcomponent == 'panel':
                    subg = subgroup.group('Applets')
                    for i in list(subg.groupList()):
                        subg2 = subg.group(i)
                        launcher = subg2.readEntry('plugin')
                        if str(launcher).find('launcher') >= 0:
                            subg2.writeEntry('plugin', self.menuSettings["selectedMenu"] )
        # Desktop Type
        if self.styleSettings["hasChangedDesktopType"] == True:
            hasChanged = True
            config =  KConfig("plasma-appletsrc")
            group = config.group("Containments")

            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                subcomponent2 = subgroup.readEntry('screen')
                if subcomponent == 'desktop' or subcomponent == 'folderview':
                    if int(subcomponent2) == 1:
                        subgroup.writeEntry('plugin', self.styleSettings["desktopType"])

            config.sync()

        # Number of Desktops
        if self.styleSettings["hasChangedDesktopNumber"] == True:
            hasChanged = True
            config = KConfig("kwinrc")
            group = config.group("Desktops")
            group.writeEntry('Number', self.styleSettings["desktopNumber"])
            group.sync()

            info =  kdeui.NETRootInfo(QtGui.QX11Info.display(), kdeui.NET.NumberOfDesktops | kdeui.NET.DesktopNames)
            info.setNumberOfDesktops(int(self.styleSettings["desktopNumber"]))
            info.activate()

            session = dbus.SessionBus()
            proxy = session.get_object('org.kde.kwin', '/KWin')
            proxy.reconfigure()
            config.sync()

        # Theme Settings
        if self.styleSettings["hasChanged"] == True:
            hasChanged = True
            configKdeGlobals = KConfig("kdeglobals")
            group = configKdeGlobals.group("General")
            group.writeEntry("widgetStyle", self.styleSettings["styleDetails"][self.styleSettings["styleName"]]["widgetStyle"])

            groupIconTheme = configKdeGlobals.group("Icons")
            groupIconTheme.writeEntry("Theme", self.styleSettings["styleDetails"][self.styleSettings["styleName"]]["iconTheme"])

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
            groupDesktopTheme.writeEntry("name", self.styleSettings["styleDetails"][self.styleSettings["styleName"]]["desktopTheme"])
            configPlasmaRc.sync()

            configPlasmaApplet = KConfig("plasma-appletsrc")
            group = configPlasmaApplet.group("Containments")
            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                if subcomponent == 'panel':
                    print subcomponent
                    subgroup.writeEntry('location', self.styleSettings["styleDetails"][self.styleSettings["styleName"]]["panelPosition"])

            configPlasmaApplet.sync()

            configKwinRc = KConfig("kwinrc")
            groupWindowDecoration = configKwinRc.group("Style")
            groupWindowDecoration.writeEntry("PluginLib", self.styleSettings["styleDetails"][self.styleSettings["styleName"]]["windowDecoration"])
            configKwinRc.sync()

            session = dbus.SessionBus()
            proxy = session.get_object('org.kde.kwin', '/KWin')
            proxy.reconfigure()

        # Smolt Settings
        if self.smoltSettings["profileSend"] == True:
            profile = smolt.Hardware()
            retvalue, pub_uuid, admin = profile.send(smoonURL=smolt.smoonURL)
            url = urljoin(smolt.smoonURL, '/show?uuid=%s' % pub_uuid)
            values = { "pub_uuid" : pub_uuid,
                       "admin" : admin,
                       "url" : url }

        if hasChanged == True:
            self.killPlasma()

        return True




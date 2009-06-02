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
import subprocess,os
from gui.ScreenWidget import ScreenWidget
from gui.summaryWidget import Ui_summaryWidget

# import other widgets to get the latest configuration
import gui.ScrWallpaper as wallpaperWidget
import gui.ScrMouse as mouseWidget
import gui.ScrWallpaper  as wallpaperWidget
import gui.ScrStyle  as styleWidget
import gui.ScrMenu  as menuWidget
import gui.ScrSearch  as searchWidget

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Welcome")
    desc = ki18n("Welcome to Kaptan Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_summaryWidget()
        self.ui.setupUi(self)

    def shown(self):
        selectedWallpaper = wallpaperWidget.Widget.selectedWallpaper
        selectedMouse = mouseWidget.Widget.selectedMouse
        selectedBehaviour = mouseWidget.Widget.selectedBehaviour
        self.menuSettings = menuWidget.Widget.screenSettings
        self.searchSettings = searchWidget.Widget.screenSettings
        selectedStyle = styleWidget.Widget.selectedStyle

        subject = "<p><li><b>%s</b></li><ul>"
        item    = "<li>%s</li>"
        end     = "</ul></p>"
        content = QString("")

        content.append("""<html><body><ul>""")

        # Mouse Settings
        content.append(subject % ("Mouse Settings"))
        content.append(item % ("Selected Mouse configuration is <b>%s</b>") % selectedMouse)
        content.append(item % ("Selected clicking behaviour is <b>%s</b>") % selectedBehaviour)
        content.append(end)

        # Menu Settings
        content.append(subject % ("Menu Settings"))
        content.append(item % ("Selected Menu is <b>%s</b>") % self.menuSettings["summaryMessage"].toString())
        content.append(end)

        # Wallpaper Settings
        content.append(subject % ("Wallpaper Settings"))
        content.append(item % ("Selected Wallpaper is <b>%s</b>") % selectedWallpaper)
        content.append(end)

        # Style Settings
        content.append(subject % ("Style Settings"))
        content.append(item % ("Selected Style is <b>%s</b>") % selectedStyle)
        content.append(end)


        # Search Settings
        content.append(subject %("Search Settings"))
        content.append(item % ("Desktop search is <b>%s</b>") % self.searchSettings["summaryMessage"].toString())
        content.append(end)

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

        # Search settings
        if self.searchSettings["hasChanged"] == True:
            config = KConfig("nepomukserverrc")
            group = config.group("Basic Settings")

            session = dbus.SessionBus()
            proxy = session.get_object( "org.kde.NepomukServer", "/nepomukserver")

            group.writeEntry('Start Nepomuk', str(self.searchSettings["state"]).lower())
            proxy.reconfigure()
            proxy.enableNepomuk(state)

        if self.menuSettings["hasChanged"] == True:
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



        self.killPlasma()
        return True




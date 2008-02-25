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
import qtxml
from kdecore import *
from kdeui import *
import kdedesigner
import dcop
import kdecore

from screens.Screen import ScreenWidget
from screens.paneldlg import PanelWidget

summary = {"sum":""}
summary["pic"] = "kaptan/pics/mouse_rh.png"
summary["desc"] = "Panel"

class Widget(PanelWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = "Configure your panel !"
    desc = "Select the one you like..."

    selectedStyle= QString()

    def __init__(self, *args):
        apply(PanelWidget.__init__, (self,) + args)
        
        # Common Pardus settings for all themes
        config = KConfig("kdeglobals")
        config.setGroup("KDE")
        config.writeEntry("ShowIconsOnPushButtons", True)
        config.writeEntry("EffectAnimateCombo", True)
        config.sync()

        #add kaptan themes into resource pool
        KGlobal.dirs().addResourceType("themes", KStandardDirs.kde_default("data") + "kaptan/themes/")

        themes = QStringList(KGlobal.dirs().findAllResources("themes", "*.xml", True))
        themes.sort()

        for thumbnail in themes:
            self.styleBox.insertItem(QFileInfo(thumbnail).baseName())

        self.connect(self.styleBox, SIGNAL("activated(int)"), self.styleSelected)
        self.connect(self.checkKickoff, SIGNAL("clicked()"), self.kickoffSelected)
        self.connect(self.styleButton, SIGNAL("clicked()"), self.applyStyle)

        #if no panel chosen, then write defaults
        summary["sum"] = self.styleBox.currentText()

        self.styleBox.setCurrentItem(0)
        self.styleSelected(0)


    def applyStyle(self):
        
        #normally this assignment should be in execute(), but for 
        #controlling panel values after applying it's in here.
        summary["sum"] = self.styleBox.currentText()

        #read entire xml into DOM tree
        dom = qtxml.QDomDocument()
        file = QFile(self.selectedStyle)
        file.open(IO_ReadOnly)
        dom.setContent(file.readAll())
        file.close()

        #attach to dcop
        client = kdecore.KApplication.dcopClient()
        if not client.isAttached():
            client.attach()

        #kicker settings
        kickerConf = KConfig("kickerrc")
        kickerConf.setGroup("General")

        Kicker = qtxml.QDomElement
        Kicker = dom.elementsByTagName("kicker").item(0).toElement()

        kickerConf.writeEntry("LegacyKMenu",not self.checkKickoff.isChecked())
        kickerConf.writeEntry("Transparent", self.getProperty(Kicker, "Transparent", "value"))
        kickerConf.writeEntry("SizePercentage", self.getProperty(Kicker, "SizePercentage", "value"))
        kickerConf.writeEntry("CustomSize", self.getProperty(Kicker, "CustomSize", "value"))
        kickerConf.writeEntry("Position", self.getProperty(Kicker, "Position", "value"))
        kickerConf.writeEntry("Alignment", self.getProperty(Kicker, "Alignment", "value"))
        kickerConf.sync()

        #restart kicker
        client.send("kicker", "kicker", "restart()", "")

        #kwin settings
        kwinConf = KConfig("kwinrc")
        kwinConf.setGroup("Style")

        KWin =  qtxml.QDomElement
        KWin = dom.elementsByTagName("kwin").item(0).toElement()

        kwinConf.writeEntry("PluginLib", self.getProperty(KWin, "PluginLib", "value"))
        kwinConf.sync()

        #restart kwin
        client.send("kwin", "KWinInterface", "reconfigure()", "")
        
        #widget settings
        globalConf = KConfig("kdeglobals")
        globalConf.setGroup("General")

        Widget = qtxml.QDomElement
        Widget = dom.elementsByTagName("widget").item(0).toElement()

        globalConf.writeEntry("widgetStyle", self.getProperty(Widget, "widgetStyle", "value"))
        globalConf.sync()
    
        KIPC.sendMessageAll(KIPC.StyleChanged)
        

    def getProperty(self, parent,tag, attr):
        
        pList = qtxml.QDomNodeList
        pList = parent.elementsByTagName(tag)
        
        if  pList.count():
            return  pList.item(0).toElement().attribute(attr)
        else:
            return

    
    def kickoffSelected(self):
        
        self.styleSelected(self.styleBox.currentItem())

    def styleSelected(self, item):

        name = QString(self.styleBox.text(item))
        previewPath = QString

        if self.checkKickoff.isChecked():
            previewPath = KGlobal.dirs().findResourceDir("themes", "/" ) + name + "/" + name + "_kickoff.preview.png"
        else:
            previewPath = KGlobal.dirs().findResourceDir("themes", "/" ) + name + "/" + name + ".preview.png"

        xmlFile = QString
        xmlFile = KGlobal.dirs().findResourceDir("themes", "/" ) + name + "/" + name + ".xml"

        if QFile.exists(previewPath):
            self.pix_style.setPixmap(QPixmap(previewPath))
            self.selectedStyle = xmlFile
        else:
            return

    def shown(self):
        pass

    def execute(self):
        if self.checkKickoff.isChecked():
            summary["sum"] += ", Kickoff Menu"


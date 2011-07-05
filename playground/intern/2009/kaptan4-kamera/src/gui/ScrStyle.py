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
    screenSettings["hasChangedDesktopType"] = False
    screenSettings["hasChangedDesktopNumber"] = False

    # Set title and description for the information widget
    title = ki18n("Some catchy title about styles")
    desc = ki18n("Some catchy description about styles")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_styleWidget()
        self.ui.setupUi(self)

        self.styleDetails = {}
        self.catLang = KGlobal.locale().language()

        config = KConfig("kwinrc")
        group = config.group("Desktops")
        defaultDesktopNumber = int(group.readEntry('Number'))

        self.ui.spinBoxDesktopNumbers.setValue(defaultDesktopNumber)
        lst2 = glob.glob1("/usr/kde/4/share/apps/kaptan/gui/styles", "*.style")

        for desktopFiles in lst2:
            parser = DesktopParser()
            parser.read("/usr/kde/4/share/apps/kaptan/gui/styles/" +str(desktopFiles))
            try:
                styleName = unicode(parser.get_locale('Style', 'name[%s]'%self.catLang, ''))
            except:
                styleName = unicode(parser.get_locale('Style', 'name', ''))
            try:
                styleDesc = unicode(parser.get_locale('Style', 'description[%s]'%self.catLang, ''))
            except:
                styleDesc = unicode(parser.get_locale('Style', 'description', ''))
            try:
                # TODO find a fallback values for these & handle exceptions seperately.
                #styleApplet = parser.get_locale('Style', 'applets', '')
                panelPosition = parser.get_locale('Style', 'panelPosition', '')
                #styleColorScheme = parser.get_locale('Style', 'colorScheme', '')
                widgetStyle = unicode(parser.get_locale('Style', 'widgetStyle', ''))
                desktopTheme = unicode(parser.get_locale('Style', 'desktopTheme', ''))
                colorScheme = unicode(parser.get_locale('Style', 'colorScheme', ''))
                iconTheme = unicode(parser.get_locale('Style', 'iconTheme', ''))
                windowDecoration = unicode(parser.get_locale('Style', 'windowDecoration', ''))
                styleThumb = unicode(os.path.join("/usr/kde/4/share/apps/kaptan/gui/styles/",  parser.get_locale('Style', 'thumbnail','')))

                colorDict = {}
                colorDir = "/usr/kde/4/share/apps/color-schemes/"
                self.Config = ConfigParser()
                self.Config.optionxform = str
                color = colorDir + colorScheme + ".colors"
                if not os.path.exists(color):
                    color = colorDir + "Oxygen.colors"

                self.Config.read(color)
                #colorConfig= KConfig("kdeglobals")
                for i in self.Config.sections():
                    #colorGroup = colorConfig.group(str(i))
                    colorDict[i] = {}
                    for key, value in self.ConfigSectionMap(i).items():
                        colorDict[i][key] = value
                        #colorGroup.writeEntry(str(key), str(value))

                self.styleDetails[styleName] = {
                        "description": styleDesc, 
                        "widgetStyle": widgetStyle, 
                        "colorScheme": colorDict, 
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
        #self.ui.previewButton.connect(self.ui.previewButton, SIGNAL("clicked()"), self.previewStyle)

    def ConfigSectionMap(self,section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def addDesktop(self, numberOfDesktop):
        self.__class__.screenSettings["hasChangedDesktopNumber"] = True
        self.__class__.screenSettings["desktopNumber"] = str(numberOfDesktop)

    def setDesktopType(self):
        currentIndex = self.ui.comboBoxDesktopType.currentIndex()
        if currentIndex == 0:
            self.selectedType = 'desktop'
        else:
            self.selectedType = 'folderview'

        self.__class__.screenSettings["hasChangedDesktopType"] = True
        self.__class__.screenSettings["desktopType"] = self.selectedType

    def setStyle(self):
        styleName =  str(self.ui.listStyles.currentItem().statusTip())
        self.__class__.screenSettings["summaryMessage"] = unicode(styleName)
        self.__class__.screenSettings["hasChanged"] = True

        self.__class__.screenSettings["styleDetails"] = self.styleDetails
        self.__class__.screenSettings["styleName"] = styleName

    def shown(self):
        pass

    def execute(self):
        return True



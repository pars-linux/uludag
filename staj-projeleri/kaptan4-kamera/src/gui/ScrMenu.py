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

from gui.ScreenWidget import ScreenWidget
from gui.menuWidget import Ui_menuWidget


class Widget(QtGui.QWidget, ScreenWidget):
    screenSettings = {}
    screenSettings["hasChanged"] = False

    # Set title and description for the information widget
    title = ki18n("Some catchy title about styles")
    desc = ki18n("Some catchy description about styles")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_menuWidget()
        self.ui.setupUi(self)

        # read default menu style first
        config = KConfig("plasma-appletsrc")
        group = config.group("Containments")

        self.menuNames = {}
        self.menuNames["launcher"] = {
                "menuIndex": 0,
                "summaryMessage": ki18n("Kick-off Menu"),
                "image": QtGui.QPixmap(':/raw/pics/kickoff.png'),
                "description": ki18n("Default menu of Pardus GNU/Linux.")
                }
        self.menuNames["simplelauncher"] = {
                "menuIndex": 1,
                "summaryMessage": ki18n("Simple Menu"),
                "image": QtGui.QPixmap(':/raw/pics/simple.png'),
                "description": ki18n("An old style menu from KDE 3.")
                }
        self.menuNames["lancelot_launcher"] = {
                "menuIndex": 2,
                "summaryMessage": ki18n("Lancelot Menu"),
                "image": QtGui.QPixmap(':/raw/pics/lancelot.png'),
                "description": ki18n("An advanced menu for KDE4.")
                }

        for each in list(group.groupList()):
            subgroup = group.group(each)
            subcomponent = subgroup.readEntry('plugin')
            if subcomponent == 'panel':
                subg = subgroup.group('Applets')
                for i in list(subg.groupList()):
                    subg2 = subg.group(i)
                    launcher = subg2.readEntry('plugin')
                    if str(launcher).find('launcher') >= 0:
                        self.__class__.screenSettings["selectedMenu"] =  subg2.readEntry('plugin')

        # set menu preview to default menu
        self.ui.pictureMenuStyles.setPixmap(self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]["image"])
        self.ui.labelMenuDescription.setText(self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]["description"].toString())
        self.ui.menuStyles.setCurrentIndex(self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]["menuIndex"])

        self.ui.menuStyles.connect(self.ui.menuStyles, SIGNAL("activated(const QString &)"), self.setMenuStyle)

    def setMenuStyle(self, enee):
        self.__class__.screenSettings["hasChanged"] = True
        currentIndex = self.ui.menuStyles.currentIndex()

        if currentIndex == 0:
            self.__class__.screenSettings["selectedMenu"] = 'launcher'

            self.ui.pictureMenuStyles.setPixmap(self.menuNames["launcher"]["image"])
            self.ui.labelMenuDescription.setText(self.menuNames["launcher"]["description"].toString())
        elif currentIndex == 1:
            self.__class__.screenSettings["selectedMenu"] = 'simplelauncher'

            self.ui.pictureMenuStyles.setPixmap(self.menuNames["simplelauncher"]["image"])
            self.ui.labelMenuDescription.setText(self.menuNames["simplelauncher"]["description"].toString())

        else:
            self.__class__.screenSettings["selectedMenu"] = 'lancelot_launcher'

            self.ui.pictureMenuStyles.setPixmap(self.menuNames["lancelot_launcher"]["image"])
            self.ui.labelMenuDescription.setText(self.menuNames["lancelot_launcher"]["description"].toString())

    def shown(self):
        pass

    def execute(self):
        self.__class__.screenSettings["summaryMessage"] = self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]["summaryMessage"]
        return True



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
        self.menuNames["launcher"] = ki18n("Kick-off Menu")
        self.menuNames["lancelot_launcher"] = ki18n("Lancelot Menu")
        self.menuNames["simplelauncher"] = ki18n("Simple Menu")

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

        # menu descriptions and preview pics
        self.kickoffPic = QtGui.QPixmap(':/raw/pics/kickoff.png')
        self.kickoffDesc = "A modern menu for KDE."

        self.simplePic = QtGui.QPixmap(':/raw/pics/simple.png')
        self.simpleDesc = "And old style menu from KDE 3."

        self.lancelotPic = QtGui.QPixmap(':/raw/pics/lancelot.png')
        self.lancelotDesc = "An experimental menu for KDE4"

        # set menu preview to default menu: kick-off
        self.ui.pictureMenuStyles.setPixmap(self.kickoffPic)
        self.ui.labelMenuDescription.setText(self.kickoffDesc)

        self.ui.menuStyles.connect(self.ui.menuStyles, SIGNAL("activated(const QString &)"), self.setMenuStyle)

    def setMenuStyle(self, enee):
        self.__class__.screenSettings["hasChanged"] = True
        currentIndex = self.ui.menuStyles.currentIndex()

        if currentIndex == 0:
            self.__class__.screenSettings["selectedMenu"] = 'launcher'

            self.ui.pictureMenuStyles.setPixmap(self.kickoffPic)
            self.ui.labelMenuDescription.setText(self.kickoffDesc)
        elif currentIndex == 1:
            self.__class__.screenSettings["selectedMenu"] = 'simplelauncher'

            self.ui.pictureMenuStyles.setPixmap(self.simplePic)
            self.ui.labelMenuDescription.setText(self.simpleDesc)

        else:
            self.__class__.screenSettings["selectedMenu"] = 'lancelot_launcher'

            self.ui.pictureMenuStyles.setPixmap(self.lancelotPic)
            self.ui.labelMenuDescription.setText(self.lancelotDesc)

    def shown(self):
        pass

    def execute(self):
        self.__class__.screenSettings["summaryMessage"] = self.menuNames[str(self.__class__.screenSettings["selectedMenu"])]
        return True



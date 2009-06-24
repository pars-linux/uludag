#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys
from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyKDE4.kdecore import ki18n, KAboutData, KConfig, KCmdLineArgs


from migration.about import aboutData

#Screens
import migration.gui.ScrWelcome as welcome



def getKernelOpt(cmdopt=None):
    if cmdopt:
        for cmd in "".join(loadFile("/proc/cmdline")).split():
            if cmd.startswith("%s=" % cmdopt):
                return cmd[len(cmdopt)+1:].split(",")
    else:
        return "".join(loadFile("/proc/cmdline")).split()

    return ""


def isLiveCD():
    opts = getKernelOpt("mudur")

    if opts and "livecd" in opts:
        return True

    return False

if isLiveCD():
    availableScreens = [welcomeWidget]
else:
    availableScreens = [welcomeWidget]
    
class Migration(QtGui.QWidget):
    def __init__(self, parent=None):
        pass
    
    def enableNext(self):
        pass
    def disableNext(self):
        pass
    def enableBack(self):
        pass
    def disableBack(self):
        pass
 
 
if __name__ =="__main__":
    
    KCmdLineArgs.init(sys.argv, aboutData)
    application = kdeui.KApplication()
    migration = Migration()
    migration.show()
    
    geometry  = QtGui.QDesktopWidget().screenGeometry()
    migration.move(geometry.width()/2 - migration.width()/2, geometry.height()/2 - migration.height()/2) 
    application.exec_()
    
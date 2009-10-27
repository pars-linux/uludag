#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from kdecore import KApplication, KAboutData, KCmdLineArgs, KGlobal, KIcon
from qt import QObject, SIGNAL, SLOT

from pakito.gui.mainwindow import MainWindow

def I18N_NOOP(x):
    return x

name = "Pakito"
version = "0.3"
mail = "gokcen.eraslan@gmail.com"
description = I18N_NOOP("A tool for accelerating package making process")

if __name__ == "__main__":    
    about = KAboutData(name.lower(), name, version, description, KAboutData.License_GPL_V2, "(C) Gökçen Eraslan 2007", None, None, mail)
    about.addAuthor("Gökçen Eraslan", None, mail)
    KCmdLineArgs.init(sys.argv, about)
    app = KApplication()
    programLogo = KGlobal.iconLoader().loadIcon("pisikga", KIcon.Desktop)
    about.setProgramLogo(programLogo.convertToImage())
    QObject.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    pac = MainWindow(None, name)
    app.setMainWidget(pac)
    pac.show()
    app.exec_loop()

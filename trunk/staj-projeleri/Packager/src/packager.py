#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from gui.mainwindow import *
from kdecore import KApplication, KAboutData, KCmdLineArgs

if __name__ == "__main__":    
    about = KAboutData("packager", "Packager", "0.0.1", "A tool for accelerating package making process", KAboutData.License_GPL_V2, "(C) Gökçen Eraslan 2007", None, None, "gokcen.eraslan@gmail.com")
    about.addAuthor("Gökçen Eraslan", None, "gokcen.eraslan@gmail.com")
    KCmdLineArgs.init(sys.argv, about)
    app = KApplication()
    programLogo = KGlobal.iconLoader().loadIcon("pisikga", KIcon.Desktop)
    about.setProgramLogo(programLogo.convertToImage())
#    QObject.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    pac = MainWindow(None, "Packager v0.0.1")
    app.setMainWidget(pac)
    pac.show()
    app.exec_loop()
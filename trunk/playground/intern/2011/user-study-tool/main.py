#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import SIGNAL

if __name__ == '__main__':
    from PyKDE4.kdeui import *
    from PyKDE4.kdecore import *

    from myStandalone import SurveyManager
    PACKAGE     = "Pardus Kullanım Araştırmaları"
    appName     = "user-study"
    modName     = "userstudy"
    version     = "1.0.0"
    homePage    = "http://developer.pardus.org.tr/projects/"
    bugEmail    = "bugs@pardus.org.tr"
    icon        = ("", "")
    catalog     = appName
    programName = ki18n(PACKAGE)
    description = ki18n(PACKAGE)
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009-2010 TUBITAK/UEKAE")
    text        = ki18n(None)
    aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

    # Authors
    aboutData.addAuthor(ki18n("Gökmen Göksel"), ki18n("Current Maintainer"))
    aboutData.setTranslator(ki18nc("NAME OF TRANSLATORS", "Your names"), ki18nc("EMAIL OF TRANSLATORS", "Your emails"))

    # Set Command-line arguments
    KCmdLineArgs.init(sys.argv, aboutData)

    # Create a Kapplitcation instance
    app = KApplication()

    # Create Main Widget
    mainWindow = SurveyManager(None, appName)
    mainWindow.show()

    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the applications
    app.exec_()

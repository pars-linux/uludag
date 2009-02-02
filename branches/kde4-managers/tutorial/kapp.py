#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication, KMainWindow

from PyQt4.QtGui import QLabel, QWidget

# A simple KMainWindow implementation
class MainWindow(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)

        self.resize(640, 480)
        label = QLabel("This is a simple PyKDE4 program", self)
        label.setGeometry(10, 10, 200, 20)

    def test(self):
        print "Test method called.."

if __name__ == '__main__':

    # About data definitions
    appName     = "KApplication"
    catalog     = ""
    programName = ki18n("KApplication")
    version     = "1.0"
    description = ki18n("KApplication example")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009 Panthera Pardus")
    text        = ki18n("none")
    homePage    = "www.pardus.org.tr"
    bugEmail    = "info@pardus.org.tr"

    # Create about data from defined variables
    aboutData   = KAboutData(appName, catalog, programName, version, description,
                                license, copyright, text, homePage, bugEmail)

    # Initialize Command Line arguments
    KCmdLineArgs.init(sys.argv, aboutData)

    # Create the application
    app = KApplication()

    # Create Main Window
    mainWindow = MainWindow()
    mainWindow.show()

    # Set top Widget as our mainWindow
    app.setTopWidget(mainWindow)

    # Run the app
    app.exec_()


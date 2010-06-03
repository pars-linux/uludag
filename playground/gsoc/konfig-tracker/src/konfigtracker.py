#!/usr/bin/env python

# System
import sys

# Application stuffs
from PyQt4.QtCore import SIGNAL

#PyKDE4 stuffs
from PyKDE4.kdeui import KUniqueApplication
from PyKDE4.kdecore import KCmdLineArgs

if __name__ == "__main__":
    
    from konfigtracker.about import aboutData
    from konfigtracker.konfigtrackermain import KonfigTracker
    
    # set commandline arguments
    KCmdLineArgs.init(sys.argv,aboutData)
    
    #creating a kapplication instance
    app = KUniqueApplication()
    MainWindow = KonfigTracker(app)
    MainWindow.show()
    
    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)
    
    # Run the application
    app.exec_()
    
    

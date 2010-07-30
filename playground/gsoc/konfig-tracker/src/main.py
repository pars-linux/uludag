#!/usr/bin/env python
# -*- coding: utf-8 -*-

# System
import sys
import dbus

# Application stuffs
from PyQt4.QtCore import SIGNAL

#PyKDE4 stuffs
from PyKDE4.kdeui import KUniqueApplication
from PyKDE4.kdecore import KCmdLineArgs

if __name__ == "__main__":
    
    from konfigtracker.about import aboutData
    from konfigtracker.konfigtrackermain import KonfigTracker
    
    # Create a dbus mainloop if its not exists
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    # set commandline arguments
    KCmdLineArgs.init(sys.argv,aboutData)
    
    #creating a kapplication instance
    app = KUniqueApplication(True, True)
    MainWindow = KonfigTracker(app)
    MainWindow.show()
    #app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)
    
    # Run the application
    app.exec_()  

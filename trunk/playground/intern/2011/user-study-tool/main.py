#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import *

import pds

Pds = pds.Pds('user-study-tool', debug = False)
	#il8n = Pds.il8n
if __name__ == '__main__':
 
    PACKAGE     = "Pardus Kullanım Araştırmaları"
    appName     = "user-study"
    modName     = "userstudy"
    version     = "1.0.0"
    catalog     = appName

    

    #if Pds.session == pds.Kde4:
      
	#from PyKDE4.kdeui import *
        #from PyKDE4.kdecore import *
   
	#programName = ki18n(PACKAGE)
	#description = ki18n(PACKAGE)
	#license     = KAboutData.License_GPL
	#copyright   = ki18n("(c) 2009-2010 TUBITAK/UEKAE")
	#text        = ki18n(None)
	#aboutData   = KAboutD   else:ata(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

	#Authors
	#aboutData.addAuthor(ki18n("Bertan Gündoğdu"), ki18n("Current Maintainer"))
	#aboutData.setTranslator(ki18nc("NAME OF TRANSLATORS", "Your names"), ki18nc("EMAIL OF TRANSLATORS", "Your emails"))
	#from myStandalone import SurveyManager
	#Set Command-line arguments
	#KCmdLineArgs.init(sys.argv, aboutData)

	#Create a Kapplitcation instance
	#app = KApplication()

	#Create Main Widget
	#mainWindow = SurveyManager(None, appName)
	#mainWindow.show()
	
	
	
   
    #else:
    from mainWin import MainManager

    #Pds Stuff
    from pds.quniqueapp import QUniqueApplication
    
    app = QUniqueApplication(sys.argv, catalog = appName)
    
    #Create Main Widget and make some settings
    mainWindow = MainManager(None)
    mainWindow.show()
    mainWindow.resize(640, 480)
    mainWindow.setWindowTitle(PACKAGE)
    
  

    app.connect(app, SIGNAL('lastWindowClosed()'), app.quit)

    # Run the applications
    app.exec_()

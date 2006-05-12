#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from qt import *

from kdeui import *
from kdecore import *
from khtml import *

def I18N_NOOP(str):
    return str

class MainWidget(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)

        self.vbox = QVBox(self)
        self.hbox = QHBox(self.vbox)
        self.hbox.setSpacing(1)
        self.label = QLabel(i18n("Address:"),self.hbox)
        self.label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
        self.lastURL = "http://www.pardus.org.tr"

        # Comboboxen
        self.combobox = KComboBox(True,self.hbox)
        self.completion = self.combobox.completionObject()
        self.connect(self.combobox,SIGNAL("returnPressed(const QString&)"),self.newURL)

        # Progress bar
        self.progress = QProgressBar(self.statusBar())
        self.progress.setTotalSteps(100)
        self.statusBar().addWidget(self.progress,0,True)

        self.progress.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
                
        self.htmlPart = KHTMLPart(self.vbox)
        self.layout = QGridLayout()
        
        self.setCentralWidget(self.vbox)

        self.reloadAction = KAction(i18n("Reload"),"reload",KShortcut.null(),self.reload,self.actionCollection(),"reload_action")
        self.stopAction = KAction(i18n("Stop"),"stop",KShortcut.null(),self.empty,self.actionCollection(),"stop_action")
        self.stopAction.setEnabled(False)
                                        

        self.setupGUI(KMainWindow.ToolBar|KMainWindow.Keys|KMainWindow.StatusBar|KMainWindow.Save|KMainWindow.Create)
        self.toolBar().setIconText(KToolBar.IconTextRight)

        self.layout.addWidget(self.hbox,1,1)
        
        self.htmlPart.openURL(KURL(self.lastURL))

        self.connect(self.htmlPart.browserExtension(),SIGNAL("openURLRequest(const KURL&, const KParts::URLArgs&)"),self.openURLRequest)
        self.connect(self.htmlPart.browserExtension(),SIGNAL("loadingProgress(int)"),self.updateLoadingProgress)
        self.connect(self.htmlPart,SIGNAL("completed()"),self.finishedRendering)

    def finishedRendering(self):
        print 'Finished rendering!'
        self.progress.setProgress(0)
        self.progress.hide()
        
    def updateLoadingProgress(self,percent):
        self.progress.setProgress(percent)
                
    def newURL(self, url):
        self.completion.addItem(url)
        self.openURL(url)

    def openURLRequest(self,url):
        self.progress.show()
        self.lastURL = url.url()
        self.htmlPart.openURL(url)
        
    def openURL(self,url):
        self.progress.show()
        if not KURL(url).isValid():
            url = "http://"+url
        self.lastURL = url
        self.htmlPart.openURL(KURL(url))

    def reload(self):
        self.htmlPart.openURL(KURL(self.lastURL))
        
    def empty(self):
        self.htmlPart.openURL(KURL("http://www.yahoo.com"))
        
if __name__ == "__main__":
    description = I18N_NOOP("An experiment in browsing")
    version = "0.0.1"

    about_data = KAboutData("tibet", "Tibet", version, description, KAboutData.License_GPL, "(C) 2006 İsmail Dönmez", None, None)
    KCmdLineArgs.init(sys.argv,about_data)
        
    app = KApplication()
    mw  = MainWidget()

    app.setMainWidget(mw)
    mw.show()

    app.exec_loop()

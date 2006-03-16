#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>
# Resistence is futile, turn on god damn Unicode!

# System
import sys
import math
import posix

# PyQt/PyKDE
from qt import *
from kdecore import *
from kdeui import *
from kio import *
from khtml import *
import kdedesigner

# Local imports
from Enums import *
from Formatter import *
import HelpDialog
import Progress
import Preferences
import ThreadRunner
import PisiUi

# Pisi Imports
import pisi.ui
import pisi.config
import pisi.packagedb
import pisi.installdb
import pisi.repodb
import pisi.context

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

description = I18N_NOOP("GUI for PiSi package manager")
version = "1.0.3"

def AboutData():
    global version,description
    
    about_data = KAboutData("pisi_kga", "PiSi X", version, \
                            description, KAboutData.License_GPL,
                            "(C) 2005,2006 UEKAE/TÜBİTAK", None, None, "ismail@uludag.org.tr")
    
    about_data.addAuthor("İsmail Dönmez", I18N_NOOP("Author"), "ismail@uludag.org.tr")
    about_data.addAuthor("Görkem Çetin",I18N_NOOP("GUI Design & Usability"), "gorkem@uludag.org.tr")
    about_data.addAuthor("Eray Özkural", I18N_NOOP("Search, Component/Category"), "eray@uludag.org.tr")
    about_data.addCredit("Gürer Özen", I18N_NOOP("Python coding help"), None)
    about_data.addCredit("Barış Metin",  I18N_NOOP("Helping with PiSi API"), None)
    about_data.addCredit("PiSi Authors", I18N_NOOP("Authors of PiSi API"), "pisi@uludag.org.tr")
    about_data.addCredit("Simon Edwards", I18N_NOOP("Author of PyKDEeXtensions"),"simon@simonzone.com")
    return about_data

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

class MainApplicationWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, "PiSi X")

        # Create a ThreadRunner and init the database
        self.command = ThreadRunner.PisiThread(self)
        self.command.initDatabase()
                        
        self.progressDialog = Progress.Progress(self)
        self.packagesOrder = []
        self.selectedItems = []
        self.currentOperation = None
        self.currentFile = None
        self.currentRepo = None
        self.totalAppCount = 1
        self.currentAppIndex = 1
        self.totalSelectedSize = 0

        self.layout = QGridLayout(self)
        self.buttonLayout = QHBox(self)
        self.leftLayout = QVBox(self)
        self.htmlPart = KHTMLPart(self)
        self.comboBox = QComboBox(self.leftLayout)
        self.listView = KListView(self.leftLayout)
        self.configButton = KPushButton(i18n("Configure Pisi X"),self.buttonLayout)
        self.installRemoveButton = KPushButton(i18n("InstallPackages"),self.buttonLayout)

        self.comboBox.insertItem(i18n("Show installed packages"))
        self.comboBox.insertItem(i18n("Show new packages"))
        self.comboBox.insertItem(i18n("Show upgrades"))

        self.leftLayout.setMargin(2)
        self.buttonLayout.setMargin(2)
        self.leftLayout.setSpacing(5)
        self.buttonLayout.setSpacing(5)
        
        self.layout.addWidget(self.leftLayout,1,1)
        self.layout.addWidget(self.htmlPart.view(),1,2)
        self.layout.addWidget(self.buttonLayout,2,2)
        self.layout.setColStretch(1,3)
        self.layout.setColStretch(2,6)
        self.resize(700,500)

        self.connect(self.configButton,SIGNAL("clicked()"),self.showPreferences)
        self.connect(self.installRemoveButton,SIGNAL("clicked()"),self.check)
        self.connect(self.listView,SIGNAL("selectionChanged(QListViewItem *)"),self.updateView)
        self.connect(self.comboBox,SIGNAL("activated(int)"),self.updateListing)

        self.createComponentList(self.command.listPackages())
        self.listView.setSelected(self.listView.firstChild(),True)
        self.show()
        
        # Check for empty repo.
        self.initialCheck()

    def updateListing(self,index):
        if index == 0:
            self.createComponentList(self.command.listPackages())
        elif index == 1:
            self.createComponentList(self.command.listAvailable())
        else:
            self.createComponentList(self.command.listUpgradable())

        self.listView.setSelected(self.listView.firstChild(),True)
                
    def initialCheck(self):
        if not nonPrivMode:
            try:
                repo = pisi.context.repodb.list()[0]
                pkg_db = pisi.packagedb.get_db(repo)
                self.packageList = pkg_db.list_packages()
            except:
                confirm = KMessageBox.questionYesNo(self,i18n("Looks like PiSi repository database is empty\nDo you want to update repository now?"),i18n("PiSi Question"))
                if confirm == KMessageBox.Yes:
                    self.command.addRepo('pardus', 'http://paketler.uludag.org.tr/pardus-1.0/pisi-index.xml')
                    self.command.updateRepo('pardus')
                else:
                    KMessageBox.information(self,i18n("You will not be able to install new programs or update old ones until you update repository."))

    def createHTML(self,packages):
        head =  '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'''
        
        self.htmlPart.begin()
        self.htmlPart.write(head)
        self.htmlPart.write('''<style type="text/css"><!-- @import url(/home/cartman/SVN/repos/pisi-x/src/layout.css); --></style>''')
        self.htmlPart.write('''<script language="JavaScript" src="/home/cartman/SVN/repos/pisi-x/src/animation.js"></script>''')
        self.htmlPart.write("</head><body>")
        self.htmlPart.write(self.createHTMLForPackages(packages))
        self.htmlPart.write('''
        <script type="text/javascript">
        initShowHideDivs();
        </script></body></html>
        ''')
        self.htmlPart.end()

    def createHTMLForPackages(self,packages):
        result = ''
        template ='''
        <!-- package start -->
        <div>
        <div class="checkboks" style="%s"><input type="checkbox" onclick="gorkem_fonksiyonu(this)" name="%s"></div>
        <div class="package_title" style="%s">
        <span class="installed_button"> yüklü </span>
        <img src="/home/cartman/pisix/pisi_kga.png" width="48px" height="48px"><b>%s</b><br>%s<br>
        <span class="version_info">Sürüm : %s - Paket Boyutu : %s</span>
        </div>
        <div class="package_info">
        <div>
        <p>
        %s
        </p>
        </div>
        </div>
        </div>
        <!-- package end -->
        '''
        
        index = 0
        style = ''
        packages.sort()

        for app in packages:
            if index % 2 == 0:
                style = "background-color:#3cBB39"
            else:
                style = ""

            installed = pisi.packagedb.inst_packagedb.has_package(app)
            if installed:
                package = pisi.packagedb.inst_packagedb.get_package(app)
            else:
                package = pisi.packagedb.get_package(app)
            desc = package.description
            summary = package.summary
            version = package.version
            size = FormatNumber(package.installedSize)
            result += template % (style,app,style,app,summary,version,size,desc)
            index += 1

        return result
        
    def updateView(self,item):
        self.createHTML(self.componentDict[item])

    def check(self):
        appsToProcess = []
        document = self.htmlPart.document()
        nodeList = document.getElementsByTagName(DOM.DOMString("input"))
        for i in range(0,nodeList.length()):
            element = DOM.HTMLInputElement(nodeList.item(i))
            if element.checked():
                divNode = element.parentNode().parentNode()
                parentNode = divNode.parentNode()
                parentNode.removeChild(divNode)
                appsToProcess.append(str(element.getAttribute(DOM.DOMString("name"))))
        self.command.remove(appsToProcess)
        
    def createComponentList(self,packages):
         # Components
         self.listView.clear()
         self.listView.addColumn("Components")
         componentNames = pisi.context.componentdb.list_components()
         componentNames.sort()
         components = [pisi.context.componentdb.get_component(x) for x in componentNames]
         self.componentDict = {}
         
         for component in components:
             componentPacks = []
             for package in packages:
                 if package in component.packages:
                     componentPacks.append(package)
             
             if len(componentPacks):
                 item = KListViewItem(self.listView)
                 item.setText(0,u"%s" % component.localName)
                 item.setPixmap(0, KGlobal.iconLoader().loadIcon("package",KIcon.Desktop,KIcon.SizeMedium))
                 self.componentDict[item] = componentPacks
                 
        
    def customEvent(self, event):
        eventType = event.type()
        eventData = event.data()

        print 'Event Type:',eventType,'Event Data:',eventData
        if eventType == CustomEvent.InitError:
            KMessageBox.information(self,i18n("Pisi could not be started! Please make sure no other pisi process is running."),i18n("Pisi Error"))
            sys.exit(1)
        elif eventType == CustomEvent.Finished:
            self.finished()
        elif eventType == CustomEvent.PisiWarning:
            pass
        elif eventType == CustomEvent.PisiError:
            self.showErrorMessage(eventData)
        elif eventType == CustomEvent.AskConfirmation:
            self.showConfirmationMessage(eventData)
        elif eventType == CustomEvent.UpdateProgress:
            self.currentFile = eventData["filename"]
            percent = eventData["percent"]
            rate = round(eventData["rate"],1)
            symbol = eventData["symbol"]
            downloaded = eventData["downloaded_size"]
            totalsize = eventData["total_size"]
            self.updateProgressBar(self.currentFile, percent, rate, symbol, downloaded, totalsize)
        elif eventType == CustomEvent.UpdateListing:
            self.updateListing()
        elif eventType == CustomEvent.PisiNotify:
            if isinstance(eventData,QString):
                if eventData == i18n("removing"):
                    self.currentFile = self.packagesOrder[self.currentAppIndex-1]
                    self.progressDialog.progressBar.setProgress((float(self.currentAppIndex)/float(self.totalApps))*100)
                elif eventData == i18n("installing"):
                    if not self.progressDialog.progressBar.progress():
                        self.progressDialog.progressBar.setProgress((float(self.currentAppIndex)/float(self.totalApps))*100)
                self.currentOperation = eventData
                self.updateProgressText()
            elif eventData in ["installed","removed","upgraded"]:
                self.currentAppIndex += 1
            elif isinstance(eventData,list):
                self.packagesOrder = eventData
                self.totalApps = len(self.packagesOrder)
        elif eventType == CustomEvent.RepositoryUpdate:
            self.currentRepo = eventData
            self.progressDialog.show()
        else:
            print 'Unhandled event:',eventType,'with data',eventData
    
    def showConfirmationMessage(self, question):
        answer = KMessageBox.questionYesNo(self,question,i18n("PiSi Question"))
        event = QCustomEvent(CustomEvent.UserConfirmed)
        if answer == KMessageBox.Yes:
            event.setData(True)
        else:
            event.setData(False)
        QThread.postEvent(self.command.ui,event)

    def showErrorMessage(self, message):
        KMessageBox.error(self,message,i18n("PiSi Error"))
        self.finished()
            
    def finished(self):
        self.selectedItems = []
        self.currentAppIndex = 1
        self.updateListing()
        self.progressDialog.closeForced()
        self.resetProgressBar()
        
    def resetProgressBar(self):
        self.progressDialog.progressBar.setProgress(0)
        self.progressDialog.setLabelText(i18n("<b>Preparing PiSi...</b>"))
        self.progressDialog.speedLabel.setText(i18n('<b>Speed:</b> Unknown'))
        self.progressDialog.sizeLabel.setText(i18n('<b>Downloaded/Total:</b> Unknown'))

    def updateProgressBar(self, filename, length, rate, symbol,downloaded_size,total_size):
        self.updateProgressText()
        self.progressDialog.speedLabel.setText(i18n('<b>Speed:</b> %1 %2').arg(rate).arg(symbol))
        
        downloadedText = FormatNumber(downloaded_size)
        totalText = FormatNumber(total_size)

        self.progressDialog.sizeLabel.setText(i18n('<b>Downloaded/Total:</b> %1/%2').arg(downloadedText).arg(totalText))
        self.progressDialog.progressBar.setProgress((float(downloaded_size)/float(total_size))*100)

    def updateProgressText(self):
        if self.currentFile:
            if self.currentFile.endswith(".xml"):
                self.currentOperation = i18n("updating repository")
                self.currentFile = self.currentRepo
            self.progressDialog.setLabelText(i18n('Now %1 <b>%2</b> (%3 of %4)')
                                             .arg(self.currentOperation).arg(self.currentFile).arg(self.currentAppIndex).arg(self.totalAppCount))
        
    def updateDetails(self,selection):

        icon =  pisi.packagedb.get_package(selection.text(0)).icon
        if icon:
            self.iconLabel.setPixmap(loadIcon(icon))
        else:
            self.iconLabel.setPixmap(loadIcon("package"))
                  
        installed = pisi.packagedb.inst_packagedb.has_package(selection.text(0))
        if installed:
            self.package = pisi.packagedb.inst_packagedb.get_package(selection.text(0))
        else:
            self.package = pisi.packagedb.get_package(selection.text(0))
            
        self.progNameLabel.setText(QString("<qt><h1>"+self.package.name+"</h1></qt>"))

        if self.package.summary != self.package.description:
            self.infoLabel.setText(u"%s<br><br>%s" % (self.package.summary, self.package.description) )
        else:
            self.infoLabel.setText(u"%s" % self.package.summary)
        
        size = self.package.installedSize
        size_string = FormatNumber(size)

        self.moreInfoLabelDetails.setText(i18n("Program Version :")+QString(" <b>")+QString(self.package.version)+QString("</b><br>")+i18n("Program Size :")+QString("<b> ")+QString(size_string)+QString("</b>"))
            
    def installSingle(self):
        app = []
        app.append(str(self.listView.currentItem().text(0)))
        self.command.install(app)
        
    def searchPackage(self):
    
        # search summary / description
        query = unicode(self.queryEdit.text())
        
        # search names
        query.strip()
        if query:
            result = self.command.searchPackage(query)
            result = result.union( self.command.searchPackage(query, 'en' ) )

            for pkg in self.packageList:
                if pkg.find(query) != -1:
                    result.add(pkg)
       
            if not len(result):
                mainwidget.infoWidgetStack.raiseWidget(1)
            else:
                mainwidget.infoWidgetStack.raiseWidget(0)
            
            self.updatePackages(list(result))
        else:
            self.updateListing() # get the whole list if blank query            
    
    def clearSearch(self):
        self.queryEdit.clear()    
        self.updateListing()

    def showPreferences(self):
        self.pref = Preferences.Preferences(self)
        self.pref.show()

    def setShowOnlyPrograms(self,hideLibraries=False):
        global kapp
        self.config = kapp.config()
        self.config.setGroup("General")
        self.config.writeEntry("HideLibraries",hideLibraries)
        self.config.sync()

    def getShowOnlyPrograms(self):
        global kapp
        self.config = kapp.config()
        self.config.setGroup("General")
        return self.config.readBoolEntry("HideLibraries")                                    

# Are we running as a separate standalone application or in KControl?
standalone = __name__=='__main__'

if standalone:
    programbase = QDialog
else:
    programbase = KCModule
    
class MainApplication(programbase):
    def __init__(self,parent=None,name=None):
        global standalone
        global mainwidget

        if standalone:
            QDialog.__init__(self,parent,name)
            self.setCaption("PiSi X")
        else:
            KCModule.__init__(self,parent,name)
            KGlobal.locale().insertCatalogue("pisi_kga")
            # Create a configuration object.
            self.config = KConfig("pisi_kga")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("pisi_kga")

        self.aboutus = KAboutApplication(self)
        self.helpWidget = None

        mainwidget = MainApplicationWidget(self)
        toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
        toplayout.addWidget(mainwidget)
        
    def showHelp(self):
        global mainwidget
        if not self.helpWidget:
            self.helpWidget = HelpDialog.HelpDialog(mainwidget)
            # FIXME make non modal
            self.helpWidget.setModal(True)
        self.helpWidget.show()

    def exec_loop(self):
        global programbase
        
        # Load configuration here
        self.__loadOptions()
        
        programbase.exec_loop(self)
        
        # Save configuration here
        self.__saveOptions()

    def __loadOptions(self):
        global kapp
        config = kapp.config()
        config.setGroup("General")
        size = config.readSizeEntry("Geometry")
        if size.isEmpty():
            self.resize(700,600)
        else:
            self.resize(size)

    def __saveOptions(self):
        global kapp
        config = kapp.config()
        config.setGroup("General")
        config.writeEntry("Geometry", self.size())
        config.sync()
        
    # KControl virtual void methods
    def load(self):
        pass
    def save(self):
        pass
    def defaults(self):
        pass        
    def sysdefaults(self):
        pass
    
    def aboutData(self):
        # Return the KAboutData object which we created during initialisation.
        return self.aboutdata
    
    def buttons(self):
        # Only supply a Help button. Other choices are Default and Apply.
        return KCModule.Help

# This is the entry point used when running this module outside of kcontrol.
def main():
    global kapp
    global nonPrivMode
    global packageToInstall

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)
    KCmdLineArgs.addCmdLineOptions ([("install <package>", I18N_NOOP("Package to install"))])

    if not KUniqueApplication.start():
        print i18n("Pisi KGA is already running!")
        return

    nonPrivMode = posix.getuid()
    kapp = KUniqueApplication(True, True, True)

    args = KCmdLineArgs.parsedArgs()
    if args.isSet("install"):
        packageToInstall = str(KIO.NetAccess.mostLocalURL(KURL(args.getOption("install")), None).path())
    else:
        packageToInstall = None

    myapp = MainApplication()
    kapp.setMainWidget(myapp)
        
    sys.exit(myapp.exec_loop())
    
# Factory function for KControl
def create_pisi_kga(parent,name):
    global kapp
    global nonPrivMode
    global packageToInstall
   
    packageToInstall = None
    nonPrivMode = posix.getuid()
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)

if standalone:
    main()

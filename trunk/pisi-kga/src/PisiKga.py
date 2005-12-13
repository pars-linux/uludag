#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
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
# Resistence is futile, turn on god damn Unicode on!

# System
import sys
import math

# PyQt/PyKDE
from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

# Local imports
import MainWindow
import ProgressDialog
import ThreadRunner
import PisiUi
import Success

# Pisi Imports
import pisi.ui
import pisi.config
import pisi.api
import pisi.packagedb
import pisi.installdb
import pisi.repodb
import pisi.context

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

description = I18N_NOOP("GUI for PiSi package manager")
version = "1.0_rc2"

def AboutData():
    global version,description
    
    about_data = KAboutData("pisi_kga", "PiSi KGA", version, \
                            description, KAboutData.License_GPL,
                            "(C) 2005 UEKAE/TÜBİTAK", None, None, "ismail@uludag.org.tr")
    
    about_data.addAuthor("İsmail Dönmez", I18N_NOOP("Author"), "ismail@uludag.org.tr")
    about_data.addAuthor("Görkem Çetin",I18N_NOOP("GUI Design & Usability"), "gorkem@uludag.org.tr")
    about_data.addAuthor("Eray Özkural", I18N_NOOP("Intuitive Search Interface"), "eray@uludag.org.tr")
    about_data.addCredit("Gürer Özen", I18N_NOOP("Python coding help"), None)
    about_data.addCredit("Barış Metin",  I18N_NOOP("Helping with PiSi api"), None)
    about_data.addCredit("Simon Edwards", I18N_NOOP("Author of PyKDEeXtensions"),"simon@simonzone.com")
    return about_data

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

class MainApplicationWidget(MainWindow.MainWindow):
    def __init__(self, parent=None):
        MainWindow.MainWindow.__init__(self, parent, "PiSi KGA")

        global glob_ui
        self.errorMessage = None
        self.savedProgress = 0
        self.oldFilename = None
        self.updatedRepo = None
        self.pDialog = ProgressDialog.ProgressDialog(self)
        self.command = ThreadRunner.MyThread(self)
        self.selectedItems = []
        self.totalSelectedSize = 0
        self.confirmed = None
        self.operation = None
        self.operationInfo = None    
        # Init pisi repository
        glob_ui = PisiUi.PisiUi(self)
        pisi.api.init(database=True, options=None, ui=glob_ui, comar=True)
        
        # Sanity check
        # FIXME: would be nice if these were put in special try:except
        repo = pisi.context.repodb.list()[0]
        pkg_db = pisi.packagedb.get_db(repo)
        self.packageList = pkg_db.list_packages()
            
        if not len(pisi.api.ctx.repodb.list()) or not len(self.packageList): 
            #FIXME: Here, it might be appropriate to have the user confirm
            self.command.updateRepo(repo)

    def customEvent(self, event):
        if event.type() == QEvent.User+1:
            self.finished()
        elif event.type() == QEvent.User+2:
            self.pDialog.setCaption(i18n("Updating repositories"))
            self.updatedRepo = event.data()
            self.pDialog.show()
        elif event.type() == QEvent.User+4:
            self.pisiError(event.data())
        elif event.type() == QEvent.User+5:
            self.operationInfo = event.data()
        elif event.type() == QEvent.User+6:
            self.showConfirm()
        elif event.type() == QEvent.User+7:
            filename = event.data().section(' ',0,0)
            percent = event.data().section(' ',1,1).toInt()[0]
            rate = int(str(event.data().section(' ',2,2)).split('.')[0])
            symbol = event.data().section(' ',3,3)
            self.updateProgressBar(filename, percent, rate, symbol)
        else:
            pass
    
    def showConfirm(self):
        self.confirmed = KMessageBox.warningContinueCancel(self, self.operationInfo, i18n("PiSi Info"))
        event = QCustomEvent(QEvent.User+8)
        if self.confirmed == KMessageBox.Cancel:
            event.setData("False")
            self.finished()
        else:
            event.setData("True")
        kapp.postEvent(glob_ui,event)
    
    def finished(self):
        self.queryEdit.clear()
        self.pDialog.close()
        self.resetProgressBar()

        if self.confirmed == KMessageBox.Cancel:
            pass
        elif not self.errorMessage:
            success = Success.Success(self)
            if not len(self.selectedItems):
                success.infoLabel.setText(i18n("All repositories are successfully updated!"))
                success.showButton.hide()
            elif self.operation == "install":
                success.infoLabel.setText(i18n("All selected packages are successfully installed!"))
                text = i18n("installed")
            elif self.operation == "remove":
                success.infoLabel.setText(i18n("All selected packages are successfully removed!"))
                text = i18n("removed")
            else:
                success.infoLabel.setText(i18n("All selected packages are successfully updated!"))
                text = i18n("updated")
            
            for i in self.selectedItems:
                success.infoBrowser.append(i+" "+text)
            self.operation = None
            success.show()
        else:
            KMessageBox.error(self, self.errorMessage, i18n("PiSi Error"))

        self.updateListing(mainwidget.selectionGroup.selectedId())
        self.errorMessage = None

    def resetProgressBar(self):
        self.savedProgress = 0
        self.pDialog.progressBar.setProgress(0)
        self.pDialog.progressLabel.setText(i18n("Preparing PiSi..."))

    def updateProgressBar(self, filename, length, rate, symbol):
        if rate < 0:
            rate = 0
            
        if filename.endsWith(".pisi"):
            self.pDialog.progressLabel.setText(i18n('Now installing <b>%1</b> (Speed: %2 %3)').arg(filename).arg(rate).arg(symbol))
        else:
            self.totalAppCount = 1
            self.pDialog.progressLabel.setText(i18n('Updating repo <b>%1</b> (Speed: %2 %3)').arg(self.updatedRepo).arg(rate).arg(symbol))

        progress = length/self.totalAppCount + self.savedProgress

        if length == 100 and filename == self.oldFilename:
            return
        elif length == 100 and filename != self.oldFilename:
           self.savedProgress = self.savedProgress + length/self.totalAppCount
           self.oldFilename = filename
        
        self.pDialog.progressBar.setProgress(progress)

    def pisiError(self, msg):
        # Re-init database because we finalized it in our exception handler
        pisi.api.init(database=True, options=None, ui=glob_ui, comar=True)

        self.pDialog.close()
        if self.errorMessage:
            self.errorMessage = self.errorMessage+msg
        else:
            self.errorMessage = msg
        
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

        self.infoLabel.setText(u"%s<br><br>%s" % (self.package.summary, self.package.description) )
        
        size = self.package.installedSize
        
        if size >= 1024*1024:
            size_string = str(size/(1024*1024))+" MB"
        elif size >= 1024:
            size_string = str(size/1024)+" KB"
        else:
            size_string = str(size)+ i18n(" Byte")

        self.moreInfoLabelDetails.setText(i18n("Program Version :")+" <b>"+self.package.version+"</b><br>"+i18n("Program Size :")+"<b> "+size_string+"</b>")
            
    def updateButtons(self, listViewItem=None):
        try:
            text = str(listViewItem.text(0))

            if pisi.packagedb.inst_packagedb.has_package(text):
                self.package = pisi.packagedb.inst_packagedb.get_package(text)
            else:
                self.package = pisi.packagedb.get_package(text)
        
            if listViewItem.isOn():
                self.installOrRemoveButton.setEnabled(True)
                self.selectedItems.append(text)
                self.totalSelectedSize += self.package.installedSize
            else:
                self.selectedItems.remove(text)
                self.totalSelectedSize -= self.package.installedSize
                if len(self.selectedItems):
                    self.installOrRemoveButton.setEnabled(True)
                else:
                    self.installOrRemoveButton.setEnabled(False)
        except:
            self.installOrRemoveButton.setEnabled(False)

    def updateSelectionInfo(self):
        if len(self.selectedItems):
            if self.totalSelectedSize >= 1024*1024 :
                self.selectionInfo.setText(i18n('Selected %1 packages, total size %2 MB').arg(len(self.selectedItems)).arg(self.totalSelectedSize/(1024*1024)))
            elif self.totalSelectedSize >= 1024 :
                self.selectionInfo.setText(i18n('Selected %1 packages, total size %2 KB').arg(len(self.selectedItems)).arg(self.totalSelectedSize/(1024)))
            else:
                self.selectionInfo.setText(i18n('Selected %1 packages, total size %2 Bytes').arg(len(self.selectedItems)).arg(self.totalSelectedSize))
        else:
            self.selectionInfo.setText(i18n("No package selected"))
        
    def updatePackages(self, list):
        self.packageList = list
        self.listView.clear()
        self.selectedItems = []

        self.queryEdit.clear()
        self.updateButtons()
        self.updateSelectionInfo()

        # list components
        componentNames = pisi.context.componentdb.list_components()
        componentNames.sort() # necessary
        components = [pisi.context.componentdb.get_component(x) for x in componentNames]
        self.componentDict = {}
        for component in components:
            componentItem = KListViewItem(self.listView,None)
            componentItem.setOpen(True)
            name = component.name
            if component.localName:
                name += u' (%s)' % component.localName
                #name = unicode(component.localName)
            componentItem.setText(0, name)
            componentItem.setPixmap(0,loadIcon('package_system', KIcon.Small))
            componentItem.setSelectable(False)
            self.componentDict[component.name] = (component, componentItem)

        list.sort()
        for pack in list:
            parent = self.listView
            # find component
            ix = 0
            for compname, (component, componentItem) in self.componentDict.items():
                if pack in component.packages:
                    parent = componentItem
                    break
            item = QCheckListItem(parent,pack,QCheckListItem.CheckBox)
            item.setText(1,pisi.packagedb.get_package(pack).version)

        # Select first item in the list
        try:
            self.listView.setSelected(packages.firstChild(),True)
        except:
            pass

    def updateListing(self, index=0):

        # Check if updateSystemButton should be enabled
        if len(pisi.api.list_upgradable()) > 0:
            self.updateSystemButton.setEnabled(True)
        else:
            self.updateSystemButton.setEnabled(False)
        
        if index == 0 :
            # Show only installed apps
            list = pisi.packagedb.inst_packagedb.list_packages()
            self.installOrRemoveButton.setText(i18n("Remove package(s)"))

        elif index == 1:
            # Only upgrades
            list = pisi.api.list_upgradable()
            self.installOrRemoveButton.setText(i18n("Update package(s)"))
        
        elif index == 2 :
            # Show only not-installed apps
            for repo in pisi.context.repodb.list():
                pkg_db = pisi.packagedb.get_db(repo)
                list = pkg_db.list_packages()
            self.installOrRemoveButton.setText(i18n("Install package(s)"))
            
        self.updatePackages(list)

    def installRemoveFinished(self):
        self.selectedItems = []
        self.installOrRemoveButton.setEnabled(True)
        self.updateListing(self.selectionGroup.selectedId())
        
    def installRemove(self):
        index = mainwidget.selectionGroup.selectedId()
        self.installOrRemoveButton.setEnabled(False)

        self.pDialog.setCaption(i18n("Add or Remove Programs"))
        self.pDialog.show()
        
        self.totalAppCount = len(pisi.api.package_graph(self.selectedItems, True).vertices())

        if index == 0: # Remove baby
            self.operation = "remove"
            self.command.remove(self.selectedItems)
                        
        elif index == 1: # Upgrade baby
            self.operation = "upgrade"
            self.command.upgrade(self.selectedItems)
                    
        elif index == 2: # Install baby
            self.operation = "install"
            self.command.install(self.selectedItems)

    def updateSystem(self):
        self.installOrRemoveButton.setEnabled(False)

        self.pDialog.setCaption(i18n("Add or Remove Programs"))
        self.pDialog.show()
                                
        list = pisi.api.list_upgradable()
        self.totalAppCount = len(list)
        self.operation = "upgrade"            
        self.command.upgrade(list)
           
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
            result = pisi.api.search_package(query)

            for pkg in self.packageList:
                if pkg.find(query) != -1:
                    result.add(pkg)
        
            self.updatePackages(list(result))
        else:
            self.updateListing(self.selectionGroup.selectedId()) # get the whole list if blank query            

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
            self.setCaption("PiSi KGA")
        else:
            KCModule.__init__(self,parent,name)
            # Create a configuration object.
            self.config = KConfig("pisi_kga")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("pisi_kga")

        # About object
        self.aboutus = KAboutApplication(self)

        mainwidget = MainApplicationWidget(self)
        toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
        toplayout.addWidget(mainwidget)
        mainwidget.listView.setResizeMode(KListView.LastColumn)
        #mainwidget.clearButton.setPixmap(loadIcon('locationbar_erase', KIcon.Small))
        mainwidget.iconLabel.setPixmap(loadIcon('package', KIcon.Desktop))

        self.connect(mainwidget.selectionGroup,SIGNAL("clicked(int)"),mainwidget.updateListing)
        self.connect(mainwidget.closeButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(mainwidget.listView,SIGNAL("selectionChanged(QListViewItem *)"),mainwidget.updateDetails)
        self.connect(mainwidget.listView,SIGNAL("clicked(QListViewItem *)"),mainwidget.updateButtons)
        self.connect(mainwidget.listView,SIGNAL("clicked(QListViewItem *)"),mainwidget.updateSelectionInfo)
        self.connect(mainwidget.listView,SIGNAL("spacePressed(QListViewItem *)"),mainwidget.updateButtons)
        self.connect(mainwidget.listView,SIGNAL("spacePressed(QListViewItem *)"),mainwidget.updateSelectionInfo)        
        self.connect(mainwidget.installOrRemoveButton,SIGNAL("clicked()"),mainwidget.installRemove)
        self.connect(mainwidget.updateSystemButton,SIGNAL("clicked()"),mainwidget.updateSystem)
        self.connect(mainwidget.searchButton,SIGNAL("clicked()"),mainwidget.searchPackage)

        mainwidget.selectionGroup.setButton(2);
        mainwidget.updateListing(2);

    def __del__(self):
        pass

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
    
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)

    if not KUniqueApplication.start():
        print i18n("Pisi KGA is already running!")
        return

    kapp = KUniqueApplication(True, True, True)
    myapp = MainApplication()
    kapp.setMainWidget(myapp)
    sys.exit(myapp.exec_loop())
    
# Factory function for KControl
def create_pisi_kga(parent,name):
    global kapp
    
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)

if standalone:
    main()

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
import Preferences
import ProgressDialog
import ThreadRunner
import PisiUi

# Pisi Imports
import pisi.ui
import pisi.config
import pisi.api
import pisi.packagedb
import pisi.installdb
import pisi.repodb

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

description = I18N_NOOP("PiSi paket yöneticisi için arayüz")
version = "1.0_alpha4"

def AboutData():
    global version,description
    
    about_data = KAboutData("pisi_kga", "PiSi KGA", version, \
                            description, KAboutData.License_GPL,
                            "(C) 2005 UEKAE/TÜBİTAK", None, None, "ismail@uludag.org.tr")
    
    about_data.addAuthor("İsmail Dönmez", None, "ismail@uludag.org.tr")
    about_data.addCredit(I18N_NOOP("Gürer Özen"), I18N_NOOP("Python kodlama yardımı"), None)
    about_data.addCredit(I18N_NOOP("Barış Metin"),  I18N_NOOP("PiSi API konusunda yardım"), None)
    about_data.addCredit("Simon Edwards", I18N_NOOP("PyKDEExtension'ın yazarı"),"simon@simonzone.com")
    return about_data

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

def loadIconSet(name, group=KIcon.Desktop):
        return KGlobal.iconLoader().loadIconSet(name, group)

class MainApplicationWidget(MainWindow.MainWindow):
    def __init__(self, parent=None):
        MainWindow.MainWindow.__init__(self, parent, "PiSi KGA")

        global glob_ui
        self.errorMessage = None
	self.savedProgress = 0
        self.oldFilename = None
        self.updatedRepo = None
        self.pref = None
        self.pDialog = ProgressDialog.ProgressDialog(self)
        self.command = ThreadRunner.MyThread(self)
        
        # Init pisi repository
        glob_ui = PisiUi.PisiUi(self)
        pisi.api.init(database=True, options=None, ui=glob_ui, comar=False)
        
        # Sanity check
        if not len(pisi.api.ctx.repodb.list()):
            self.showSettings()
        
    
    def customEvent(self, event):
        if event.type() == QEvent.User+1:
            self.finished()
        elif event.type() == QEvent.User+2:
            self.pDialog.setCaption(u'Depolar Güncelleniyor')
            self.updatedRepo = event.data()
            self.pDialog.show()
        elif event.type() == QEvent.User+4:
            self.pisiError(event.data())
        elif event.type() == QEvent.User+5:
            filename = event.data().section(' ',0,0)
            percent = event.data().section(' ',1,1).toInt()[0]
            self.updateProgressBar(filename, percent)
        else:
            pass
    
    def finished(self):
        self.pDialog.close()
        self.resetProgressBar()
        self.updateListing()
        if self.errorMessage:
            KMessageBox.error(self, self.errorMessage, u'Pisi Hatası')
        self.errorMessage = None

        event = QCustomEvent(QEvent.User+3)
        kapp.postEvent(self.pref,event)

    def resetProgressBar(self):
        self.savedProgress = 0
        self.pDialog.progressBar.setProgress(0)
        self.pDialog.progressLabel.setText(u'PiSi Hazırlanıyor...')

    def updateProgressBar(self, filename, length):
        if filename.endsWith(".pisi"):
            self.pDialog.progressLabel.setText(u'Şu anda işlenilen dosya: <b>%s</b>'%(filename))
        else:
            self.totalAppCount = 1
            self.pDialog.progressLabel.setText(u'Şu anda güncellenen depo: <b>%s</b>'%(self.updatedRepo))

       	progress = length/self.totalAppCount + self.savedProgress

	if length == 100 and filename == self.oldFilename:
            return
        elif length == 100 and filename != self.oldFilename:
           self.savedProgress = self.savedProgress + length/self.totalAppCount
           self.oldFilename = filename
        
        self.pDialog.progressBar.setProgress(progress)

    def pisiError(self, msg):
        self.pDialog.close()
        if self.errorMessage:
            self.errorMessage = self.errorMessage+msg
        else:
            self.errorMessage = msg
        
    def updateDetails(self,selection):

        if selection.childCount():
            return

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
            
        self.progNameLabel.setText(QString("<qt><h1>"+self.package.name.capitalize()+"</h1></qt>"))
        self.infoLabel.setText(self.package.summary)
        
        size = self.package.installedSize
        
        if size >= 1024*1024:
            size_string = str(size/(1024*1024))+" MB"
        elif size >= 1024:
            size_string = str(size/1024)+" KB"
        else:
            size_string = str(size)+ i18n(" Bytes")

        self.moreInfoLabel.setText(QString(": <b>"+self.package.version+"</b><br>: <b>"+size_string+"</b><br>: <b>"+self.package.partof))
            
        if installed:
            self.warningLabel.hide()
            self.installButton.hide()
        else:
            self.warningLabel.show()
            self.installButton.show()
            

    def updateButtons(self):
        # This is slow but we don't have a better method so ...
        listViewItem = self.listView.firstChild()

        try:
            if self.listView.currentItem().isOn(): # Make sure this is a QCheckListItem
                pass
            if self.listView.currentItem().isSelected():
                self.installButton.setEnabled(True)
            else:
                self.installButton.setEnabled(False)
        except AttributeError:
            self.installButton.setEnabled(False)
        
        while listViewItem:
            try:
                if listViewItem.isOn():
                    self.installOrRemoveButton.setEnabled(True)
                    return
            except AttributeError: # This exception is thrown because some items are QListViewItem
                pass
            listViewItem = listViewItem.itemBelow()

        self.installOrRemoveButton.setEnabled(False)

    def updateListing(self, index=-1):
        self.listView.clear()

        if index == -1:
            index = self.selectComboBox.currentItem()
            
        base = QListViewItem(self.listView,None)
        base.setOpen(True)
        base.setText(0,i18n("Temel"))
        base.setPixmap(0,loadIcon('blockdevice', KIcon.Small))

        component = QListViewItem(self.listView,None)
        component.setOpen(True)
        component.setText(0,i18n("Bileşen"))
        component.setPixmap(0,loadIcon('package', KIcon.Small))

        # Check if updateSystemButton should be enabled
        if len(pisi.api.list_upgradable()) > 0:
            self.updateSystemButton.setEnabled(True)
        else:
            self.updateSystemButton.setEnabled(False)
        
        if index == 0 :
            # Show only installed apps
            list = pisi.packagedb.inst_packagedb.list_packages()
            list.sort()
            for pack in list:
                if pisi.packagedb.get_package(pack).partof == 'base':
                    partof = base
                elif pisi.packagedb.get_package(pack).partof == 'component':
                    partof = component
                item = QCheckListItem(partof,pack,QCheckListItem.CheckBox)
                item.setText(1,pisi.packagedb.get_package(pack).version)

        elif index == 1:
            # Only upgrades
            list = pisi.api.list_upgradable()
            list.sort()
            for pack in list:
                if pisi.packagedb.get_package(pack).partof == 'base':
                    partof = base
                elif pisi.packagedb.get_package(pack).partof == 'component':
                    partof = component
                    item = QCheckListItem(partof,pack,QCheckListItem.CheckBox)
                    item.setText(1,pisi.packagedb.get_package(pack).version)
        
        elif index == 2 :
            # Show only not-installed apps
            for repo in pisi.context.repodb.list():
                pkg_db = pisi.packagedb.get_db(repo)
                list = pkg_db.list_packages()
                list.sort()
                for pack in list:
                    if  not pisi.packagedb.inst_packagedb.has_package(pack):
                        if pisi.packagedb.get_package(pack).partof == 'base':
                            partof = base
                        elif pisi.packagedb.get_package(pack).partof == 'component':
                            partof = component
                        item = QCheckListItem(partof,pack,QCheckListItem.CheckBox)
                        item.setText(1,pisi.packagedb.get_package(pack).version)

        item = self.listView.firstChild()

        try:
            while not item.firstChild():
                item = item.itemBelow()
            self.listView.setSelected(item.firstChild(), True)
            self.installButton.setEnabled(True)
        except AttributeError:
            pass

    def installRemoveFinished(self):
        self.installOrRemoveButton.setEnabled(True)
        self.updateListing()
        
    def installRemove(self):
        index = self.selectComboBox.currentItem()
        self.installOrRemoveButton.setEnabled(False)

        self.pDialog.setCaption(i18n("Program Ekle ve Kaldır"))
        self.pDialog.show()
        
	# Get the list of selected items
        self.selectedItems = []
        listViewItem = self.listView.firstChild()

        while listViewItem:
            try:
                if listViewItem.isOn():
                    self.selectedItems.append(str(listViewItem.text(0)))
            except AttributeError: # This exception is thrown because some items are QListViewItem
                pass

            listViewItem = listViewItem.itemBelow()

        self.totalAppCount = len(pisi.api.package_graph(self.selectedItems, True).vertices())
        print 'Total app count',self.totalAppCount
                
        if index == 0: # Remove baby
            self.command.remove(self.selectedItems)
                        
        elif index == 1: # Upgrade baby
            self.command.upgrade(self.selectedItems)
            	    
        elif index == 2: # Install baby
            self.command.install(self.selectedItems)
            
    def installSingle(self):
        app = []
        app.append(str(self.listView.currentItem().text(0)))
        self.command.install(app)

    def showSettings(self):
        self.pref = Preferences.Preferences(self)
        self.pref.setModal(True)
        self.pref.show()
        

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
            self.setFixedSize(700,600)
        else:
            KCModule.__init__(self,parent,name)
            # Create a configuration object.
            self.config = KConfig("pisi_kga")
            self.setButtons(0)
            self.aboutdata = AboutData()

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir("pisi_kga")

        mainwidget = MainApplicationWidget(self)
        toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
        toplayout.addWidget(mainwidget)
        mainwidget.warningLabel.hide()
        mainwidget.installButton.hide()
        mainwidget.listView.setResizeMode(QListView.LastColumn)
        mainwidget.clearButton.setPixmap(loadIcon('locationbar_erase', KIcon.Small))
        mainwidget.iconLabel.setPixmap(loadIcon('package', KIcon.Desktop))
        mainwidget.searchLine.setListView(mainwidget.listView)
	mainwidget.searchLine.setSearchColumns([0])

        self.connect(mainwidget.closeButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(mainwidget.listView,SIGNAL("selectionChanged(QListViewItem *)"),mainwidget.updateDetails)
        self.connect(mainwidget.listView,SIGNAL("clicked(QListViewItem *)"),mainwidget.updateButtons)
        self.connect(mainwidget.selectComboBox,SIGNAL("activated(int)"),mainwidget.updateListing)
        self.connect(mainwidget.installOrRemoveButton,SIGNAL("clicked()"),mainwidget.installRemove)
        self.connect(mainwidget.installButton,SIGNAL("clicked()"),mainwidget.installSingle)
        self.connect(mainwidget.settingsButton,SIGNAL("clicked()"),mainwidget.showSettings)

        self.aboutus = KAboutApplication(self)

        if not standalone:
            mainwidget.updateListing(0)

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
        listBoxSelection = config.readNumEntry("ListBoxSelection",0)
        mainwidget.selectComboBox.setCurrentItem(listBoxSelection)
        mainwidget.updateListing(listBoxSelection)
        if size.isEmpty()==False:
            self.resize(size)

    def __saveOptions(self):
        global kapp
        config = kapp.config()
        config.setGroup("General")
        config.writeEntry("Geometry", self.size())
        config.writeEntry("ListBoxSelection",mainwidget.selectComboBox.currentItem())
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

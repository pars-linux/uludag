#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# PiSi KGA - GUI for PiSi package manager                                 #
# ------------------------------                                          #
# begin     : Pzt Ağu 15 10:07:29 EEST 2005                               #
# copyright : (C) 2005 by UEKAE/TÜBİTAK                                   #
# email     : ismail@uludag.org.tr                                        #
#                                                                         #
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
###########################################################################

# System
import sys

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

# Pisi Imports
import pisi.ui
import pisi.config
import pisi.api
import pisi.packagedb
import pisi.installdb
import pisi.repodb

############################################################################
# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

############################################################################
description = I18N_NOOP("A GUI for PiSi package manager")
version = "0.4"

############################################################################
def AboutData():
    global version,description
    
    about_data = KAboutData("pisi_kga", "PiSi KGA", version, \
                            description, KAboutData.License_GPL,
                            "(C) 2005 UEKAE/TÜBİTAK", None, None, "ismail@uludag.org.tr")
    
    about_data.addAuthor("İsmail Dönmez", None, "ismail@uludag.org.tr")
    about_data.addCredit(I18N_NOOP("Madcat"), I18N_NOOP("Helping with my Python troubles"), None)
    about_data.addCredit(I18N_NOOP("PiSi Authors"),  I18N_NOOP("The reason this application exists"), None)
    about_data.addCredit("Simon Edwards", I18N_NOOP("Author of beautiful PyKDE extensions"),"simon@simonzone.com")
    return about_data

############################################################################
def loadIcon(name, group=KIcon.NoGroup):
    return KGlobal.iconLoader().loadIcon(name, group)

############################################################################
class MainApplicationWidget(MainWindow.MainWindow):
    def __init__(self, parent=None):
        MainWindow.MainWindow.__init__(self, parent, "PiSi KGA")

        self.qObject = QObject()
        self.pDialog = ProgressDialog.ProgressDialog(self)

        self.connect(self.qObject,PYSIGNAL("finished()"),self.finished)
        self.connect(self.qObject,PYSIGNAL("progress(str,str)"),self.updateProgressBar)
        self.connect(self.qObject,PYSIGNAL("incrementProgressBar(int)"),self.incrementProgressBar)

    def finished(self):
        self.pDialog.progressBar.setProgress(100)
        self.pDialog.progressBar.close()

    def updateProgressBar(self, app, action):
        self.pDialog.progressLabel.setText("<qt>Şu anda %s: <b>%s</b></qt>"%(action,app))
        
    def incrementProgressBar(self, length):
        length = self.pDialog.progressBar.progress()+length
        self.pDialog.progressBar.setProgress(length)
        
    def updateDetails(self,selection):

        if selection.childCount():
            return
        
        self.package = pisi.packagedb.get_package(selection.text(0))
        self.progNameLabel.setText(QString("<qt><h1>"+self.package.name.capitalize()+"</h1></qt>"))
        self.infoLabel.setText(self.package.summary)
        
        installed = pisi.packagedb.inst_packagedb.has_package(self.package.name)
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
                
    def updateListing(self,index):
        self.listView.clear()

        base = QListViewItem(self.listView,None)
        base.setOpen(True)
        base.setText(0,i18n("Base"))
        base.setPixmap(0,loadIcon('blockdevice', KIcon.Small))

        component = QListViewItem(self.listView,None)
        component.setOpen(True)
        component.setText(0,i18n("Component"))
        component.setPixmap(0,loadIcon('package', KIcon.Small))
        
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
        index = self.selectComboBox.currentItem()
        self.installOrRemoveButton.setEnabled(True)
        self.updateListing(index)
        
    def installRemove(self):
        index = self.selectComboBox.currentItem()
        self.installOrRemoveButton.setEnabled(False)
        self.command = ThreadRunner.Thread(self.qObject)

        self.pDialog.setCaption(i18n("Program Ekle ve Kaldır"))
        self.pDialog.progressBar.setTotalSteps(100)
        self.pDialog.setModal(True)
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

        if index == 0: # Remove baby
            self.command.remove(self.selectedItems)
            
        elif index == 1: # Upgrade baby
            self.command.upgrade(self.selectedItems)
	    
        elif index == 2: # Install baby
            self.command.install(self.selectedItems)
            

    def installSingle(self):
        index = self.selectComboBox.currentItem()
        app = []
        app.append(str(self.listView.currentItem().text(0)))
        pisi.api.install(app)
        self.updateListing(index)
        print "Finished installing."

    def showSettings(self):
        self.pref = Preferences.Preferences(self)
        self.pref.setModal(True)
        self.pref.show()
        

############################################################################
# The base class that we use depends on whether this is running inside
# kcontrol or as a standalone application.
# Are we running as a separate standalone application or in KControl?
standalone = __name__=='__main__'

if standalone:
    programbase = QDialog
else:
    programbase = KCModule
    
class MainApplication(programbase):
    ########################################################################
    def __init__(self,parent=None,name=None):
        global standalone
        global mainwidget

        # Init pisi repository
        pisi.api.init()

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
        
        if standalone:
            toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
            mainwidget = MainApplicationWidget(self)
        else:
            toplayout = QVBoxLayout( self, 0, KDialog.spacingHint() )
            mainwidget = MainApplicationWidget(self)

        toplayout.addWidget(mainwidget)
        mainwidget.warningLabel.hide()
        mainwidget.installButton.hide()
        mainwidget.listView.setResizeMode(QListView.LastColumn)
        mainwidget.iconLabel.setPixmap(loadIcon('package', KIcon.Desktop))
        mainwidget.searchLine.setListView(mainwidget.listView)
        
        self.connect(mainwidget.closeButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(mainwidget.listView,SIGNAL("selectionChanged(QListViewItem *)"),mainwidget.updateDetails)
        self.connect(mainwidget.listView,SIGNAL("clicked(QListViewItem *)"),mainwidget.updateButtons)
        self.connect(mainwidget.selectComboBox,SIGNAL("activated(int)"),mainwidget.updateListing)
        self.connect(mainwidget.installOrRemoveButton,SIGNAL("clicked()"),mainwidget.installRemove)
        self.connect(mainwidget.installButton,SIGNAL("clicked()"),mainwidget.installSingle)
        self.connect(mainwidget.settingsButton,SIGNAL("clicked()"),mainwidget.showSettings)

        self.aboutus = KAboutApplication(self)

    ########################################################################
    def __del__(self):
        pass

    ########################################################################
    # KDialogBase method
    def exec_loop(self):
        global programbase
        
        # Load configuration here
        self.__loadOptions()
        
        programbase.exec_loop(self)
        
        # Save configuration here
        self.__saveOptions()

    ########################################################################
    # KDialogBase method
    def slotUser1(self):
        self.aboutus.show()

    ########################################################################
    def slotCloseButton(self):
        self.close()

    ########################################################################
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

    #######################################################################
    def __saveOptions(self):
        global kapp
        config = kapp.config()
        config.setGroup("General")
        config.writeEntry("Geometry", self.size())
        config.writeEntry("ListBoxSelection",mainwidget.selectComboBox.currentItem())
        config.sync()

    #######################################################################
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

############################################################################
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
    myapp.exec_loop()
    
############################################################################
# Factory function for KControl
def create_pisi_kga(parent,name):
    global kapp
    
    kapp = KApplication.kApplication()
    return MainApplication(parent, name)

############################################################################
if standalone:
    main()

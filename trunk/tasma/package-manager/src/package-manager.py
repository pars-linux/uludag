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
# Authors: İsmail Dönmez <ismail@pardus.org.tr>
# Resistence is futile, turn on god damn Unicode!

# System
import sys
import string
import re

# PyQt/PyKDE
from qt import *
from kdecore import *
from kdeui import *
from kio import *
from khtml import *

# Local imports
import Progress
import Preferences
import Commander
import UpdateDialog
import CustomEventListener

# Pisi
import pisi

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

description = I18N_NOOP("GUI for PiSi package manager")
version = "1.1.0_b4"
base_packages = set(['qt','kdelibs','kdebase','sip','PyQt','PyKDE'])
(install_state, remove_state) = range(2)

def AboutData():
    global version,description

    about_data = KAboutData("package-manager", I18N_NOOP("Package Manager"), version, description, KAboutData.License_GPL,
                            "(C) 2005, 2006 UEKAE/TÜBİTAK", None, None)

    about_data.addAuthor("İsmail Dönmez", I18N_NOOP("Main Coder"), "ismail@pardus.org.tr")
    about_data.addAuthor("Gökmen Göksel",I18N_NOOP("CSS/JS Meister"), "gokmen@pardus.org.tr")
    about_data.addAuthor("Görkem Çetin",I18N_NOOP("GUI Design & Usability"), "gorkem@pardus.org.tr")
    about_data.addCredit("Eray Özkural", I18N_NOOP("Misc. Fixes"), "eray@pardus.org.tr")
    about_data.addCredit("Gürer Özen", I18N_NOOP("Comar/Python Help"), None)
    about_data.addCredit("Barış Metin",  I18N_NOOP("Speedup fixes"), None)
    about_data.addCredit(I18N_NOOP("PiSi Authors"), I18N_NOOP("Authors of PiSi API"), "pisi@pardus.org.tr")
    return about_data

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

def getIconPath(name, group=KIcon.Desktop):
    if not name:
        name = "package"
    return KGlobal.iconLoader().iconPath(name,group)

class MainApplicationWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent

        self.progressDialog = Progress.Progress(self)

        self.initialRepoCheck = None
        self.packagesOrder = []
        self.componentDict = {}
        self.possibleError = False
        self.state = install_state

        self.layout = QGridLayout(self)
        self.leftLayout = QVBox(self)
        self.rightLayout = QVBox(self)

        self.leftLayout.setSpacing(3)
        self.rightLayout.setSpacing(3)

        # KListViewSearchLineWidget can't be used here, so time to implement ours :P
        self.rightTopLayout = QHBox(self.rightLayout)
        self.rightTopLayout.setSpacing(3)
        self.clearButton = KPushButton(self.rightTopLayout)
        self.clearButton.setIconSet(loadIconSet("locationbar_erase"))
        self.searchLabel = QLabel(i18n("Search: "), self.rightTopLayout)
        self.searchLine = KLineEdit(self.rightTopLayout)
        self.timer = QTimer(self)

        self.htmlPart = KHTMLPart(self.rightLayout)

        self.listView = KListView(self.leftLayout)
        self.listView.setFullWidth(True)

        # Read javascript
        js = file(str(locate("data","package-manager/animation.js"))).read()
        js = re.sub("#3cBB39", KGlobalSettings.alternateBackgroundColor().name(), js)
        js = re.sub("#3c8839", KGlobalSettings.baseColor().name(), js)
        self.javascript = re.sub("#533359",KGlobalSettings.highlightColor().name(), js)

        # Read Css
        cssFile = file(str(locate("data","package-manager/layout.css"))).read()
        self.css = cssFile

        self.listView.addColumn(i18n("Components"))

        self.leftLayout.setMargin(2)
        self.rightLayout.setMargin(2)
        self.leftLayout.setSpacing(5)
        self.rightLayout.setSpacing(5)

        self.layout.addWidget(self.leftLayout,1,1)
        self.layout.addWidget(self.rightLayout,1,2)
        self.layout.setColStretch(1,2)
        self.layout.setColStretch(2,6)

        self.connect(self.listView,SIGNAL("selectionChanged(QListViewItem *)"),self.updateView)
        self.connect(self.htmlPart,SIGNAL("completed()"),self.registerEventListener)
        self.connect(self.htmlPart,SIGNAL("completed()"),self.updateCheckboxes)
        self.connect(self.searchLine,SIGNAL("textChanged(const QString&)"),self.searchStringChanged)
        self.connect(self.timer, SIGNAL("timeout()"), self.searchPackage)
        self.connect(self.clearButton,SIGNAL("clicked()"),self.clearSearchLine)

        self.currentAppList = []

        self.delayTimer = QTimer(self)
        self.connect(self.delayTimer, SIGNAL("timeout()"), self.lazyLoadComponentList)
        self.delayTimer.start(500, True)

        # inform user for the delay...
        item = KListViewItem(self.listView)
        item.setText(0,i18n("Loading Package List..."))
        self.listView.setSelected(self.listView.firstChild(),True)

        self.htmlPart.view().setFocus()
        self.show()

    def lazyLoadComponentList(self):
        self.command = Commander.Commander(self)

        # Show updates dialog if requested
        global showUpdates

        if showUpdates:
            self.update()
        else:
            # Empty repo check
            self.initialCheck()

        self.currentAppList = self.command.listNewPackages()
        self.createComponentList(self.currentAppList)
        self.listView.setSelected(self.listView.firstChild(),True)

    def processEvents(self):
        global kapp
        kapp.processEvents(QEventLoop.ExcludeUserInput)

    def initialCheck(self):
        self.initialRepoCheck = True

        if not pisi.context.componentdb.list_components(): # Repo metadata empty
            self.progressDialog.show()
            self.command.updateAllRepos()

    def repoMetadataCheck(self):
        global kapp

        # At this point if componentList is empty we should quit as there is no way to work reliably
        if not pisi.context.componentdb.list_components():
            KMessageBox.error(self,i18n("Package repository still does not have category information.\nExiting..."),i18n("Error"))
            kapp.quit()

    def switchListing(self):
        self.updateListing(True)

    def updateListing(self,switch=False):

        if switch or self.possibleError:
            self.eventListener.packageList = []
            self.parent.operateAction.setEnabled(False)
            self.parent.basketAction.setEnabled(False)
            self.clearSearchLine(False)

        if self.state == remove_state:
            if switch:
                self.currentAppList = self.command.listNewPackages()
                self.createComponentList(self.currentAppList)
                self.parent.showAction.setText(i18n("Show Installed Packages"))
                self.parent.showAction.setIconSet(loadIconSet("package"))
                self.parent.operateAction.setText(i18n("Install Package(s)"))
                self.parent.operateAction.setIconSet(loadIconSet("ok"))
                self.state = install_state
            else:
                self.currentAppList = self.command.listPackages()
                self.createComponentList(self.currentAppList)
        elif self.state == install_state:
            if switch:
                self.currentAppList = self.command.listPackages()
                self.createComponentList(self.currentAppList)
                self.parent.showAction.setText(i18n("Show New Packages"))
                self.parent.showAction.setIconSet(loadIconSet("edit_add"))
                self.parent.operateAction.setText(i18n("Remove Package(s)"))
                self.parent.operateAction.setIconSet(loadIconSet("no"))
                self.state = remove_state
            else:
                self.currentAppList = self.command.listNewPackages()
                self.createComponentList(self.currentAppList)

        self.listView.setSelected(self.listView.firstChild(),True)

    def createHTML(self,packages,part=None):
        head =  '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        '''

        if not part:
            part = self.htmlPart

        part.begin()
        part.write(head)
        part.write("<style type=\"text/css\">%s</style>" % self.css)
        part.write("<script language=\"JavaScript\">%s</script>" % self.javascript)
        part.write("</head><body>")
        part.write('''<font size="-2"><a href="#selectall">'''+i18n("Select all packages in this category")+'''</a></font>''')
        part.write(self.createHTMLForPackages(packages))
        part.write('''
        <script type="text/javascript">
        initShowHideDivs();
        </script></body></html>
        ''')
        part.end()

    def createHTMLForPackages(self,packages):
        result = ''
        template ='''
        <!-- package start -->
        <div>
        <div class="checkboks" style="%s"><input type="checkbox" onclick="gorkem_fonksiyonu(this)" name="%s"></div>
        <div class="package_title" style="%s">
        <img src="%s" style="float:left;" width="48px" height="48px">
        <b>%s</b><br>%s<br>
        </div>
        <div class="package_info" style="%s">
        <div style="margin-left:25px;">
        <p><b>%s</b>
        %s<br>
        <b>%s</b>%s<br><b>%s</b>%s<br><b>%s</b><a href=\"%s\">%s</a>
        </p>
        </div>
        </div>
        </div>
        <!-- package end -->
        '''

        index = 0
        style = ''
        packages.sort(key=string.lower)

        for app in packages:
            if index % 2 == 0:
                style = "background-color:%s" % KGlobalSettings.alternateBackgroundColor().name()
            else:
                style = "background-color:%s" % KGlobalSettings.baseColor().name()

            if not pisi.packagedb.ctx.installdb.is_installed(app):
                package = pisi.context.packagedb.get_package(app)
            else:
                package = pisi.context.packagedb.get_package(app, pisi.itembyrepodb.installed)

            desc = package.description
            summary = package.summary
            version = package.version
            size = package.packageSize
            iconPath = getIconPath(package.icon)

            if package.source:
                homepage = package.source.homepage
            else:
                homepage = 'http://paketler.pardus.org.tr'

            if size:
                tpl = pisi.util.human_readable_size(size)
                size = "%.0f %s" % (tpl[0], tpl[1])
            else:
                size = i18n("N\A")
            result += template % (style,app,style,iconPath,app,summary,style,i18n("Description: "),desc,i18n("Version: "),
                                  version,i18n("Package Size: "),size,i18n("Homepage: "),homepage,homepage)
            index += 1

        return result

    def registerEventListener(self):
        self.eventListener = CustomEventListener.CustomEventListener(self)
        node = self.htmlPart.document().getElementsByTagName(DOM.DOMString("body")).item(0)
        node.addEventListener(DOM.DOMString("click"),self.eventListener,True)

    def updateCheckboxes(self):
        self.htmlPart.view().setUpdatesEnabled(False)
        if self.eventListener.packageList:
            document = self.htmlPart.document()
            nodeList = document.getElementsByTagName(DOM.DOMString("input"))
            for i in range(0,nodeList.length()):
                element = DOM.HTMLInputElement(nodeList.item(i))
                if element.name().string() in self.eventListener.packageList:
                    element.click()
        self.htmlPart.view().setUpdatesEnabled(True)

    def updateView(self,item):
        try:
            self.createHTML(self.componentDict[item])
        except:
            pass

    def updateButtons(self):
        if self.eventListener.packageList:
            self.parent.operateAction.setEnabled(True)
            self.parent.basketAction.setEnabled(True)
        else:
            self.parent.operateAction.setEnabled(False)
            self.parent.basketAction.setEnabled(False)

    def showBasket(self):
        print "Show me the basket"
        pass

    def takeAction(self):
        # install or remove button action taker
        appsToProcess = []
        document = self.htmlPart.document()
        nodeList = document.getElementsByTagName(DOM.DOMString("input"))
        for i in range(0,nodeList.length()):
            element = DOM.HTMLInputElement(nodeList.item(i))
            if element.checked():
                divNode = element.parentNode().parentNode()
                parentNode = divNode.parentNode()
                parentNode.removeChild(divNode)
                packageName = str(element.getAttribute(DOM.DOMString("name")).string())
                appsToProcess.append(packageName)
                self.componentDict[self.listView.currentItem()].remove(packageName)

        self.progressDialog.show()
        if self.state == remove_state:
            self.command.remove(appsToProcess)
        else:
            self.command.install(appsToProcess)

    def createComponentList(self, packages):
        # Components
        self.listView.clear()
        self.componentDict.clear()

        componentNames = ["desktop.kde","desktop.gnome","desktop.freedesktop","applications.network","applications.multimedia",
                          "applications.games","applications.hardware","system.base","system.devel", "system.kernel.drivers","system.kernel.firmware"]
        components = [pisi.context.componentdb.get_component(x) for x in componentNames]
        componentPackages = []

        for component in components:
            if len(component.packages):
                componentPackages += component.packages
                item = KListViewItem(self.listView)
                if component.localName:
                    item.setText(0,u"%s" % component.localName)
                else:
                    item.setText(0,u"%s" % component.name)
                item.setPixmap(0, KGlobal.iconLoader().loadIcon("package",KIcon.Desktop,KIcon.SizeMedium))
                self.componentDict[item] = [x for x in component.packages if x in packages]

        # Rest of the packages
        packages = list(set(self.command.listPackages()) - set(componentPackages))

        item = KListViewItem(self.listView)
        item.setText(0,i18n("Others"))
        item.setPixmap(0, KGlobal.iconLoader().loadIcon("package",KIcon.Desktop,KIcon.SizeMedium))
        self.componentDict[item] = packages

    def createSearchResults(self, packages):
        self.listView.clear()
        self.componentDict.clear()

        item = KListViewItem(self.listView)
        item.setText(0,i18n("Search Results"))
        item.setPixmap(0, KGlobal.iconLoader().loadIcon("find",KIcon.Desktop,KIcon.SizeMedium))
        self.componentDict[item] = list(packages)
        self.listView.setSelected(self.listView.firstChild(),True)

#   @data: [operation, <arg1>, <arg2>, <arg3> ...]
#           "downloading": <name>
    def pisiNotify(self,data):
        data = data.split(",")
        operation = data[0]

        self.progressDialog.currentOperation = i18n(str(operation))
        if operation == "removing":
#             if len(self.updatesToProcess):
#                 self.progressDialog.currentAppIndex += 1

            self.progressDialog.currentFile = self.packagesOrder[self.progressDialog.currentAppIndex-1]
        elif operation in ["downloading", "installing"]:
            self.progressDialog.currentFile = data[1]
            self.progressDialog.updateProgressText()
        elif operation in ["extracting","configuring"]:
            self.progressDialog.updateProgressText()
        elif operation in ["installed","removed","upgraded"]:
            self.progressDialog.currentAppIndex += 1
        elif operation in ["removing"]:
            self.packagesOrder = data
            self.progressDialog.totalAppCount = len(self.packagesOrder)

            if self.state == remove_state:
                if len(base_packages.intersection(self.packagesOrder)) > 0:
                    self.showErrorMessage(i18n("Removing these packages may break system safety. Aborting."))
                    self.finished()

    def showErrorMessage(self, message):
        self.possibleError = True
        KMessageBox.error(self,message,i18n("Error"))

    def finished(self, command=None):

        if command == "System.Manager.updateAllRepositories":
            pisi.api.finalize()
            pisi.api.init(write=False)
            self.showUpdateDialog()

        elif command == "System.Manager.updatePackage":
            self.updateDialog.refreshDialog()

        self.progressDialog.currentAppIndex = 1

        # Here we don't use updateListing() if there is no error, because we already updated the view
        # in check() using DOM which is fast, so unless an error occurred there is no need for a refresh
        if self.possibleError:
            self.updateListing()
            self.possibleError = False
        else:
            self.eventListener.packageList = []

        self.parent.operateAction.setEnabled(False)
        self.parent.basketAction.setEnabled(False)
        self.progressDialog.closeForced()
        self.progressDialog.reset()

    def installSingle(self):
        app = []
        app.append(str(self.listView.currentItem().text(0)))
        self.command.install(app)

    def searchStringChanged(self):
        if (self.timer.isActive()):
            self.timer.stop()
        self.timer.start(500, True)

    def searchPackage(self):
        query = self.searchLine.text()
        if not query.isEmpty():
            result = self.command.searchPackage(query)
            result = result.union(self.command.searchPackage(query,"en"))
            self.createSearchResults(result)
        else:
            self.updateListing()

    def clearSearchLine(self, updateListing=True):
        self.searchLine.clear()
        self.timer.stop()
        if updateListing:
            self.updateListing()

    def showPreferences(self):
        try:
            self.pref
        except AttributeError:
            self.pref = Preferences.Preferences(self)
        self.pref.show()

    def update(self):
        self.progressDialog.show()
        self.command.startUpdate()

    def showUpdateDialog(self):
        upgradables = pisi.api.list_upgradable()
        if not upgradables:
            KMessageBox.information(self,i18n("There are no updates available at this time"))
            return

        self.updateDialog = UpdateDialog.UpdateDialog(self, upgradables)
        self.updateDialog.show()

# TODO: move this to updatedialog
    def updatePackages(self):
        self.progressDialog.currentAppIndex = 0
        self.progressDialog.show()
        self.command.updatePackage(self.updateDialog.eventListener.packageList)

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
        return self.config.readBoolEntry("HideLibraries",True)

class MainApplication(KMainWindow):
    def __init__(self,parent=None,name=None):
        KMainWindow.__init__(self,parent,name)
        self.setCaption(i18n("Package Manager"))
        self.aboutus = KAboutApplication(self)
        self.helpWidget = None
        self.mainwidget = MainApplicationWidget(self)
        self.setCentralWidget(self.mainwidget)

        self.setupMenu()
        self.setupGUI(KMainWindow.ToolBar|KMainWindow.Keys|KMainWindow.StatusBar|KMainWindow.Save|KMainWindow.Create)
        self.toolBar().setIconText(KToolBar.IconTextRight)

    def setupMenu(self):
        fileMenu = QPopupMenu(self)
        settingsMenu = QPopupMenu(self)

        self.quitAction = KStdAction.quit(kapp.quit, self.actionCollection())
        self.settingsAction = KStdAction.preferences(self.mainwidget.showPreferences, self.actionCollection())
        self.showAction = KAction(i18n("Show Installed Packages"),"package",KShortcut.null(),self.mainwidget.switchListing,self.actionCollection(),"show_action")
        self.operateAction = KAction(i18n("Install Package(s)"),"ok",KShortcut.null(),self.mainwidget.takeAction,self.actionCollection(),"operate_action")
        self.upgradeAction = KAction(i18n("Check for updates"),"reload",KShortcut.null(),self.mainwidget.update ,self.actionCollection(),"upgrade_packages")
        self.basketAction = KAction(i18n("Show basket"),"basket",KShortcut.null(),self.mainwidget.showBasket ,self.actionCollection(),"show_basket")

        self.operateAction.setEnabled(False)
        self.basketAction.setEnabled(False)

        self.showAction.plug(fileMenu)
        self.operateAction.plug(fileMenu)
        self.quitAction.plug(fileMenu)
        self.settingsAction.plug(settingsMenu)

        self.menuBar().insertItem(i18n ("&File"), fileMenu,0,0)
        self.menuBar().insertItem(i18n("&Settings"), settingsMenu,1,1)

def main():
    global kapp
    global packageToInstall
    global showUpdates

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)
    KCmdLineArgs.addCmdLineOptions ([("install <package>", I18N_NOOP("Package to install")),("showupdates", I18N_NOOP("Show available updates"))])

    if not KUniqueApplication.start():
        print i18n("Package Manager is already running!")
        return

    kapp = KUniqueApplication(True, True, True)

    args = KCmdLineArgs.parsedArgs()
    if args.isSet("install"):
        packageToInstall = str(KIO.NetAccess.mostLocalURL(KURL(args.getOption("install")), None).path())
    else:
        packageToInstall = None

    if args.isSet("showupdates"):
        showUpdates = True
    else:
        showUpdates = None

    myapp = MainApplication()
    myapp.show()
    kapp.setMainWidget(myapp)

    sys.exit(kapp.exec_loop())

if __name__ == "__main__":
    main()

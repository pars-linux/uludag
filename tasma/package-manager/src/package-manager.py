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
import kdedesigner

# Local imports
import Progress
import Preferences
import Commander
import CustomEventListener
import BasketDialog

# Pisi
import pisi

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

description = I18N_NOOP("GUI for PiSi package manager")
version = "1.1.0_b4"
base_packages = set(['qt','kdelibs','kdebase','sip','PyQt','PyKDE'])
(install_state, remove_state, upgrade_state) = range(3)

def AboutData():
    global version,description

    about_data = KAboutData("package-manager", I18N_NOOP("Package Manager"), version, description, KAboutData.License_GPL,
                            "(C) 2005, 2006 UEKAE/TÜBİTAK", None, None)

    about_data.addAuthor("Faik Uygur", I18N_NOOP("Developer and Current Maintainer"), "faik@pardus.org.tr")
    about_data.addAuthor("İsmail Dönmez", I18N_NOOP("Original Author"), "ismail@pardus.org.tr")
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

class Basket:
    def __init__(self):
        self.packages = []

    def add(self, package):
        self.packages.append(str(package))

    def remove(self, package):
        self.packages.remove(str(package))

    def empty(self):
        self.packages = []

class Component:
    def __init__(self, name, packages, summary):
        self.name = name
        self.packages = packages
        self.summary = summary

    def remove(self, package):
        self.packages.remove(package)

class ComponentTipper(QToolTip):
    def __init__(self, parent):
        super(ComponentTipper, self).__init__(parent.listView.viewport())
        self.components = parent.componentDict
        self.list = parent.listView
        self.setWakeUpDelay(500)

    def maybeTip(self, point):
        item = self.list.itemAt(point)
        if item:
            component = self.components[item]
            self.tip(self.list.itemRect(item),
                     u"<b>%s</b> - %s" %
                     (component.name, component.summary))

class MainApplicationWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.progressDialog = Progress.Progress(self)

        self.initialRepoCheck = None
        self.componentDict = {}
        self.state = install_state
        self.basket = Basket()

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

        self.basketAction = KPushButton(self.rightTopLayout)
        self.basketAction.setText(i18n("Show basket"))
        self.basketAction.setIconSet(loadIconSet("package"))
        self.basketAction.setEnabled(False)

        self.operateAction = KPushButton(self.rightTopLayout)
        self.operateAction.setText(i18n("Install Package(s)"))
        self.operateAction.setIconSet(loadIconSet("ok"))
        self.operateAction.setEnabled(False)

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
        self.connect(self.basketAction,SIGNAL("clicked()"),self.showBasket)
        self.connect(self.operateAction,SIGNAL("clicked()"),self.takeAction)

        self.delayTimer = QTimer(self)
        self.connect(self.delayTimer, SIGNAL("timeout()"), self.lazyLoadComponentList)
        self.delayTimer.start(500, True)

        # inform user for the delay...
        item = KListViewItem(self.listView)
        item.setText(0,i18n("Loading Package List..."))
        self.listView.setSelected(self.listView.firstChild(),True)

        self.tipper = ComponentTipper(self)

        self.htmlPart.view().setFocus()
        self.show()

    def lazyLoadComponentList(self):
        self.command = Commander.Commander(self)
        self.initialCheck()
        self.createComponentList(self.command.listNewPackages())
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

    def resetState(self):
        self.basket.empty()
        self.basketAction.setEnabled(False)
        self.operateAction.setEnabled(False)
        self.clearSearchLine(False)
        self.parent.showNewAction.setChecked(False)
        self.parent.showInstalledAction.setChecked(False)
        self.parent.showUpgradeAction.setChecked(False)

    def installState(self):
        self.resetState()
        self.parent.showNewAction.setChecked(True)
        self.processEvents()
        packages = self.command.listNewPackages()
        self.createComponentList(packages)
        self.operateAction.setText(i18n("Install Package(s)"))
        self.operateAction.setIconSet(loadIconSet("ok"))
        self.state = install_state
        self.listView.setSelected(self.listView.firstChild(),True)

    def removeState(self):
        self.resetState()
        self.parent.showInstalledAction.setChecked(True)
        self.processEvents()
        packages = self.command.listPackages()
        self.createComponentList(packages)
        self.operateAction.setText(i18n("Remove Package(s)"))
        self.operateAction.setIconSet(loadIconSet("no"))
        self.state = remove_state
        self.listView.setSelected(self.listView.firstChild(),True)

    def upgradeState(self):
        upgradables = pisi.api.list_upgradable()
        self.createComponentList(upgradables, True)
        self.operateAction.setText(i18n("Upgrade Package(s)"))
        self.operateAction.setIconSet(loadIconSet("reload"))
        self.listView.setSelected(self.listView.firstChild(),True)

        if not upgradables and self.state != upgrade_state:
            KMessageBox.information(self,i18n("There are no updates available at this time"))

        self.state = upgrade_state

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

            size = 0L
            if not pisi.packagedb.ctx.installdb.is_installed(app):
                package = pisi.context.packagedb.get_package(app)
                size = package.packageSize
            else:
                package = pisi.context.packagedb.get_package(app, pisi.itembyrepodb.installed)
                size = package.installedSize

            desc = package.description
            summary = package.summary
            version = package.version
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
        if self.basket.packages:
            document = self.htmlPart.document()
            nodeList = document.getElementsByTagName(DOM.DOMString("input"))
            for i in range(0,nodeList.length()):
                element = DOM.HTMLInputElement(nodeList.item(i))
                if element.name().string() in self.basket.packages:
                    element.click()
        self.htmlPart.view().setUpdatesEnabled(True)

    def updateView(self,item=None):
        # basket may have been emptied from basket dialog
        if not self.basket.packages:
            self.basketAction.setEnabled(False)
            self.operateAction.setEnabled(False)

        try:
            if not item:
                item = self.listView.currentItem()
            self.createHTML(self.componentDict[item].packages)
        except:
            pass

    def updateButtons(self):
        if self.basket.packages:
            self.operateAction.setEnabled(True)
            self.basketAction.setEnabled(True)
        else:
            self.operateAction.setEnabled(False)
            self.basketAction.setEnabled(False)

    def showBasket(self):
        basketDialog = BasketDialog.BasketDialog(self, self.basket.packages, self.state)
        self.connect(basketDialog, SIGNAL("destroyed()"), self.updateView)
        basketDialog.show()

    def takeAction(self):
        self.progressDialog.show()

        if self.state == remove_state:
            self.command.remove(self.basket.packages)
        elif self.state == install_state:
            self.command.install(self.basket.packages)
        elif self.state == upgrade_state:
            self.command.updatePackage(self.basket.packages)

    def updateListing(self):
        if self.state == install_state:
            self.installState()
        elif self.state == remove_state:
            self.removeState()
        elif self.state == upgrade_state:
            self.upgradeState()

    def updateComponentList(self):
        item = self.listView.currentItem()
        component = self.componentDict[item]
        if component.packages:
            item.setText(0,u"%s (%s)" % (component.name, len(component.packages)))
        else:
            self.listView.takeItem(item)
            self.listView.setSelected(self.listView.firstChild(),True)

    def createComponentList(self, packages, allComponent=False):
        # Components
        self.listView.clear()
        self.componentDict.clear()

        componentNames = ["desktop.kde","desktop.gnome","desktop.freedesktop","applications.network","applications.multimedia",
                          "applications.games","applications.hardware","system.base","system.devel", "system.kernel.drivers",
                          "system.kernel.firmware"]
        components = [pisi.context.componentdb.get_component(x) for x in componentNames]
        componentPackages = []

        for component in components:
            component_packages = list(set(packages).intersection(component.packages))
            if len(component_packages):
                componentPackages += component.packages
                item = KListViewItem(self.listView)
                if component.localName:
                    name = component.localName
                else:
                    name = component.name

                item.setText(0,u"%s (%s)" % (name, len(component_packages)))
                item.setPixmap(0, KGlobal.iconLoader().loadIcon("package",KIcon.Desktop,KIcon.SizeMedium))
                self.componentDict[item] = Component(name, component_packages, component.summary)

        # Rest of the packages
        rest_packages = list(set(packages) - set(componentPackages))
        if rest_packages:
            item = KListViewItem(self.listView)
            name = i18n("Others")
            item.setText(0, u"%s (%s)" % (name, len(rest_packages)))
            item.setPixmap(0, KGlobal.iconLoader().loadIcon("package",KIcon.Desktop,KIcon.SizeMedium))
            self.componentDict[item] = Component(name, rest_packages, name)

        # All of the component's packages
        if allComponent:
            item = KListViewItem(self.listView)
            name = i18n("All")
            item.setText(0, u"%s (%s)" % (name, len(packages)))
            item.setPixmap(0, KGlobal.iconLoader().loadIcon("package",KIcon.Desktop,KIcon.SizeMedium))
            self.componentDict[item] = Component(name, packages, name)

    def createSearchResults(self, packages):
        self.listView.clear()
        item = KListViewItem(self.listView)
        item.setText(0,i18n("Search Results"))
        item.setPixmap(0, KGlobal.iconLoader().loadIcon("find",KIcon.Desktop,KIcon.SizeMedium))
        self.createHTML(packages)
        self.listView.setSelected(self.listView.firstChild(),True)

    def displayProgress(self, data):
        data = data.split(",")
        operation = data[0]

        if operation == "updatingrepo":
            self.progressDialog.setOperationDescription(i18n(str(data[2])))
            self.progressDialog.hideStatus()
            percent = data[1]
            self.progressDialog.updateProgressBar(percent)

        elif operation == "fetching":
            if "pisi-index.xml" in data[1]:
                self.progressDialog.updateUpgradingInfo(percent=data[2], rate=data[3], symbol=data[4])
            else:
                self.progressDialog.updateDownloadingInfo(i18n("downloading"), file=data[1], percent=data[2], rate=data[3], symbol=data[4])
                if self.state == install_state:
                    self.progressDialog.setCurrentOperation(i18n("<b>Installing Package(s)</b>"))
                elif self.state == upgrade_state:
                    self.progressDialog.setCurrentOperation(i18n("<b>Upgrading Package(s)</b>"))

    def pisiNotify(self,data):
        data = data.split(",")
        operation = data[0]

        if operation in ["removing"]:
            if self.state == remove_state:
                self.progressDialog.setCurrentOperation(i18n("<b>Removing Package(s)</b>"))
            elif self.state == upgrade_state:
                self.progressDialog.setCurrentOperation(i18n("<b>Upgrading Package(s)</b>"))

            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=data[1])

        elif operation in ["installing"]:
            if self.state == install_state:
                self.progressDialog.setCurrentOperation(i18n("<b>Installing Package(s)</b>"))
            elif self.state == upgrade_state:
                self.progressDialog.setCurrentOperation(i18n("<b>Upgrading Package(s)</b>"))

            self.progressDialog.packageNo += 1
            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=data[1])

        elif operation in ["extracting", "configuring"]:
            self.progressDialog.hideStatus()
            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=data[1])

        elif operation in ["removed"]:
            self.progressDialog.packageNo += 1

        elif operation in ["updatingrepo"]:
            self.progressDialog.setCurrentOperation(i18n("<b>Updating Repository</b>"))
            self.progressDialog.setOperationDescription(i18n('Downloading package list of %1').arg(data[1]))

        else: # pisi.ui.packagetogo
            # pisi sends unnecessary remove order notify in the middle of install, upgrade, remove
            if self.progressDialog.totalPackages == 1 and len(data) > 1:
                self.progressDialog.totalPackages = len(data)

            if self.state == remove_state:
                if len(base_packages.intersection(data)) > 0:
                    self.showErrorMessage(i18n("Removing these packages may break system safety. Aborting."))
                    self.finished()

    def showErrorMessage(self, message):
        KMessageBox.error(self,message,i18n("Error"))

    def finished(self, command=None):

        # this is pisi's lack of db locking mechanism usage fault.
        pisi.api.finalize()
        pisi.api.init(write=False)

        self.basket.empty()
        self.operateAction.setEnabled(False)
        self.basketAction.setEnabled(False)
        self.progressDialog.closeForced()
        self.progressDialog.reset()

        if command == "System.Manager.updateAllRepositories":
            self.upgradeState()

        elif command in ["System.Manager.updateAllRepositories",
                       "System.Manager.updatePackage",
                       "System.Manager.installPackage",
                       "System.Manager.removePackage"]:
            self.updateListing()

    def installSingle(self):
        app = []
        app.append(str(self.listView.currentItem().text(0)))
        self.command.install(app)

    def searchStringChanged(self):
        if (self.timer.isActive()):
            self.timer.stop()
        self.timer.start(300, True)

    def searchPackage(self):
        query = self.searchLine.text()
        if not query.isEmpty():
            result = self.searchPackageName(query)
            self.createSearchResults(result)
        else:
            self.updateListing()

    def searchPackageName(self, query):
        packages = []
        for key in self.componentDict.keys():
            if self.componentDict[key].name == i18n("All"):
                continue
            for package in self.componentDict[key].packages:
                if query in package:
                    packages.append(package)

        return packages

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

    def updateCheck(self):
        self.resetState()
        self.parent.showUpgradeAction.setChecked(True)
        self.processEvents()
        self.progressDialog.show()
        self.command.startUpdate()

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
        self.showInstalledAction = KToggleAction(i18n("Show Installed Packages"),"package",KShortcut.null(),self.mainwidget.removeState,self.actionCollection(),"show_installed_action")
        self.showNewAction = KToggleAction(i18n("Show New Packages"),"edit_add",KShortcut.null(),self.mainwidget.installState,self.actionCollection(),"show_new_action")
        self.showUpgradeAction = KToggleAction(i18n("Show Upgradable Packages"),"reload",KShortcut.null(),self.mainwidget.updateCheck ,self.actionCollection(),"show_upgradable_action")

        self.showNewAction.plug(fileMenu)
        self.showNewAction.setChecked(True)
        self.showInstalledAction.plug(fileMenu)
        self.showUpgradeAction.plug(fileMenu)
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

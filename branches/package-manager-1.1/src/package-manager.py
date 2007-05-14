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
import PmDcop

# Local imports
import Progress
import Preferences
import Commander
import CustomEventListener
import Basket
import BasketDialog
import Tray
import Settings
from Icons import *
import LocaleData
import HelpDialog
import PackageCache

# Pisi
import pisi

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

description = I18N_NOOP("GUI for PiSi package manager")
version = "1.1"
unremovable_packages = set(['qt','kdelibs','kdebase','sip','PyQt','PyKDE','pisi', 'package-manager'])
(install_state, remove_state, upgrade_state) = range(3)

def AboutData():
    global version,description

    about_data = KAboutData("package-manager", I18N_NOOP("Package Manager"), version, description, KAboutData.License_GPL,
                            "(C) 2005, 2006 UEKAE/TÜBİTAK", None, None)

    about_data.addAuthor("Faik Uygur", I18N_NOOP("Developer and Current Maintainer"), "faik@pardus.org.tr")
    about_data.addAuthor("İsmail Dönmez", I18N_NOOP("Original Author"), "ismail@pardus.org.tr")
    about_data.addAuthor("Gökmen Göksel",I18N_NOOP("CSS/JS Meister"), "gokmen@pardus.org.tr")
    about_data.addAuthor("Görkem Çetin",I18N_NOOP("GUI Design & Usability"), "gorkem@pardus.org.tr")
    about_data.addCredit(I18N_NOOP("PiSi Authors"), I18N_NOOP("Authors of PiSi API"), "pisi@pardus.org.tr")
    return about_data

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

        self.componentDict = {}
        self.lastSelectedComponent = None
        self.command = None
        self.state = install_state
        self.basket = Basket.Basket()
        self.packageCache = PackageCache.PackageCache()

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

        self.connect(self.listView,SIGNAL("selectionChanged(QListViewItem *)"),self.refreshComponentList)
        self.connect(self.htmlPart,SIGNAL("completed()"),self.registerEventListener)
        self.connect(self.searchLine,SIGNAL("textChanged(const QString&)"),self.searchStringChanged)
        self.connect(self.timer, SIGNAL("timeout()"), self.searchPackage)
        self.connect(self.clearButton,SIGNAL("clicked()"),self.searchLine, SLOT("clear()"))
        self.connect(self.basketAction,SIGNAL("clicked()"),self.showBasket)
        self.connect(self.operateAction,SIGNAL("clicked()"),self.takeAction)

        self.command = Commander.Commander(self)

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

        self.settings = Settings.Settings(kapp.config())

    def lazyLoadComponentList(self):
        # pisi should now be ready for tray to get upgrades info
        self.parent.tray.updateTrayIcon()
 
        if self.componentsReady():
            self.installState()

            global packageToInstall
            if packageToInstall:
                self.installPackage(packageToInstall)
                self.progressDialog.show()
                # KWin forces to raise it even though the parent is hidden, QWidget does not.
                KWin.raiseWindow(self.progressDialog.winId())
        else:
            self.updateCheck()

    def processEvents(self):
        global kapp
        kapp.processEvents(QEventLoop.ExcludeUserInput)

    def componentsReady(self):
        if not pisi.context.componentdb.list_components(): # Repo metadata empty
            return False

        return True

    def repoNotReady(self):
        KMessageBox.error(self, i18n("Package-manager needs to update package database. You need a network connection to update."),
                          i18n("Package database is empty"))

    def resetState(self):
        self.basket.empty()
        self.basketAction.setEnabled(False)
        self.operateAction.setEnabled(False)
        self.searchLine.clear()
        self.packageCache.clearCache()
        self.parent.showNewAction.setChecked(False)
        self.parent.showInstalledAction.setChecked(False)
        self.parent.showUpgradeAction.setEnabled(True)
        self.parent.showUpgradeAction.setChecked(False)

    def installState(self, reset=True):
        kapp.setOverrideCursor(Qt.waitCursor)
        if reset:
            self.resetState()
        self.parent.showNewAction.setChecked(True)
        self.processEvents()
        packages = self.command.listNewPackages()
        self.state = install_state
        self.createComponentList(packages)
        self.operateAction.setText(i18n("Install Package(s)"))
        self.operateAction.setIconSet(loadIconSet("ok"))
        self.basket.setState(self.state)
        self.setLastSelected()
        self.updateStatusBar()
        kapp.restoreOverrideCursor()

    def removeState(self, reset=True):
        kapp.setOverrideCursor(Qt.waitCursor)
        if reset:
            self.resetState()
        self.parent.showInstalledAction.setChecked(True)
        self.processEvents()
        packages = self.command.listPackages()
        self.state = remove_state
        self.createComponentList(packages)
        self.operateAction.setText(i18n("Remove Package(s)"))
        self.operateAction.setIconSet(loadIconSet("no"))
        self.basket.setState(self.state)
        self.setLastSelected()
        self.updateStatusBar()
        kapp.restoreOverrideCursor()

    def upgradeState(self):
        kapp.setOverrideCursor(Qt.waitCursor)

        # TODO:
        # If package-manager is opened while tray is updating-repo; progress dialog is
        # shown. And when it ends, pm switches to upgradeState but without checking
        # operation buttons. If pm is not opened while this is done, no change state happens
        # in pm, and when it is opened it will be seen in which state it was left.
        #
        # Later this background update may be done with a widget like kmail's small progress 
        # and any operation button will be disabled when tray is caught while updating. For 
        # now we show progress dialog and change pm state and button states manually.
        self.parent.showUpgradeAction.setChecked(True)
        self.parent.showNewAction.setChecked(False)
        self.parent.showInstalledAction.setChecked(False)
        ##

        self.packageCache.clearCache()
        upgradables = pisi.api.list_upgradable()
        self.createComponentList(upgradables, True)
        self.operateAction.setText(i18n("Upgrade Package(s)"))
        self.operateAction.setIconSet(loadIconSet("reload"))
        self.lastSelectedComponent = i18n("All")
        self.setLastSelected()

        self.basket.setState(self.state)
        self.updateStatusBar()
        kapp.restoreOverrideCursor()

    def createHTML(self,packages,part=None):
        head =  '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        '''

        if not part:
            part = self.htmlPart

        kapp.setOverrideCursor(Qt.waitCursor)
        part.view().setContentsPos(0, 0)
        part.begin()
        part.write(head)
        part.write("<style type=\"text/css\">%s</style>" % self.css)
        part.write("<script language=\"JavaScript\">%s</script>" % self.javascript)
        part.write("</head><body>")

        if set(packages) - set(self.basket.packages):
            part.write('''<font size="-2"><a href="#selectall">'''+i18n("Select all packages in this category")+'''</a></font>''')
        else:
            part.write('''<font size="-2"><a href="#selectall">'''+i18n("Reverse package selections")+'''</a></font>''')

        part.write(self.createHTMLForPackages(packages))
        part.end()
        kapp.restoreOverrideCursor()

    def createHTMLForPackages(self,packages):
        result = ''
        template ='''
        <!-- package start -->
        <div>
        <!-- checkbox --> %s <!-- checkbox -->
        <div class="package_title" style="%s" id="package_t%d" onclick="showHideContent(this)">
        <img src="%s" style="float:left;" width="%dpx" height="%dpx">
        <b>%s</b><br><span style="color:#303030">%s</span><br>
        </div>
        <div class="package_info" style="%s" id="package_i%d">
        <div style="margin-left:25px;" class="package_info_content" id="package_ic%d">
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
        titleStyle = ''
        style = ''
        packages.sort(key=string.lower)

        for app in packages:
            if index % 2 == 0:
                style = "background-color:%s" % KGlobalSettings.alternateBackgroundColor().name()
            else:
                style = "background-color:%s" % KGlobalSettings.baseColor().name()
            titleStyle = style

            size = 0L
            if self.state == remove_state:
                package = pisi.context.packagedb.get_package(app, pisi.itembyrepodb.installed)
                size = package.installedSize
            else:
                package = pisi.context.packagedb.get_package(app)
                size = package.packageSize

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

            if app in self.basket.packages:
                titleStyle = "background-color:#678DB2"
                checkState = "checked"
            else:
                checkState = ""

            curindex = index+1
            if self.state == remove_state and app in unremovable_packages:
                checkbox = """<div class="checkboks" style="%s" id="checkboks_t%d"><input type="checkbox" \
                           disabled %s name="%s id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app,curindex)
            else:
                checkbox = """<div class="checkboks" style="%s" id="checkboks_t%d"><input type="checkbox" \
                           %s onclick="changeBackgroundColor(this)" name="%s" id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app,curindex)
            
            iconSize = getIconSize()
            result += template % (checkbox, titleStyle,curindex,iconPath,iconSize,iconSize,app,summary,style,curindex,curindex,
                                  i18n("Description: "),desc,i18n("Version: "),
                                  version,i18n("Package Size: "),size,i18n("Homepage: "),
                                  homepage,homepage)
            index += 1

        return result

    def registerEventListener(self):
        self.eventListener = CustomEventListener.CustomEventListener(self)
        node = self.htmlPart.document().getElementsByTagName(DOM.DOMString("body")).item(0)
        node.addEventListener(DOM.DOMString("click"),self.eventListener,True)

    def setLastSelected(self):
        item = self.listView.firstChild()

        # FIXME: a quick and ugly hack to see if we are in search state.
        if item.text(0) == i18n("Search Results"):
            return item

        for i in self.componentDict.keys():
            if self.componentDict[i].name == self.lastSelectedComponent:
                item = i
                break

        self.listView.setSelected(item, True)
        return item

    def refreshComponentList(self, item):
        kapp.setOverrideCursor(Qt.waitCursor)
        try:
            self.createHTML(self.componentDict[item].packages)
            self.lastSelectedComponent = self.componentDict[item].name
        # initialization and search state listview items are not components
        except KeyError:
            pass
        kapp.restoreOverrideCursor()

    def updateStatusBar(self):
        def humanReadableSize(size):
            tpl = pisi.util.human_readable_size(size)
            if tpl[0] == 0:
                return "0 B"
            return "%.1f %s" % (tpl[0], tpl[1])

        kapp.setOverrideCursor(Qt.waitCursor)
        self.basket.update()
        kapp.restoreOverrideCursor()

        if not self.basket.packages:
            text = i18n("Currently your basket is empty.")

        elif self.state == install_state or self.state == upgrade_state:
            text = i18n("Currently there are <b>%1</b> selected package(s) of total <b>%2</b> of size ").arg(len(self.basket.packages)).arg(humanReadableSize(self.basket.packagesSize))

            if self.basket.extraPackages:
                text += i18n("with <b>%3</b> extra dependencies of total <b>%4</b> of size ").arg(len(self.basket.extraPackages)).arg(humanReadableSize(self.basket.extraPackagesSize))

            text += i18n("in your basket.")

        elif self.state == remove_state:
            text = i18n("Currently there are <b>%1</b> selected package(s) of total <b>%2</b> of size ").arg(len(self.basket.packages)).arg(humanReadableSize(self.basket.packagesSize))

            if self.basket.extraPackages:
                text += i18n("with <b>%3</b> reverse dependencies of total <b>%4</b> of size ").arg(len(self.basket.extraPackages)).arg(humanReadableSize(self.basket.extraPackagesSize))

            text += i18n("in your basket.")

        self.parent.updateStatusBarText(text)

    def updateButtons(self):
        if self.basket.packages:
            self.operateAction.setEnabled(True)
            self.basketAction.setEnabled(True)
        else:
            self.operateAction.setEnabled(False)
            self.basketAction.setEnabled(False)

    def showBasket(self):
        basketDialog = BasketDialog.BasketDialog(self, self.basket)
        action = basketDialog.exec_loop()
        self.processEvents()

        if action == BasketDialog.APPLY_OPERATION:
            self.takeAction()

        self.updateButtons()
        self.refreshComponentList(self.setLastSelected())
        basketDialog.deleteLater()

    def conflictCheckPass(self):
        (C, D, pkg_conflicts) = self.command.checkConflicts(self.basket.packages + self.basket.extraPackages)

        conflicts_within = list(D)
        if conflicts_within:
            msg = i18n("Selected packages [%1] are in conflict with each other. These packages can not be installed together.").arg(", ".join(conflicts_within))
            self.showErrorMessage(msg, i18n("Conflict Error"))
            self.searchLine.clear()
            self.refreshState(False)
            return False

        if pkg_conflicts:
            msg = i18n("The following packages conflicts:\n")
            for pkg in pkg_conflicts.keys():
                msg += i18n("%1 conflicts with: [%2]\n").arg(pkg).arg(", ".join(pkg_conflicts[pkg]))
            msg += i18n("\nRemove the following conflicting packages?")
            if self.showConfirmMessage(msg, i18n("Conflict Error")) == KMessageBox.No:
                self.searchLine.clear()
                self.refreshState(False)
                return False

        return True

    def installPackage(self, package):
        self.progressDialog.hideStatus(True)
        self.progressDialog.updateProgressBar(100)

        if not self.command.inProgress():
            self.progressDialog.totalPackages = 1
            self.command.install([package])
            self.progressDialog.setCurrentOperation(i18n("<b>Installing Package(s)</b>"))
            self.progressDialog.show()
            # KWin forces to raise it even though the parent is hidden, QWidget does not.
            KWin.raiseWindow(self.progressDialog.winId())


    def confirmAction(self):

        message = None
        if self.state == install_state:
            message = QString(i18n("<qt>You have selected <b>%1</b> package(s) to be <b>installed</b>.")).arg(len(self.basket.packages))

            if self.basket.extraPackages:
                message += QString(i18n(" With the selected packages; <b>%1</b> extra dependencies are also going to be <b>installed</b>.")).arg(len(self.basket.extraPackages))
                message += QString(i18n("<br><br>Total of <b>%1</b> packages are going to be <b>installed</b>.")).arg(len(self.basket.packages) + len(self.basket.extraPackages))

        elif self.state == upgrade_state:
            message = i18n("<qt>You have selected <b>%1</b> package(s) to be <b>upgraded</b>.").arg(len(self.basket.packages))

            if self.basket.extraPackages:
                message += i18n(" With the selected packages; <b>%1</b> extra dependencies are also going to be <b>upgraded</b>.").arg(len(self.basket.extraPackages))
                message += i18n("<br><br>Total of <b>%1</b> packages are going to be <b>upgraded</b>.").arg(len(self.basket.packages) + len(self.basket.extraPackages))

        elif self.state == remove_state:
            message = i18n("<qt>You have selected <b>%1</b> package(s) to be <b>removed</b>.").arg(len(self.basket.packages))

            if self.basket.extraPackages:
                message += i18n(" Selected packages have reverse dependencies. Because the reverse dependencies of the selected packages needs those packages to work; by removing the selected packages; <b>%1</b> reverse dependencies are also going to be <b>removed</b>. Please check your basket and make sure those are the packages you want to remove. Accidentally removing some reverse dependencies may break the system stability.").arg(len(self.basket.extraPackages))

                message += i18n("<br><br>Total of <b>%1</b> packages are going to be <b>removed</b>.").arg(len(self.basket.packages) + len(self.basket.extraPackages))

        message += i18n("<br>Do you want to continue?</qt>")

        if KMessageBox.Yes == KMessageBox.warningYesNo(self, 
                                                       message,
                                                       i18n("Warning"),
                                                       KGuiItem(i18n("Continue"), "ok"),
                                                       KGuiItem(i18n("Cancel"), "no"),
                                                       ):
            return True

        return False

    def takeAction(self):

        if not self.confirmAction():
            return

        self.progressDialog.totalPackages = len(self.basket.packages + self.basket.extraPackages)

        # remove action
        if self.state == remove_state:
            self.command.remove(self.basket.packages)
            self.progressDialog.setCurrentOperation(i18n("<b>Removing Package(s)</b>"))
            self.progressDialog.hideStatus()

        # install action
        elif self.state == install_state:
            if not self.conflictCheckPass():
                return

            self.progressDialog.setCurrentOperation(i18n("<b>Installing Package(s)</b>"))
            self.progressDialog.showStatus()
            self.command.install(self.basket.packages)

        # upgrade action
        elif self.state == upgrade_state:
            if not self.conflictCheckPass():
                return

            self.progressDialog.setCurrentOperation(i18n("<b>Upgrading Package(s)</b>"))
            self.progressDialog.showStatus()
            self.command.updatePackage(self.basket.packages)

        if not self.parent.isHidden():
            self.progressDialog.show()

    def refreshState(self, reset=True):

        if self.settings.getBoolValue(Settings.general, "SystemTray"):
            self.parent.tray.show()
        elif not self.settings.getBoolValue(Settings.general, "SystemTray"):
            self.parent.tray.hide()

        if self.state == install_state:
            self.installState(reset)
        elif self.state == remove_state:
            self.removeState(reset)
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

        def appGuiFilter(pkg_name):
            if self.state == remove_state:
                package = pisi.context.packagedb.get_package(pkg_name, pisi.itembyrepodb.installed)
                return "app:gui" in package.isA
            elif self.state == install_state:
                package = pisi.context.packagedb.get_package(pkg_name)
                return "app:gui" in package.isA

        # Components
        self.listView.clear()
        self.componentDict.clear()

        if self.packageCache.isEmpty() and packages:
            if self.state == remove_state:
                self.packageCache.populateCache(packages, pisi.itembyrepodb.installed)
            else:
                self.packageCache.populateCache(packages, None)

        cdb = pisi.context.componentdb
        componentNames = [cname for cname in cdb.list_components() if cdb.get_component(cname).visibleTo == 'user']

        showOnlyGuiApp = self.settings.getBoolValue(Settings.general, "ShowOnlyGuiApp")

        componentPackages = []
        for componentName in componentNames:
            try:
                component = pisi.context.componentdb.get_union_comp(componentName)
            except pisi.component.Error:
                continue

            compPkgs = pisi.context.componentdb.get_union_packages(componentName, walk=True)
            component_packages = list(set(packages).intersection(compPkgs))
            componentPackages += component_packages

            if self.state != upgrade_state and showOnlyGuiApp:
                    component_packages = filter(appGuiFilter, component_packages)

            if len(component_packages):
                item = KListViewItem(self.listView)
                if component.localName:
                    name = component.localName
                else:
                    name = component.name

                if component.icon:
                    icon = component.icon
                else:
                    icon = "package"

                item.setText(0,u"%s (%s)" % (name, len(component_packages)))
                item.setPixmap(0, KGlobal.iconLoader().loadIcon(icon, KIcon.Desktop,KIcon.SizeMedium))
                self.componentDict[item] = Component(name, component_packages, component.summary)

        # Rest of the packages
        rest_packages = list(set(packages) - set(componentPackages))
        if self.state != upgrade_state and showOnlyGuiApp:
            rest_packages = filter(appGuiFilter, rest_packages)
        if rest_packages:
            item = KListViewItem(self.listView)
            name = i18n("Others")
            item.setText(0, u"%s (%s)" % (name, len(rest_packages)))
            item.setPixmap(0, KGlobal.iconLoader().loadIcon("package_applications",KIcon.Desktop,KIcon.SizeMedium))
            self.componentDict[item] = Component(name, rest_packages, name)

        # All of the component's packages
        if allComponent:
            item = KListViewItem(self.listView)
            name = i18n("All")
            item.setText(0, u"%s (%s)" % (name, len(packages)))
            item.setPixmap(0, KGlobal.iconLoader().loadIcon("package_network",KIcon.Desktop,KIcon.SizeMedium))
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

        if operation in ["updatingrepo", "rebuilding-db"]:
            self.progressDialog.setOperationDescription(i18n(str(data[2])))
            percent = data[1]
            self.progressDialog.updateProgressBar(percent)

        elif operation == "fetching":
            if "pisi-index.xml" in data[1]:
                self.progressDialog.updateUpgradingInfo()
                self.progressDialog.updateProgressBar(progress=data[2])

            else:
                if self.state == install_state:
                    self.progressDialog.setCurrentOperation(i18n("<b>Installing Package(s)</b>"))
                elif self.state == upgrade_state:
                    self.progressDialog.setCurrentOperation(i18n("<b>Upgrading Package(s)</b>"))

                self.progressDialog.updateDownloadingInfo(i18n("downloading"), file=data[1])
                self.progressDialog.updateTotalDownloaded(pkgDownSize=data[5], pkgTotalSize=data[6])
                self.progressDialog.updateTotalOperationPercent()

    def pisiNotify(self,data):
        data = data.split(",")
        operation = data[0]

        # operation is now cancellable
        if operation in ["started"]:
            self.progressDialog.enableCancel()

        elif operation in ["removing"]:
            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=data[1])
            self.progressDialog.updatePackageInfo()

        elif operation in ["cached"]:
            # progressDialog.totalSize is the to be downloaded size by package-manager.
            # And that is (totalDownloadSize - alreadyCachedSize) 
            self.progressDialog.totalSize = int(data[1]) - int(data[2])
            self.progressDialog.updateTotalOperationPercent()
            self.progressDialog.updateStatus()
            
        elif operation in ["installing"]:
            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=data[1])
            self.progressDialog.updatePackageInfo()

        elif operation in ["extracting", "configuring"]:
            self.progressDialog.updateOperationDescription(i18n(str(operation)), package=data[1])

        elif operation in ["removed", "installed", "upgraded"]:
            # Bug 4030
            if self.state != remove_state and operation == "removed":
                return

            self.progressDialog.packageNo += 1
            self.progressDialog.updatePackageInfo()

            # installed does not affect progress because the real progress is the "download" in install state
            if operation != "installed":
                self.progressDialog.updatePackageProgress()

        elif operation in ["savingrepos"]:
            self.progressDialog.setCurrentOperation(i18n("<b>Applying Repository Changes</b>"))

        elif operation in ["updatingrepo"]:
            self.progressDialog.setCurrentOperation(i18n("<b>Updating Repository</b>"))
            self.progressDialog.setOperationDescription(i18n('Downloading package list of %1').arg(data[1]))

    def showErrorMessage(self, message, error=i18n("Error")):
        KMessageBox.error(self, message, error)

    def showConfirmMessage(self, message, error=i18n("Confirm")):
        return KMessageBox.questionYesNo(self, message, error)

    def reloadPisi(self):
        for module in sys.modules.keys():
            if module.startswith("pisi."):
                """removal from sys.modules forces reload via import"""
                del sys.modules[module]

        reload(pisi)

    def finished(self, command=None):
 
        pisi.api.finalize()

        # when pisi db version is upgraded, reload is needed before init
        packages = self.basket.packages + self.basket.extraPackages
        if command == "System.Manager.updatePackage" and "pisi" in packages:
            self.reloadPisi()
        
        pisi.api.init(write=False)

        # after every operation check package cache limits
        if command not in ["System.Manager.clearCache", 
                           "System.Manager.setRepositories"]:
            self.command.checkCacheLimits()

        self.basket.empty()
        self.operateAction.setEnabled(False)
        self.basketAction.setEnabled(False)
        self.parent.showUpgradeAction.setEnabled(True)

        self.progressDialog.closeForced()
        self.progressDialog.reset()

        if command in ["System.Manager.updateAllRepositories",
                       "System.Manager.updateRepository"]:
            self.refreshState()

            if self.parent.isHidden():
                self.parent.tray.showPopup()

        elif command == "System.Manager.setRepositories":
            self.updateCheck()

        elif command in ["System.Manager.updatePackage",
                         "System.Manager.installPackage",
                         "System.Manager.removePackage",
                         "System.Manager.cancelled"]:
            self.refreshState()

        self.parent.tray.updateTrayIcon()

    def searchStringChanged(self):
        if (self.timer.isActive()):
            self.timer.stop()
        self.timer.start(500, True)

    def searchPackage(self):
        query = unicode(self.searchLine.text())
        if query:
            import time
            start = time.time()
            result = self.packageCache.searchInPackages(query.split())
            finish = time.time()
            print finish - start
            self.createSearchResults(result)
            finish = time.time()
            print finish - start
        else:
            self.timer.stop()
            self.refreshState(reset=False)

    def showPreferences(self):
        try:
            self.pref
        except AttributeError:
            self.pref = Preferences.Preferences(self)
        self.pref.show()

    def show(self):
        QWidget.show(self)
        if self.command and self.command.inProgress():
            self.progressDialog.show()

    def updateCheck(self):
        self.resetState()
        self.state = upgrade_state
        self.parent.showUpgradeAction.setChecked(True)
        self.parent.showUpgradeAction.setEnabled(False)
        self.processEvents()
        self.progressDialog.hideStatus(True)
        self.progressDialog.setCurrentOperation(i18n("<b>Updating Repository</b>"))
        self.progressDialog.show()
        self.command.startUpdate()

    def trayUpdateCheck(self, repo = None, forced = False):
        # timer interval check should not be run if package-manager is not hidden.
        if not forced and not self.parent.isHidden():
            return

        self.parent.showUpgradeAction.setEnabled(False)
        self.processEvents()
        self.progressDialog.hideStatus(True)

        id = 0
        if not forced:
            id = Tray.ID_TRAY_INTERVAL_CHECK
            
        self.command.startUpdate(repo, id)
        # update repo command is given by the user
        if forced and not self.parent.isHidden():
            self.progressDialog.show()

    def trayUpgradeSwitch(self):
        self.resetState()
        self.state = upgrade_state
        self.upgradeState()
        self.processEvents()

class MainApplication(KMainWindow):
    def __init__(self,parent=None,name=None):
        KMainWindow.__init__(self,parent,name)
        self.statusLabel = QLabel("", self.statusBar())
        self.statusBar().addWidget(self.statusLabel)
        self.statusBar().setSizeGripEnabled(True)
        self.setCaption(i18n("Package Manager"))
        self.aboutus = KAboutApplication(self)
        self.helpWidget = None
        self.mainwidget = MainApplicationWidget(self)
        self.setCentralWidget(self.mainwidget)

        self.setupMenu()
        self.setupGUI(KMainWindow.ToolBar|KMainWindow.Keys|KMainWindow.StatusBar|KMainWindow.Save|KMainWindow.Create)
        self.fixHelpMenu()
        self.toolBar().setIconText(KToolBar.IconTextRight)
        self.tray = Tray.Tray(self)
        self.dcop = PmDcop.PmDcop(self)

        self.connect(self.tray, SIGNAL("quitSelected()"), self.slotQuit)
        self.connect(kapp, SIGNAL("shutDown()"), self.slotQuit)

        if self.mainwidget.settings.getBoolValue(Settings.general, "SystemTray"):
            if self.mainwidget.settings.getBoolValue(Settings.general, "UpdateCheck"):
                interval = self.mainwidget.settings.getNumValue(Settings.general, "UpdateCheckInterval")
                self.tray.updateInterval(interval)

            self.tray.show()

    def updateStatusBarText(self, text):
        self.statusLabel.setText(text)
        self.statusLabel.setAlignment(Qt.AlignHCenter)

    def closeEvent(self, closeEvent):
        if self.mainwidget.settings.getBoolValue(Settings.general, "SystemTray"):
            self.hide()
        else:
            self.slotQuit()

    def slotQuit(self):
        pisi.api.finalize()

        # Don't know why but without this, after exiting package-manager, crash occurs. This may be a workaround 
        # or a PyQt bug.
        self.mainwidget.deleteLater()
        kapp.quit()

    def setupMenu(self):
        fileMenu = QPopupMenu(self)
        settingsMenu = QPopupMenu(self)

        self.quitAction = KStdAction.quit(self.slotQuit, self.actionCollection())
        self.settingsAction = KStdAction.preferences(self.mainwidget.showPreferences, self.actionCollection())

        self.showInstalledAction = KToggleAction(i18n("Show Installed Packages"),"package",KShortcut.null(),
                                                 self.mainwidget.removeState,self.actionCollection(),
                                                 "show_installed_action")
        self.showNewAction = KToggleAction(i18n("Show New Packages"),"edit_add",KShortcut.null(),
                                           self.mainwidget.installState,self.actionCollection(),"show_new_action")
        self.showUpgradeAction = KToggleAction(i18n("Show Upgradable Packages"),"reload",KShortcut.null(),
                                               self.mainwidget.updateCheck ,self.actionCollection(),"show_upgradable_action")

        self.showNewAction.plug(fileMenu)
        self.showNewAction.setChecked(True)
        self.showInstalledAction.plug(fileMenu)
        self.showUpgradeAction.plug(fileMenu)
        self.quitAction.plug(fileMenu)
        self.settingsAction.plug(settingsMenu)
        self.setHelpMenuEnabled(False)

        self.menuBar().insertItem(i18n ("&File"), fileMenu,0,0)
        self.menuBar().insertItem(i18n("&Settings"), settingsMenu,1,1)

    def showHelp(self):
        helpwin = HelpDialog.HelpDialog(self, HelpDialog.MAINAPP)
        helpwin.show()

    def fixHelpMenu(self):
        helpMenu = self.helpMenu()
        helpMenu.removeItem(KHelpMenu.menuHelpContents)
        helpMenu.insertItem(i18n("Package Manager Help"),
                            KHelpMenu.menuHelpContents,
                            0)
        helpMenu.setAccel(Qt.Key_F1, KHelpMenu.menuHelpContents)
        helpMenu.connectItem(KHelpMenu.menuHelpContents, self.showHelp)
        self.menuBar().insertItem(i18n("&Help"), helpMenu)

def main():
    global kapp
    global packageToInstall

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)
    KCmdLineArgs.addCmdLineOptions ([("install <package>", I18N_NOOP("Package to install")), ("show-mainwindow", I18N_NOOP("Show main window on startup"))])

    if not KUniqueApplication.start():
        print i18n("Package Manager is already running!")
        return

    kapp = KUniqueApplication(True, True, True)

    args = KCmdLineArgs.parsedArgs()
    if args.isSet("install"):
        packageToInstall = str(KIO.NetAccess.mostLocalURL(KURL(args.getOption("install")), None).path())
    else:
        packageToInstall = None

    myapp = MainApplication()
    if not myapp.mainwidget.settings.getBoolValue(Settings.general, "SystemTray"):
        myapp.show()
    else:
        if args.isSet("show-mainwindow"):
            myapp.show()

    kapp.setMainWidget(myapp)

    LocaleData.setSystemLocale()

    sys.exit(kapp.exec_loop())

if __name__ == "__main__":
    main()

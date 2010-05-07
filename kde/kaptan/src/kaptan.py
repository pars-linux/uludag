#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs, KConfig

import gui, subprocess, os, dbus

from gui.kaptanMain import Ui_kaptanUI
import gui.ScrWelcome as welcomeWidget
import gui.ScrMouse as mouseWidget
import gui.ScrNetwork as networkWidget
import gui.ScrWallpaper  as wallpaperWidget
import gui.ScrGoodbye  as goodbyeWidget
import gui.ScrStyle  as styleWidget
import gui.ScrMenu  as menuWidget
import gui.ScrSearch  as searchWidget
import gui.ScrSummary  as summaryWidget
import gui.ScrKeyboard  as keyboardWidget
import gui.ScrPackage as packageWidget
import gui.ScrSmolt as smoltWidget

import gui.tools as tools

def loadFile(_file):
    try:
        f = file(_file)
        d = [a.strip() for a in f]
        d = (x for x in d if x and x[0] != "#")
        f.close()
        return d
    except:
        return []

def profileSended():
    ''' Do not show smolt screen if profile was already sended.'''
    file = open("/etc/smolt/pub-uuid-smolt.pardus.org.tr", 'r')

    if file.read() != '':
        return True

    return False

if tools.isLiveCD():
    availableScreens = [welcomeWidget, keyboardWidget, mouseWidget, styleWidget, menuWidget, wallpaperWidget, networkWidget, smoltWidget, summaryWidget, goodbyeWidget]
elif profileSended():
    availableScreens = [welcomeWidget, mouseWidget, styleWidget, menuWidget, wallpaperWidget, searchWidget, networkWidget, packageWidget, summaryWidget, goodbyeWidget]
else:
    availableScreens = [welcomeWidget, mouseWidget, styleWidget, menuWidget, wallpaperWidget, searchWidget, networkWidget, smoltWidget, packageWidget, summaryWidget, goodbyeWidget]

class Kaptan(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_kaptanUI()

        self.ui.setupUi(self)
        self.screens = availableScreens
        self.screenData = None
        self.moveInc = 1
        self.menuText = ""
        self.config = KConfig("kaptanrc")

        # Add screens to StackWidget
        self.createWidgets(self.screens)

        self.screenId = []
        for screen in self.screens:
            title = screen.Widget.title.toString()
            desc = screen.Widget.desc.toString()
            self.screenId.append(title)

            if self.screens.index(screen) == 0:
                self.menuText += self.putBold(title)
                self.ui.screenTitle.setText(desc)
            else:
                self.menuText += self.putBr(title)

        self.ui.labelMenu.setText(self.menuText)

        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        QtCore.QObject.connect(self.ui.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        QtCore.QObject.connect(self.ui.buttonFinish, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.ui.buttonCancel, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))

    def slotFinished(self):
        if wallpaperWidget.Widget.selectedWallpaper:
            config =  KConfig("plasma-desktop-appletsrc")
            group = config.group("Containments")
            for each in list(group.groupList()):
                subgroup = group.group(each)
                subcomponent = subgroup.readEntry('plugin')
                if subcomponent == 'desktop' or subcomponent == 'folderview':
                    subg = subgroup.group('Wallpaper')
                    subg_2 = subg.group('image')
                    subg_2.writeEntry("wallpaper", wallpaperWidget.Widget.selectedWallpaper)
            self.killPlasma()
            QtGui.qApp.quit()
        else:
            QtGui.qApp.quit()

    def killPlasma(self):
        p = subprocess.Popen(["pidof", "-s", "plasma-desktop"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        pidOfPlasma = int(out)

        try:
            os.kill(pidOfPlasma, 15)
            self.startPlasma()
        except OSError, e:
            print 'WARNING: failed os.kill: %s' % e
            print "Trying SIGKILL"
            os.kill(pidOfPlasma, 9)
            self.startPlasma()

    def startPlasma(self):
        p = subprocess.Popen(["plasma-desktop"], stdout=subprocess.PIPE)

    # returns the id of current stack
    def getCur(self, d):
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    # move to id numbered step
    def setCurrent(self, id=None):
        if id:
            self.stackMove(id)

    def getNextWidgetDesc(self, id):
        self.ui.mainStack.setCurrentIndex(id+1)
        print dir(self.ui.mainStack)
        desc = self.ui.mainStack.currentWidget().desc.toString()
        self.ui.mainStack.setCurrentIndex(id)
        return desc

    def getPreviousWidgetDesc(self, id):
        self.ui.mainStack.setCurrentIndex(id-1)
        print dir(self.ui.mainStack)
        desc = self.ui.mainStack.currentWidget().desc.toString()
        self.ui.mainStack.setCurrentIndex(id)
        return desc

    # execute next step
    def slotNext(self,dryRun=False):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex() + 1

        for each in self.screenId:
            i = self.screenId.index(each)
            if  curIndex < len(self.screenId):
                if i == curIndex:
                    self.menuText += self.putBold(self.screenId[i])

                    # Set screen title
                    self.ui.screenTitle.setText(self.getNextWidgetDesc(i))
                else:
                    self.menuText += self.putBr(self.screenId[i])

        self.ui.labelMenu.setText(self.menuText)
        _w = self.ui.mainStack.currentWidget()

        ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1

    # execute previous step
    def slotBack(self):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex()
        for each in self.screenId:
            i = self.screenId.index(each)
            if i <= len(self.screenId) and not i == 0:
                if i == curIndex:
                    self.menuText += self.putBold(self.screenId[i -1])

                    # Set screen title
                    self.ui.screenTitle.setText(self.getPreviousWidgetDesc(i))
                else:
                    self.menuText += self.putBr(self.screenId[i -1])

        self.menuText += self.putBr(self.screenId[-1])
        self.ui.labelMenu.setText(self.menuText)

        _w = self.ui.mainStack.currentWidget()
        # Set screen title
        self.ui.screenTitle.setText(_w.desc.toString())

        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    def putBr(self, item):
        return unicode("  ") + item + " "#"<br>"

    def putBold(self, item):
        return "<b>" + unicode("  ") + item + " </b>"# "</b><br>"


    # move to id numbered stack
    def stackMove(self, id):
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)
            _w = self.ui.mainStack.currentWidget()
            _w.update()
            _w.shown()

        if self.ui.mainStack.currentIndex() == len(self.screens)-1:
            self.ui.buttonNext.hide()
            self.ui.buttonFinish.show()
        else:
            self.ui.buttonNext.show()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == 0:
            self.ui.buttonBack.hide()
        else:
            self.ui.buttonBack.show()

    # create all widgets and add inside stack
    def createWidgets(self, screens=[]):
        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _scr = screen.Widget()
            self.ui.mainStack.addWidget(_scr)

        self.stackMove(0)

    def disableNext(self):
        self.buttonNext.setEnabled(False)

    def disableBack(self):
        self.buttonBack.setEnabled(False)

    def enableNext(self):
        self.buttonNext.setEnabled(True)

    def enableBack(self):
        self.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.buttonBack.isEnabled()

    def __del__(self):
        group = self.config.group("General")
        group.writeEntry("RunOnStart", "False")

if __name__ == "__main__":
    # About data
    appName     = "kaptan"
    catalog     = ""
    programName = ki18n("kaptan")
    version     = "4.0"
    description = ki18n("Kaptan is a welcome wizard for Pardus")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009 Pardus")
    text        = ki18n("none")
    homePage    = "www.pardus.org.tr"
    bugEmail    = "renan@pardus.org.tr"

    aboutData   = KAboutData(appName,catalog, programName, version, description,
                                license, copyright,text, homePage, bugEmail)

    KCmdLineArgs.init(sys.argv, aboutData)
    app =  kdeui.KApplication()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    kaptan = Kaptan()
    kaptan.show()
    rect  = QtGui.QDesktopWidget().screenGeometry()
    kaptan.move(rect.width()/2 - kaptan.width()/2, rect.height()/2 - kaptan.height()/2)
    app.exec_()


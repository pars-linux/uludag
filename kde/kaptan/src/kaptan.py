#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyQt4.QtCore import QTimeLine
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs, KConfig

import os
import dbus
import subprocess

from kaptan.screens.ui_kaptan import Ui_kaptan

from kaptan.tools import tools
from kaptan.tools.progress_pie import DrawPie
from kaptan.tools.kaptan_menu import Menu

import glob

def loadScreen(screenName):
    split = screenName.split('.')
    screen = __import__(screenName)

    for s in split[1:]:
        screen = getattr(screen, s)

    return screen

screens = glob.glob("screens/scr*py")
for screen in screens:
    print screen
    screenName = screen.split("/")[-1].split(".")[0]
    print screenName
    vars()[screenName] = loadScreen("kaptan.screens." + screenName)


class Kaptan(QtGui.QWidget):
    def __init__(self, parent = None):

        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_kaptan()

        self.ui.setupUi(self)
        #self.setStyle(QtGui.QStyleFactory.create('Plastique'))

        # Kaptan screen settings
        self.commonScreens = [scrWelcome, scrMouse, scrStyle, scrMenu, scrWallpaper, scrNetwork]
        self.endScreens = [scrSummary, scrGoodbye]
        self.screens = self.appendOtherScreens(self.commonScreens) + self.endScreens

        self.screenData = None
        self.moveInc = 1
        self.menuText = ""
        self.config = KConfig("kaptanrc")
        self.titles = []
        self.descriptions = []

        # Draw progress pie
        self.countScreens = len(self.screens)
        self.pie = DrawPie(self.countScreens, self.ui.labelProgress)

        # Add screens to StackWidget
        self.createWidgets(self.screens)

        # Get Screen Titles
        for screen in self.screens:
            title = screen.Widget.title.toString()
            self.titles.append(title)

        # Initialize Menu
        self.menu = Menu(self.titles, self.ui.labelMenu)
        self.menu.start()

        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        QtCore.QObject.connect(self.ui.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        QtCore.QObject.connect(self.ui.buttonFinish, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.ui.buttonCancel, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))


        def compile_module(self, filename):
            """
                Compiles a Python module and returns locals.

                Args:
                    filename: Path to Python module
                Returns: Dictionary of local objects
            """
            try:
                locals = globals = {}
                code = open(filename).read()
                exec compile(code, "error", "exec") in locals, globals
            except IOError, e:
                logging.warning("Module has errors: %s" % filename)
            except SyntaxError, e:
                logging.warning("Module has syntax errors: %s" % filename)
            return locals

    def smoltProfileSent(self):
        ''' Do not show smolt screen if profile was already sended.'''
        smolt_uuid_path = "/etc/smolt/pub-uuid-smolt.pardus.org.tr"

        if os.path.exists(smolt_uuid_path):
            if os.path.getsize(smolt_uuid_path) > 0:
                return True

        return False

    def appendOtherScreens(self, commonScreens):
        screens = commonScreens

        # Append other screens depending on the following cases
        if tools.isLiveCD():
            screens.append(scrKeyboard)

        else:
            if self.smoltProfileSent():
                screens.append(scrPackage)
                screens.append(scrSearch)
            else:
                screens.append(scrSearch)
                screens.append(scrSmolt)
                screens.append(scrPackage)

        return screens

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

    # execute next step
    def slotNext(self,dryRun=False):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex() + 1

        # update pie progress
        self.pie.updatePie(curIndex)

        # animate menu
        self.menu.next()

        _w = self.ui.mainStack.currentWidget()

        ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1

    # execute previous step
    def slotBack(self):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex()

        # update pie progress
        self.pie.updatePie(curIndex-1)

        # animate menu
        self.menu.prev()


        _w = self.ui.mainStack.currentWidget()

        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    # move to id numbered stack
    def stackMove(self, id):
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)

            # Set screen title
            self.ui.screenTitle.setText(self.descriptions[id])

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

            # Append screen descriptions to list
            self.descriptions.append(_scr.desc.toString())

            # Append screens to stack widget
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
    version     = "4.5"
    description = ki18n("Kaptan is a welcome wizard for Pardus")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2010 Pardus")
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


#!/usr/bin/python
# -*- coding: utf-8 -*-

import apport.ui
import sys
from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from threading import Thread

import gui, subprocess, os, dbus

from gui.bugtoolMain import Ui_bugtoolUI
from gui import errorScreen

availableScreens = [errorScreen, ]

class PApport(QtGui.QWidget, apport.ui.UserInterface):

    def __init__(self, app, parent=None):
        apport.ui.UserInterface.__init__(self)
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_bugtoolUI()

        self.ui.setupUi(self)
        self.screens = availableScreens
        self.active_screens = []
        self.screenData = None
        self.moveInc = 1
        self.app = app
        self.app.setQuitOnLastWindowClosed(True)
        self.running = True

        self.waitNextClick = QtCore.QWaitCondition()
        self.mutex = QtCore.QMutex()

        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"),
                               self.slotNext)
        QtCore.QObject.connect(self.ui.buttonFinish,
                               QtCore.SIGNAL("clicked()"),
                               self._doQuit)
        QtCore.QObject.connect(self.ui.buttonCancel,
                               QtCore.SIGNAL("clicked()"),
                               self._doQuit)

        self.run_argv()

    def slotNext(self):
        self.waitNextClick.wakeAll()

    def _doQuit(self):
        self.running = False
        self.waitNextClick.wakeAll()
        self.app.quit()

    def _updateMenu(self):
        self.menuText = ""
        current = self.ui.mainStack.currentIndex()
        for each in self.active_screens:
            title = each.Widget().windowTitle()
            if self.active_screens.index(each) == current:
                self.menuText += self.putBold(title)
            else:
                self.menuText += self.putBr(title)
        self.ui.labelMenu.setText(self.menuText)

    def getCur(self, d):
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    def setCurrent(self, wid=None):
        if wid:
            self.stackMove(wid)

    def appendScreen(self, screen):
        self.active_screens.append(screen)
        widget = screen.Widget()
        self.ui.mainStack.addWidget(widget)
        #index = self.ui.mainStack.count()
        #self.ui.mainStack.setCurrentIndex(index)
        self.ui.mainStack.setCurrentWidget(widget)
        self._updateMenu()

    def putBr(self, item):
        return unicode(u"» ") + item + "<br>"

    def putBold(self, item):
        return "<b>" + unicode(u"» ") + item + "</b><br>"

    def wait_for_next_click(self):
        self.mutex.lock()
        self.waitNextClick.wait(self.mutex)

    def wait_user_input(self):
        t = Thread(None, self.wait_for_next_click, 'waiter', (), None)
        t.start()
        while t.is_alive():
            self.app.processEvents()
        if not self.running:
            sys.exit(0)

    # Apport interface
    def ui_present_crash(self, desktop_entry):
        self.appendScreen(errorScreen)
        self.wait_user_input()



if __name__ == "__main__":
    # About data
    appName     = "papport"
    catalog     = ""
    programName = ki18n("papport")
    version     = "0.1"
    description = ki18n("Pardus' Apport KDE GUI")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009 Pardus")
    text        = ki18n("none")
    homePage    = "www.pardus.org.tr"
    bugEmail    = "pinar@pardus.org.tr"

    aboutData   = KAboutData(appName,catalog, programName, version, description,
                                license, copyright,text, homePage, bugEmail)

    KCmdLineArgs.init(sys.argv, aboutData)
    app =  kdeui.KApplication()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    papport = PApport(app)
    papport.show()
    rect  = QtGui.QDesktopWidget().screenGeometry()
    papport.move(rect.width()/2 - papport.width()/2, rect.height()/2 -\
                 papport.height()/2)
    papport.ui_present_crash(None)
    #papport.appendScreen(goodbyeWidget)
    app.exec_()


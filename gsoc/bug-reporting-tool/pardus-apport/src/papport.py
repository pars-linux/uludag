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
        self.active_widgets = []
        self.screenData = None
        self.moveInc = 1
        self.app = app
        self.app.setQuitOnLastWindowClosed(True)
        self.running = True

        self.waitNextClick = QtCore.QWaitCondition()
        self.mutex = QtCore.QMutex()

        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"),
                               self.slotNext)
        QtCore.QObject.connect(self.ui.buttonCancel,
                               QtCore.SIGNAL("clicked()"),
                               self.closeEvent)

        self.run_argv()

    def slotNext(self):
        self.waitNextClick.wakeAll()

    def closeEvent(self, event=None):
        self.running = False
        self.waitNextClick.wakeAll()
        if event is not None:
            event.accept()
        self.app.quit()

    def _updateMenu(self):
        self.menuText = ""
        current = self.ui.mainStack.currentIndex()
        for each in self.active_widgets:
            title = each.windowTitle()
            if self.active_widgets.index(each) == current:
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
        widget = screen.Widget()
        self.active_widgets.append(widget)
        self.ui.mainStack.addWidget(widget)
        #index = self.ui.mainStack.count()
        #self.ui.mainStack.setCurrentIndex(index)
        self.ui.mainStack.setCurrentWidget(widget)
        self._updateMenu()

    def set_current_title(self, title):
        self.current.setWindowTitle(title)
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

    @property
    def current(self):
        return self.ui.mainStack.currentWidget()

    # Apport interface
    def ui_present_crash(self, desktop_entry):
        self.appendScreen(errorScreen)

        if desktop_entry:
            name = desktop_entry.getName()
            heading = 'Sorry, %s closed unexpectedly' % name
        elif self.report.has_key('ExecutablePath'):
            name = os.path.basename(self.report['ExecutablePath'])
            heading = 'Sorry, the program "%s" closed unexpectedly.' % name
        else:
            name = self.cur_package
            heading = 'Sorry, %s closed unexpectedly.' % name

        self.set_current_title(name)
        self.current.ui.heading.setText(heading)
        self.current.ui.text.setText('If you were not doing anything '
                                     'confidential (entering passwords or '
                                     'other private information), you can help'
                                     'to improve the application by reporting'
                                     'the problem.')
        self.current.setCheckBox('&Ignore future crashes of this program'
                                 ' version')
        self.wait_user_input()

        blacklist = self.current.ui.checkBox.isChecked()
        return {'action': 'report', 'blacklist': blacklist}

    def ui_present_kernel_error(self):
        self.appendScreen(errorScreen)

        message = 'Your system encountered a serious kernel problem.'
        annotate = ''
        if self.report.has_key('Annotation'):
            annotate = self.report['Annotation'] + '\n\n'
        annotate += ('You can help the developers to fix the problem by '
                     'reporting it.')

        self.set_current_title('Kernel problem')
        self.current.ui.heading.setText(message)
        self.current.ui.text.setText(annotate)

        self.wait_user_input()
        return 'report'

    def ui_persent_package_error(self):
        self.appendScreen(errorScreen)

        name = self.report['Package']
        heading = 'Sorry, the package "%s" failed to install or upgrade.' % name
        text = ('You can help the developers to fix the package by reporting'\
                ' the problem')

        self.wait_user_input()
        return 'report'



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
    app.exec_()


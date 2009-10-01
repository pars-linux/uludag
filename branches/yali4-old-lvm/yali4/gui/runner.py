# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import *

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4
import yali4.installer
import yali4.sysutils
import yali4.localedata
import yali4.gui.context as ctx
from yali4.gui.YaliDialog import Dialog

from yali4.gui.debugger import Debugger
from yali4.gui.debugger import DebuggerAspect

# mainScreen
import YaliWindow
from yali4.gui.installdata import *

##
# Runner creates main GUI components for installation...
class Runner:

    _window = None
    _app = None

    def __init__(self):

        # Qt Stuff
        ctx._app = self._app = QtGui.QApplication(sys.argv)
        desktop  = self._app.desktop()

        # Yali..
        self._window = YaliWindow.Widget()
        ctx.mainScreen = self._window

        # Check for firstBoot on installed system (parameters from options)
        install_type = YALI_INSTALL

        if ctx.options.firstBoot == True or os.path.exists("/etc/yali-is-firstboot"):
            install_type = YALI_FIRSTBOOT

        # check for oemInstall
        if yali4.sysutils.checkYaliParams(param=ctx.consts.oemInstallParam):
            install_type = YALI_OEMINSTALL

        # check for rescue Mode
        if ctx.options.rescueMode == True or yali4.sysutils.checkYaliParams(param=ctx.consts.rescueModeParam):
            install_type = YALI_RESCUE

        install_plugin = yali4.sysutils.checkYaliOptions("plugin") or ctx.options.plugin or None
        if install_plugin:
            install_type = YALI_PLUGIN

        # Creating the installer
        ctx.yali = yali4.installer.Yali(install_type, install_plugin)

        # These shorcuts for developers :)
        prevScreenShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.SHIFT + Qt.Key_F1),self._window)
        nextScreenShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.SHIFT + Qt.Key_F2),self._window)
        QObject.connect(prevScreenShortCut, SIGNAL("activated()"), self._window.slotBack)
        QObject.connect(nextScreenShortCut, SIGNAL("activated()"), self._window.slotNext)

        # yimirtaShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.SHIFT + Qt.Key_F5),self._window)
        # QObject.connect(yimirtaShortCut, SIGNAL("activated()"), ctx.yali.toggleYimirta)

        # visual debugger
        ctx.debugger = Debugger()

        # check boot flags
        # visual debug mode
        if ctx.options.debug == "True" or yali4.sysutils.checkYaliParams(param="debug"):
            ctx.debugEnabled = True

        # Let start
        ctx.debugger.log("Yali has been started.")
        ctx.debugger.log("System language is '%s'" % ctx.consts.lang)
        ctx.debugger.log("Install type is %d" % ctx.yali.install_type)
        ctx.debugger.log("Kernel Command Line : %s" % file("/proc/cmdline","r").read())
        # VBox utils
        ctx.debugger.log("Starting VirtualBox tools..")
        yali4.sysutils.run("VBoxClient --autoresize")
        yali4.sysutils.run("VBoxClient --clipboard")

        # add Screens for selected install type
        self._window.createWidgets(ctx.yali.screens)

        # base connections
        QObject.connect(self._app, SIGNAL("lastWindowClosed()"),
                        self._app, SLOT("quit()"))
        QObject.connect(ctx.mainScreen, SIGNAL("signalProcessEvents"),
                        self._app.processEvents)
        QObject.connect(desktop, SIGNAL("resized(int)"),
                        self._reinit_screen)

        # set the current screen ...
        ctx.mainScreen.setCurrent(ctx.options.startupScreen)

        # Font Resize
        fontMinusShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.CTRL + Qt.Key_Minus),self._window)
        fontPlusShortCut  = QtGui.QShortcut(QtGui.QKeySequence(Qt.CTRL + Qt.Key_Plus) ,self._window)
        QObject.connect(fontMinusShortCut, SIGNAL("activated()"), self._window.setFontMinus)
        QObject.connect(fontPlusShortCut , SIGNAL("activated()"), self._window.setFontPlus)

    ##
    # Fire up the interface.
    def run(self):

        # Use default theme;
        # if you use different Qt4 theme our works looks ugly :)
        self._app.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self._init_screen()

        # For testing..
        # self._window.resize(QSize(800,600))

        # Run run run
        self._app.exec_()

    def _reinit_screen(self):
        QTimer.singleShot(700,self._init_screen)

    def _init_screen(self, screen = 0):
        # We want it to be a full-screen window.
        self._window.resize(self._app.desktop().size())
        self._window.setMaximumSize(self._app.desktop().size())
        self._window.move(0,0)
        self._window.show()
        ctx.yali.info.updateMessage()

def showException(ex_type, tb):
    title = _("Error!")
    closeButton = True

    if ex_type in (yali4.exception_fatal, yali4.exception_pisi):
        closeButton = False
        w = ErrorWidget(tb)
    else:
        w = ExceptionWidget(tb)

    print "BACKTRACE: ",tb
    ctx.debugger.log(tb)
    d = Dialog(title, w, None, closeButton)
    d.resize(500,400)
    d.exec_()

class ExceptionWidget(QtGui.QWidget):
    def __init__(self, tb_text, *args):
        apply(QtGui.QWidget.__init__, (self,) + args)

        info = QtGui.QLabel(self)
        info.setText("Unhandled exception occured!")
        traceback = QtGui.QTextBrowser(self)
        traceback.setText(tb_text)

        l = QtGui.QVBoxLayout(self)
        l.setSpacing(10)
        l.addWidget(info)
        l.addWidget(traceback)

class ErrorWidget(QtGui.QWidget):
    def __init__(self, tb_text, *args):
        apply(QtGui.QWidget.__init__, (self,) + args)

        info = QtGui.QLabel(self)
        info.setText(_("Unhandled error occured!"))
        traceback = QtGui.QTextBrowser(self)
        traceback.setText(tb_text)

        reboot_button = QtGui.QPushButton(self)
        reboot_button.setText(_("Reboot System!"))

        l = QtGui.QVBoxLayout(self)
        l.setSpacing(10)
        l.addWidget(info)
        l.addWidget(traceback)
        l.addWidget(reboot_button)

        self.connect(reboot_button, SIGNAL("clicked()"),
                     self.slotReboot)

    def slotReboot(self):
        yali4.sysutils.reboot()


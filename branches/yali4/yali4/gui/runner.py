# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import *

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4
import yali4.installer
import yali4.sysutils
import yali4.gui.context as ctx
from yali4.gui.YaliDialog import Dialog

from yali4.gui.debugger import Debugger
from yali4.gui.debugger import DebuggerAspect

# mainScreen
import YaliWindow

YALI_INSTALL, YALI_FIRSTBOOT, YALI_OEMINSTALL, YALI_PARTITIONER = range(4)

##
# Runner creates main GUI components for installation...
class Runner:

    _window = None
    _app = None

    def __init__(self):

        # Qt Stuff
        self._app = QtGui.QApplication(sys.argv)

        # Yali..
        self._window = YaliWindow.Widget()
        ctx.mainScreen = self._window

        # Check for firstBoot on installed system (parameters from options)
        install_type = YALI_INSTALL

        if ctx.options.firstBoot == True:
            install_type = YALI_FIRSTBOOT

        # check for oemInstall
        if yali4.sysutils.checkYaliParams(param=ctx.consts.oemInstallParam):
            install_type = YALI_OEMINSTALL

        ctx.yali = yali4.installer.Yali(install_type)

        # visual debugger
        ctx.debugger = Debugger()

        # check boot flags
        # visual debug mode
        if ctx.options.debug == True or yali4.sysutils.checkYaliParams(param="debug"):
            ctx.debugEnabled = True

        # Let start
        ctx.debugger.log("Yali has been started.")
        ctx.debugger.log("Install type is %d" % ctx.yali.install_type)

        # font = QtGui.QFont()
        # font.setFamily("Droid Sans")
        # font.setPixelSize(11)
        # self._app.setFont(font)

        # add Screens for selected install type
        self._window.createWidgets(ctx.yali.screens)

        # base connections
        QObject.connect(self._app, SIGNAL("lastWindowClosed()"),
                        self._app, SLOT("quit()"))
        QObject.connect(ctx.mainScreen.ui, SIGNAL("signalProcessEvents"),
                        self._app.processEvents)

        # set the current screen ...
        ctx.mainScreen.setCurrent(ctx.options.startupScreen)

    ##
    # Fire up the interface.
    def run(self):

        # Use default theme;
        # if you use different Qt4 theme our works looks ugly :)
        self._app.setStyle(QtGui.QStyleFactory.create('Plastique'))

        # We want it to be a full-screen window.
        self._window.ui.resize(self._app.desktop().size())
        self._window.ui.move(0,0)
        self._window.ui.show()
        ctx.yali.info.updateMessage()

        # For testing..
        # self._window.ui.resize(QSize(800,600))

        # Run run run
        self._app.exec_()

def showException(ex_type, tb):
    title = _("Error!")

    if ex_type in (yali4.exception_fatal, yali4.exception_pisi):
        w = ErrorWidget(tb)
    else:
        w = ExceptionWidget(tb)

    print "BACKTRACE: ",tb
    ctx.debugger.log(tb)
    d = Dialog(title, w, None)
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


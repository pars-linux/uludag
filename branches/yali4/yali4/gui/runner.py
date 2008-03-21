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
import yali4.sysutils
import yali4.gui.context as ctx
from yali4.gui.YaliDialog import Dialog

from yali4.gui.debugger import Debugger
from yali4.gui.debugger import DebuggerAspect

# mainScreen
import YaliWindow

# screens
import ScrKahyaCheck
import ScrWelcome
import ScrCheckCD
import ScrKeyboard
import ScrDateTime
import ScrAdmin
import ScrUsers
import ScrPartitionAuto
import ScrPartitionManual
import ScrBootloader
import ScrInstall
import ScrGoodbye

##
# Runner creates main GUI components for installation...
class Runner:

    _window = None
    _app = None

    def __init__(self):

        _all_screens = [                        # Numbers can be used with -s paramter
                        ScrKahyaCheck,          # 00
                        ScrWelcome,             # 01
                        ScrCheckCD,             # 02
                        ScrKeyboard,            # 03
                        ScrDateTime,            # 04
                        ScrUsers,               # 05
                        ScrAdmin,               # 06
                        ScrPartitionAuto,       # 07
                        ScrPartitionManual,     # 08
                        ScrBootloader,          # 09
                        ScrInstall,             # 10
                        ScrGoodbye              # 11
                       ]

        self._app = QtGui.QApplication(sys.argv)
        self._window = YaliWindow.Widget()

        # check for oemInstall
        if yali4.sysutils.checkYaliParams(param=ctx.consts.firstBootParam):
            ctx.options.kahyaFile = ctx.consts.firstBootFile

        # font = QtGui.QFont()
        # font.setFamily("Droid Sans")
        # self._app.setFont(font)

        ctx.mainScreen = self._window

        # visual debugger
        ctx.debugger = Debugger()

        # visual debug mode
        if ctx.options.debug == True or yali4.sysutils.checkYaliParams(param="debug"):
            ctx.debugEnabled = True

        ctx.debugger.log("Yali Started")

        self._window.createWidgets(_all_screens)
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
        self._window.ui.show()

        # For testing..
        #self._window.ui.resize(QSize(800,600))
        # self._window.ui.move(0,0)
        self._app.exec_()


def showException(ex_type, tb):
    title = _("Error!")

    if ex_type in (yali4.exception_fatal, yali4.exception_pisi):
        w = ErrorWidget(tb)
    else:
        w = ExceptionWidget(tb)
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


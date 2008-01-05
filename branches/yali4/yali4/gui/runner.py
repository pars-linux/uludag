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

import YaliWindow
# screens
import ScrWelcome
import ScrCheckCD
import ScrKeyboard
import ScrAdmin
import ScrUsers
import ScrPartitionAuto
import ScrPartitionManual

#import ScrInstall
#import ScrBootloader
#import ScrGoodbye
#import ScrKahyaCheck

##
# Runner creates main GUI components for installation...
class Runner:

    _window = None
    _app = None

    def __init__(self):

        _all_screens = [
                        ScrWelcome,
                        ScrCheckCD,
                        ScrKeyboard,
                        ScrAdmin,
                        ScrUsers,
                        ScrPartitionAuto,
                        ScrPartitionManual
                       ]

        """
        _all_stages = [
            {'num': 1, 'text': _("Basic setup")},
            {'num': 2, 'text': _("Prepare for install")},
            {'num': 3, 'text': _("Install system")}
            ]

        _all_screens = [
             {'stage': 1, 'module': ScrKahyaCheck},
             {'stage': 1, 'module': ScrWelcome},
             {'stage': 1, 'module': ScrCheckCD},
             {'stage': 1, 'module': ScrKeyboard},
             {'stage': 1, 'module': ScrAdmin},
             {'stage': 1, 'module': ScrUsers},
             {'stage': 2, 'module': ScrPartitionAuto},
             {'stage': 2, 'module': ScrPartitionManual},
             {'stage': 2, 'module': ScrBootloader},
             {'stage': 3, 'module': ScrInstall},
             {'stage': 3, 'module': ScrGoodbye}
             ]
        """

        self._app = QtGui.QApplication(sys.argv)
        self._window = YaliWindow.Widget()

        # check for oemInstall
        if yali4.sysutils.checkYaliParams(param=ctx.consts.firstBootParam):
            ctx.options.kahyaFile = ctx.consts.firstBootFile

        # font = QtGui.QFont()
        # font.setFamily("Droid Sans")
        # self._app.setFont(font)

        # visual debugger
        ctx.debugger = Debugger()

        # visual debug mode
        if ctx.options.debug == True or yali4.sysutils.checkYaliParams(param="debug"):
            ctx.debugEnabled = True

        ctx.debugger.log("Yali Started")

        # add stages
        # for stg in _all_stages:
        #     ctx.stages.addStage(stg['num'], stg['text'])

        ctx.mainScreen = self._window

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
        self._window.ui.show()
        # We want it to be a full-screen window.
        # self._window.ui.resize(self._app.desktop().size())

        # For testing..
        self._window.ui.resize(QSize(800,600))
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

        b = QtGui.QHBoxLayout(l)
        b.setMargin(5)
        b.addStretch(1)
        b.addWidget(reboot_button)

        self.connect(reboot_button, SIGNAL("clicked()"),
                     self.slotReboot)

    def slotReboot(self):
        yali4.sysutils.reboot()


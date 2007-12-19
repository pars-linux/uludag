# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from pyaspects.meta import MetaAspect
import yali4.gui.context as ctx
import time

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

from yali4.gui.YaliDialog import Dialog

class Debugger:
    def __init__(self,showTimeStamp=True):
        title = _("Debug")
        self.debugWidget = QtGui.QWidget()
        self.traceback = DebugContainer(self.debugWidget,showTimeStamp)

        l = QtGui.QVBoxLayout(self.debugWidget)
        l.addWidget(self.traceback)

        self.window = Dialog(title,self.debugWidget)
        self.window.resize(500,400)
        self.aspect = DebuggerAspect(self)

    def showWindow(self):
        self.window.show()

    def log(self,log,type=1,indent=0):
        if ctx.debugEnabled:
            self.traceback.add(unicode(log),type,indent)

class DebugContainer(QtGui.QTextBrowser):
    def __init__(self, parent, showTimeStamp=True):
        QtGui.QTextBrowser.__init__(self, parent)
        self.setStyleSheet("font-size:8pt;font-family:\"Envy Code R\";")
        self.showTimeStamp = showTimeStamp
        self.setReadOnly(True)
        self.setOverwriteMode(True)
        self.plainLogs = ''
        self.indent = 0

    def add(self,log,type,indent):
        if indent==+1:
            self.indent += indent
        if type==1:
            self.plainLogs += "%s\n" % log
            log = "<b>%s</b>" % log
        if self.showTimeStamp:
            _now = time.strftime("%H:%M:%S", time.localtime())
            self.append(unicode("%s : %s %s" % (_now,"»"*self.indent,log)))
        else:
            self.append(unicode(log))
        if indent==-1:
            self.indent += indent

class DebuggerAspect:
    __metaclass__ = MetaAspect
    name = "DebugAspect"

    def __init__(self, out ):
        self.out = out

    def before(self, wobj, data, *args, **kwargs):
        met_name = data['original_method_name']
        class_ = str(data['__class__'])[8:-2]
        fun_str = "%s%s from %s" % (met_name, args, class_)
        self.out.log("call, %s" % fun_str,0,+1)

    def after(self, wobj, data, *args, **kwargs):
        met_name = data['original_method_name']
        fun_str = "%s%s" % (met_name, args)
        self.out.log("left, %s" % fun_str,0,-1)


#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import QEventLoop
from kdeui import KCursor

from Debug import Debug

# global KApplication reference for setting cursor type
app = None
debugger = None
packageToInstall = None

def init(application, debug = False):
    global app
    app = application
    if debug:
        global debugger
        debugger = Debug()

def debug(msg):
    if debugger:
        debugger.write(msg)

def setWaitCursor():
    if app:
        app.setOverrideCursor(KCursor.waitCursor)

def setNormalCursor():
    if app:
        app.restoreOverrideCursor()

def config():
    if app:
        return app.config()
    return None

def setPackageToInstall(pack):
    global packageToInstall
    packageToInstall = pack

def processEvents():
    if app:
        app.processEvents(QEventLoop.ExcludeUserInput)

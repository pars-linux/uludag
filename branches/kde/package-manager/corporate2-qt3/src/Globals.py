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
        app.setOverrideCursor(KCursor.waitCursor())

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
    return
    #FIXME: package-manager freezes after this
    if app:
        app.processEvents(QEventLoop.ExcludeUserInput)

def humanReadableSize(size, precision=".1"):
    symbols, depth = [' B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'], 0

    while size > 1000 and depth < 8:
        size = float(size / 1024)
        depth += 1

    if size == 0:
        return "0 B"

    fmt = "%%%sf %%s" % precision
    return fmt % (size, symbols[depth])

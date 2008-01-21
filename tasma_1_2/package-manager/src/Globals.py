#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import QEventLoop
from kdeui import KCursor

# global KApplication reference for setting cursor type
app = None

def init(application):
    global app
    app = application

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

def processEvents():
    if app:
        app.processEvents(QEventLoop.ExcludeUserInput)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
from PyQt4.QtGui import QDesktopWidget

def importScreen(screenName):
    ''' imports a screen by name '''
    screen = __import__(screenName)
    for s in screenName.split('.')[1:]:
        screen = getattr(screen, s)
    return screen

def loadScreens(screensPath, globals):
    ''' imports all screens in the specified directory '''
    screens = glob.glob(screensPath)
    print screens
    for screen in screens:
        screenName = screen.split("/")[-1].split(".")[0]
        globals[screenName] = importScreen("migration.gui." + screenName)

def isLiveCD():
    return os.path.exists('/var/run/pardus/livemedia')

def centerWindow(window):
    rect   = QDesktopWidget().screenGeometry()
    width  = 0
    heigth = 0

    if rect.width <= 640: width = 620
    elif rect.width <= 800: width = 720
    else: width = 960

    if rect.height <= 480: height = 450
    elif rect.height <= 600: height = 520
    else: height = 680

    window.resize(width, height)
    window.move(rect.width()/2 - window.width()/2, rect.height()/2 - window.height()/2)

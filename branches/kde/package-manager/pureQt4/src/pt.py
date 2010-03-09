#!/usr/bin/python
# -*- coding: utf-8 -*-

# from qticonloader import QIconLoader
from os import getenv
from os.path import exists

import gettext
__trans = gettext.translation('package-manager', fallback=True)

def log(msg):
    if getenv("DEBUG_PT"):
        print msg

def isKde4():
    return getenv("KDE_SESSION_VERSION") or exists('/usr/kde/4')

if isKde4():
    log("You are running KDE 4")

    from PyKDE4.kdecore import *

    i18n      = __trans.ugettext
    AboutData = KAboutData
    Config    = KConfig


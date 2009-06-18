#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardus.localedata import languages as LANGUAGES

def listLanguages():
    languages = []
    for code, info in LANGUAGES.iteritems():
        languages.append((code, str(info.name)))
    return languages

def getLanguage():
    return "tr"

def setLanguage(lang):
    pass


def listKeymaps(language=""):
    keymaps = []
    if language and language in LANGUAGES:
        for keymap in LANGUAGES[language].keymaps:
            keymaps.append((keymap.console_layout, str(keymap.name)))
    else:
        for language in LANGUAGES:
            for keymap in LANGUAGES[language].keymaps:
                keymaps.append((keymap.console_layout, str(keymap.name)))
    return keymaps

def getKeymap():
    return "trq"

def setKeymap(keymap):
    pass


def listLocales(language=""):
    locales = []
    if language and language in LANGUAGES:
        locale = LANGUAGES[language].locale
        locales.append((locale, str(locale)))
    else:
        for language in LANGUAGES:
            locale = LANGUAGES[language].locale
            locales.append((locale, str(locale)))
    return locales

def getLocale():
    return "tr_TR.UTF-8"

def setLocale(local):
    pass


def getHeadStart():
    return "xdm"

def setHeadStart(package):
    pass


def getClock():
    return True, True

def setClock(clock, adjust):
    pass


def getTTYs():
    return 6

def setTTYs(count):
    pass

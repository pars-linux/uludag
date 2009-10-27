#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *
from kdeui import *
from khtml import *
import os

mod_name = 'History Manager'
mod_app = 'history-manager'
mod_version = '0.1.1'

def I18N_NOOP(str):
    return str

def AboutData():
    global mod_app
    global mod_name
    global mod_version
    about_data = KAboutData(mod_app,
                            mod_name,
                            mod_version,
                            I18N_NOOP('History Manager Interface'),
                            KAboutData.License_GPL,
                            '(C) 2008 UEKAE/TÜBİTAK',
                            None, None,
                            'bugs@pardus.org.tr')
    about_data.addAuthor('İşbaran Akçayır', None, 'isbaran@gmail.com')

    return about_data

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIconSet(name, group, size)

def runQuiet(cmd):
    f = file('/dev/null', 'w')
    return subprocess.call(cmd, stdout=f, stderr=f)

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(i18n('History Manager'))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 300)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)
        self.lang_code = os.environ['LANG'][:5].split('_')[0].lower()
        if os.path.isdir(locate('data', 'history-manager/help/%s/'%self.lang_code)):
            self.htmlPart.openURL(KURL(locate('data', 'history-manager/help/%s/main_help.html'%self.lang_code)))
        else:
            self.htmlPart.openURL(KURL(locate('data', 'history-manager/help/en/main_help.html')))

def isLocked(file):
    try:
        f = open(file, 'r')
    except:
        print i18n("Can't open lock file")
    import string
    a = f.readlines()
    if string.split(a[0])[0] == 'locked':
        return True
    else:
        return False

def lock(file, true=True):
    try:
        f = open(file, 'w')
    except:
        print i18n("Can't open lock file")
        return
    import fcntl
    if true:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            f.write("locked")
        except IO_Error, value:
            if value[0] == 11:
                print i18n("Resource temporarily unavailable, Lock failed")
            else:
                raise
    else:
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    f.close()


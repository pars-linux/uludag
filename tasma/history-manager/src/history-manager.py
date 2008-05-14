#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

import sys

from qt import *
from kdecore import *
from kdeui import *

from historygui import formMain
from history_gui import *

import dbus

mod_name = 'History Manager'
mod_app = 'history-manager'
mod_version = '0.1'

def AboutData():
    global mod_app
    global mod_name
    global mod_version
    about_data = KAboutData(mod_app,
                            mod_name,
                            mod_version,
                            'History Manager Interface',
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

def attachMainWidget(self):
    KGlobal.iconLoader().addAppDir(mod_app)
    self.mainwidget = widgetMain(self)
    self.aboutus = KAboutApplication(self)

class Module(KCModule):
    def __init__(self, parent, name):
        KCModule.__init__(self, parent, name)
        KGlobal.locale().insertCatalogue(mod_app)
        self.config = KConfig(mod_app)
        self.aboutData = AboutData()
        attachMainWidget(self)

    def aboutData(self):
        return self.aboutData

def create_history_manager(parent, name):
    global kapp

    kapp = KApplication.kApplication()
    return Module(parent, name)

def main():
    global kapp

    about = AboutData()
    KCmdLineArgs.init(sys.argv, about)
    KUniqueApplication.addCmdLineOptions()

    if not KUniqueApplication.start():
        print i18n('History Manager is already runnings!')
        return

    kapp = KUniqueApplication(True, True, True)

    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    win = QDialog()
    #win.config = KConfig(mod_app)
    win.setCaption(i18n('History Manager'))
    attachMainWidget(win)
    kapp.setMainWidget(win)

    sys.exit(win.exec_loop())

if __name__ == '__main__':
    main()

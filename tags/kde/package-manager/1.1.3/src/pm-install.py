#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import sys
import os

# PyQt/PyKDE
from kdecore import *
from kdeui import *
from kio import *

import dcopext

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

def main():

    aboutdata = KAboutData("pm-install","pm-install","0.0.1", "package-manager command line dcop interface installer", \
                               KAboutData.License_GPL, "Copyright (C) 2006 TUBITAK/UEKAE")

    options = [
        ("+package", I18N_NOOP("PiSi package to install")),
        ]

    KLocale.setMainCatalogue("package-manager")

    KCmdLineArgs.init(sys.argv, aboutdata)
    KCmdLineArgs.addCmdLineOptions(options)

    if not KUniqueApplication.start():
        sys.exit(0)

    kapp = KUniqueApplication(True, True, True)
    args = KCmdLineArgs.parsedArgs()

    if args.count():
        
        if KMessageBox.No == KMessageBox.warningYesNo(None, 
                                                      i18n("You have selected a package to install. Do you want to continue?"),
                                                      i18n("Install Package"),
                                                      KGuiItem(i18n("Continue"), "ok"),
                                                      KGuiItem(i18n("Cancel"), "no"),
                                                      ):
            sys.exit(0)

        packageToInstall = KIO.NetAccess.mostLocalURL(args.url(0), None).path()

        dcop = kapp.dcopClient()
        pmi = dcopext.DCOPApp("package-manager", dcop)

        if pmi.objects:
            pmi.Installer.install(packageToInstall)
        else:
            os.system("/usr/kde/3.5/bin/package-manager --install %s" % packageToInstall)

if __name__ == "__main__":
    main()

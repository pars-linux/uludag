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
from kio import *

import dcopext

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

def main():

    aboutdata = KAboutData("pm-installer","pm-installer","0.0.1", "package-manager command line dcop interface installer", \
                               KAboutData.License_GPL, "Copyright (C) 2006 TUBITAK/UEKAE")

    KCmdLineArgs.init(sys.argv, aboutdata)
    KCmdLineArgs.addCmdLineOptions ([("install <package>", I18N_NOOP("Package to install"))])

    kapp = KApplication()
    args = KCmdLineArgs.parsedArgs()

    if args.isSet("install"):
        packageToInstall = str(KIO.NetAccess.mostLocalURL(KURL(args.getOption("install")), None).path())

        dcop = kapp.dcopClient()
        pmi = dcopext.DCOPApp("package-manager", dcop)

        if pmi.objects:
            pmi.Installer.install(packageToInstall)
        else:
            os.system("/usr/kde/3.5/bin/package-manager --install %s" % packageToInstall)

if __name__ == "__main__":
    main()

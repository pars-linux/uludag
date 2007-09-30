#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import sys

from qt import *
from kdecore import *
from kdeui import *

from wizard import MigrationWizard

def I18N_NOOP(text):
    return text

def main():
    about = KAboutData(
        "migration",
        I18N_NOOP("Migration Tool"),
        "0.8.2",
        I18N_NOOP("A wizard to transfer files and settings from existing operating systems"),
        KAboutData.License_GPL,
        '(C) 2006-2007 UEKAE/TÜBİTAK',
        None,
        "http://www.pardus.org.tr",
        "bugs@pardus.org.tr"
    )
    about.addAuthor("Murat Ongan", I18N_NOOP("Developer and Current Maintainer"), "mongan@cclub.metu.edu.tr")
    KCmdLineArgs.init(sys.argv, about)
    kapp = KApplication(True, True)
    wizard = MigrationWizard(kapp)
    
    kapp.setMainWidget(wizard)
    wizard.show()
    kapp.exec_loop()

if __name__ == "__main__":
    main()

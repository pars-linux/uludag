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

from wizard import Wizard

def main():
    about = KAboutData(
        "Migration Tool",
        "migration",
        "0.3",
        "Migration Tool",
        KAboutData.License_GPL,
        '(C) 2006-2007 UEKAE/TÜBİTAK',
        None,
        None,
        'bugs@pardus.org.tr'
    )
    about.addAuthor("Murat Ongan", "Developer and Current Maintainer", "mongan@cclub.metu.edu.tr")
    
    KCmdLineArgs.init(sys.argv, about)
    app = KUniqueApplication(True, True, True)
    wizard = Wizard()
    
    app.setMainWidget(wizard)
    wizard.show()
    app.exec_loop()

if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 TUBITAK/UEKAE
# Upgrade Manager
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys

# PDS
from pds import Pds
from pds.quniqueapp import QUniqueApplication
from gui import UmMainScreen

from PyQt4.QtGui import QMessageBox

# Translations
_pds = Pds('upgrade-manager', debug = False)
_ = _pds.i18n

if __name__ == '__main__':

    app = QUniqueApplication(sys.argv, catalog='um')

    if not os.geteuid() == 0:
        QMessageBox.critical(None, _("Upgrade Manager"),
                                   _("You must have super user privileges to launch upgrade-manager"))
        sys.exit()

    if '--start-from-step2' in sys.argv:
        step = 2
    elif '--start-from-step3' in sys.argv:
        step = 3
    else:
        step = 1

    def oldStep():
        step_file = os.path.expanduser("~/.umstep")
        if os.path.exists(step_file):
            return int(open(step_file).read())
        return 1

    if oldStep() > 1 and oldStep() < 4 and not step > 1:
        answer = QMessageBox.question(None, _("Upgrade Manager"),
                                            _("There are uncompleted upgrade steps left.\n"
                                              "Do you want to continue from this step ? (Recommended)"),
                                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                            QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            step = oldStep()
        elif answer == QMessageBox.Cancel:
            sys.exit(0)

    window = UmMainScreen(step = step)
    window.show()

    app.setStyle('plastique')
    app.exec_()

    sys.exit(0)


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
from pds.quniqueapp import QUniqueApplication
from gui import UmMainScreen

if __name__ == '__main__':

    app = QUniqueApplication(sys.argv, catalog='um')

    if '--start-from-step2' in sys.argv:
        step = 2
    elif '--start-from-step3' in sys.argv:
        step = 3
    else:
        step = 1

    window = UmMainScreen(step = step)
    window.show()

    app.setStyle('plastique')
    app.exec_()

    sys.exit(0)


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
from gui import UmGui

if __name__ == '__main__':

    app = QUniqueApplication(sys.argv, catalog='um')

    window = UmGui()
    window.show()

    app.exec_()

    sys.exit(0)


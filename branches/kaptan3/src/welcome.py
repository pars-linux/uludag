#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# QT & KDE Modules
from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

from Welcomedlg import kaptanUi

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = kaptanUi()
    f.show()
    app.setMainWidget(f)
    app.exec_loop()


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *

import mainview

app = QApplication([])
app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
w = QMainWindow()
w.setMinimumSize(620, 360)
a = mainview.UserManager(w, w)
w.setCentralWidget(a)
w.show()
app.exec_loop()

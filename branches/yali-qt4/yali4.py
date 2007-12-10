#!/usr/bin/env python
#
# Copyright (C) 2007 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from PyQt4 import QtCore, QtGui
from uis.main import Ui_YaliMain

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    YaliMain = QtGui.QWidget()
    ui = Ui_YaliMain()
    ui.setupUi(YaliMain)
    YaliMain.show()
    sys.exit(app.exec_())


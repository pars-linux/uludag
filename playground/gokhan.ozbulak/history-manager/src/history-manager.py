#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from hm import HM

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    hm = HM()
    hm.show()
    sys.exit(app.exec_())


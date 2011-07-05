#!/usr/bin/python
# -*- coding: utf-8 -*-
"""swipe finger dialog."""
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QApplication
import swipeform

class swipeDialog(QDialog, swipeform.Ui_dialogSwipe):
    """Dialog to indicate to the user that they need to swipe their finger.
    This dialog is modal dialog to inform the user. It has no ok or
    cancel buttons or X on the titlebar. It appears right before the device
    expects a swipe and blocks the GUI."""
    def __init__(self, parent=None):
        super(swipeDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

if __name__ == "__main__":
    import sys
    swipeapp = QApplication(sys.argv)
    form = swipeDialog()
    form.show()
    swipeapp.exec_()

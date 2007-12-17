#!/usr/bin/env python

import sys
import time

from qt import *

from d_light import DLoop, BUS_SYSTEM, BUS_SESSION

class mainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # DBus
        self.dloop = DLoop()
        self.dloop.start()

        box = QVBoxLayout(self)

        self.buttonCall = QPushButton(self)
        self.buttonCall.setText('Push Me!')
        box.addWidget(self.buttonCall)

        self.textMessages = QTextEdit(self)
        box.addWidget(self.textMessages)

        # register signal handler
        self.dloop.register("type='signal'", self.handleSignal, BUS_SYSTEM)

        self.connect(self.buttonCall, SIGNAL('clicked()'), self.slotClicked)

        self.resize(500, 300)

    def slotClicked(self):
        self.dloop.call("tr.org.pardus.comar", "/system", "tr.org.pardus.comar", "listApplications", (), self.handleClick, BUS_SYSTEM)

    def handleSignal(self, *args):
        self.textMessages.append("Recieved Signal : %s" % repr(args))

    def handleClick(self, lst):
        self.textMessages.append("Applications : %s " % ", ".join(lst))


def main():
    app = QApplication(sys.argv)
    win = mainWidget()
    win.show()
    app.exec_loop()

if __name__ == "__main__":
    main()

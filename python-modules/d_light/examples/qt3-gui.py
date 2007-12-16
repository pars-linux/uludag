#!/usr/bin/env python

import sys
import time

from qt import *

from d_light import d_light


class dbusEvent(QThread):
    def run(self):
        while 1:
            d_light.fetch()
            time.sleep(0.5)
            d_light.exec_()


class mainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # DBus
        d_light.init()
        self.thread = dbusEvent()
        self.thread.start()

        box = QVBoxLayout(self)

        self.buttonCall = QPushButton(self)
        self.buttonCall.setText('Push Me!')
        box.addWidget(self.buttonCall)

        self.textMessages = QTextEdit(self)
        box.addWidget(self.textMessages)

        # register signal handler
        d_light.registerSignal("type='signal'", self.handleSignal)

        self.connect(self.buttonCall, SIGNAL('clicked()'), self.slotClicked)

        self.resize(500, 300)

    def slotClicked(self):
        d_light.call("tr.org.pardus.comar", "/system", "tr.org.pardus.comar", "listApplications", (), self.handleClick)

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

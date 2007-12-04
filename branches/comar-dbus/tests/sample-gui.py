#!/usr/bin/env python

import random
import sys

import dbus
import dbus.mainloop.qt

from PyQt4.Qt import QWidget, QApplication, QPushButton, QTextEdit, QVBoxLayout, SIGNAL


class mainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()

        box = QVBoxLayout(self)

        self.buttonCall = QPushButton(self)
        self.buttonCall.setText('Push Me!')
        box.addWidget(self.buttonCall)

        self.textMessages = QTextEdit(self)
        box.addWidget(self.textMessages)

        self.connect(self.buttonCall, SIGNAL('clicked()'), self.slotCall)

        self.resize(500, 300)

    def slotCall(self):
        object = self.bus.get_object('tr.org.pardus.comar', '/package/apache', introspect=False)
        iface = dbus.Interface(object, 'System.Package')
        rand = random.randint(0, 10)
        self.textMessages.append("C: " + str(rand))
        iface.postInstall(rand, reply_handler=self.handleDBus, error_handler=self.handleDBus)

    def handleDBus(self, *args):
        self.textMessages.append("S: " + args[0])


def main():
    app = QApplication(sys.argv)
    win = mainWidget()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main()

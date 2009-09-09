#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, socket
from PyQt4.QtGui import QApplication


class FileSender:
    def __init__(self, FILE, HOST):
        self.CPORT = 9091
        self.MPORT = 9081
        self.file = FILE
        self.host = HOST
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendFile(self):
        self.cs.connect((self.host, self.CPORT))
        self.cs.send("SEND " + self.file)

    def waitforcheck(self)
        self.rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rs.bind(('', 9071))
        self.rs.listen(1)
        print '[Media] Listening on port 9081'
        self.rconn, self.raddr = this.rs.accept()
        if self.rconn:
            print "Requested"
        else:
            print "Not Requested"

    def sendContent(self):
        self.ms.connect((self.host, self.MPORT))
        f = open(self.file, "rb")
        self.data = f.read()
        f.close()
        self.ms.send(self.data)

    def close(self):
        self.cs.close()
        self.ms.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = FileSender('text.txt', '10.10.1.26')
    instance.sendFile()
    insatnce.waitforcheck()
    instance.sendContent()
    instance.close()
    app.exec_()

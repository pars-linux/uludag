#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, socket
from PyQt4.QtGui import QApplication


class FileSender:
    def __init__(self, FILE, HOST):
        self.port = 9091
        self.file = FILE
        self.host = HOST

    def sendFile(self):
        self.visitorSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.visitorSocket.connect((self.host, self.port))
        self.visitorSocket.send("SEND " + self.file)

    def waitforcheck(self):
        print '[Media] Waiting For Acception On Visitor'
        self.selfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.selfSocket.bind(('', self.port))
        self.selfSocket.listen(1)
        self.senderConn, self.senderAddr = self.selfSocket.accept()
        if self.senderAddr:
            print '[Media] Yep Accepted!'

    def sendContent(self):
        self.cs.connect((self.host, self.port))
        f = open(self.file, "rb")
        self.data = f.read()
        f.close()
        self.cs.send(self.data)

    def close(self):
        self.visitorSocket.close()
        self.selfSocket.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = FileSender('text.txt', '10.10.1.26')
    instance.sendFile()
    instance.waitforcheck()
    #instance.close()
    app.exec_()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, socket
from PyQt4.QtGui import QApplication


class FileSender:
    def __init__(self, FILE, HOST):
        self.port = 9091
        self.file = FILE
        self.host = HOST

        self.senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.selfSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendFile(self):
        self.senderSock.connect((self.host, self.port))
        self.senderSock.send("SEND " + self.file)

    def waitforcheck(self):
        print '[Media] Waiting For Acception On Visitor'
        self.selfSock.bind(('', self.port))
        self.selfSock.listen(1)
        self.selfConn, self.selfAddr = self.selfSock.accept()
        print self.selfAddr
        if self.selfAddr:
            f = open(self.file, "rb")
            print '[Media] Yep Accepted! Starting File Transfer...'
            self.data = f.read()
            self.senderSock.send(self.data)
            f.close()

    def close(self):
        self.senderSock.close()
        self.selfSock.close()

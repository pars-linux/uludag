#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, socket, os
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication
from preloader import ProgressBar


class FileSender(QtCore.QThread):

    def __init__(self, FILE, HOST):
        QtCore.QThread.__init__(self)
        self.port = 9091
        self.file = FILE
        self.host = HOST
        self.transferSize = 1024
        self.fileSize = 86687

        self.senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.selfSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.process()

    def sendFile(self):
        self.senderSock.connect((self.host, self.port))
        self.senderSock.send("SEND " + self.file)

    def waitforcheck(self):
        print '[Media] Waiting For Acception On Visitor'
        self.selfSock.bind(('', self.port))
        self.selfSock.listen(1)
        self.selfConn, self.selfAddr = self.selfSock.accept()
        if self.selfAddr:
            f = open(self.file, "rb")
            print '[Media] Accepted! Starting File Transfer...'
            self.data = f.read()
            self.senderSock.send(self.data)
            f.close()

    def process(self):
        while 1:
            self.sendFile()
            self.waitforcheck()

    def close(self):
        self.senderSock.close()
        self.selfSock.close()

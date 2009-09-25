#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, socket, os
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication
from preloader import ProgressBar
from receiver import StreamHandler

class FileSender(QtCore.QThread):

    def __init__(self, FILE, HOST):
        QtCore.QThread.__init__(self)
        self.port = 9091
        self.file = FILE
        self.host = HOST
        self.senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.process()

    def sendFile(self):
        self.senderSock.connect((self.host, self.port))
        self.senderSock.send("SEND " + self.file)

    def waitforcheck(self):
        print '[Media] Waiting For Acception On Visitor'
        self.StreamHandler.dataSock.listen(1)
        self.selfConn, self.selfAddr = self.StreamHandler.dataSock.accept()
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

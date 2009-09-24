#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, time, string, sys, urlparse
from threading import *
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *
from PyQt4 import QtGui
from PyQt4.QtGui import QApplication
from about import aboutData
from PyQt4.QtCore import *

class TransferHandler (QThread):

    def __init__( self, dataConn, filename ):
        QThread.__init__(self)
        KCmdLineArgs.init(sys.argv, aboutData)

    def run( self ):
        self.process()

    def sendInfo( self ):
        self.senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.senderSock.connect((self.dataAddr[0], 9091))
        self.senderSock.send(self.requestCheck)

    def process( self ):
        while 1:
            self.sendInfo()
            self.transfer()

    def transfer( self ):
        f = open(self.filename,"wb")
        while 1:
            data = self.dataConn.recv(1024)
            if not data: break
            f.write(data)
        f.close()

        print '[Media] Got "%s"' % self.filename
        print '[Media] Closing media transfer for "%s"' % self.filename

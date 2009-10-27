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

class StreamHandler (QThread):

    def __init__(self):
        QThread.__init__(self)
        self.dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataSock.bind(('', 9091))
        self.senderAddress = None
        KCmdLineArgs.init(sys.argv, aboutData)
        self.notification = KNotification("Request")
        self.notification.setActions(QStringList((i18n("Accept"), i18n("Reject"))))
        self.notification.setFlags(KNotification.Persistent)
        self.notification.setComponentData(KComponentData("pide","pide"))

    def run(self):
        self.process()

    def bindcsock( self ):
        print '[Control] Listening on port 9091...'

        self.dataSock.listen(1)
        self.dataConn, self.dataAddr = self.dataSock.accept()
        print '[Control] Got connection from', self.dataAddr


        data = self.dataConn.recv(1024)
        self.filename = self.getFileName(data)
        print '[Control] Getting ready to receive "%s"' % self.filename


    def checkrequest ( self ):
        if self.dataConn:
            message = i18n("<b> %1 </b> size <b> %2 </b> isimli dosyayı göndermek istiyor!", self.senderName(), self.filename)
            self.notification.setText(message)
            self.emit(SIGNAL("requestReceived()"))


    def receiverAccepted(self):
        print "Accepted!"

    def receiverDenied( self ):
        print "Denied!"

    def senderName(self):
        self.senderAddress = self.dataAddr[0]
        return self.senderAddress

    def process( self ):
        while 1:
            self.bindcsock()
            self.checkrequest()

    def getFileName( self, data ):
        name = data.split('/')
        return name[-1]


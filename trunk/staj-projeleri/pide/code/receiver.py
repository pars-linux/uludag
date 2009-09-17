#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, time, string, sys, urlparse
from threading import *
from PyQt4.QtGui import QApplication

class StreamHandler ( Thread ):

    def __init__( self ):
        Thread.__init__( self )
        self.KdeN = KNotification()
        self.dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataSock.bind(('', 9091))

    def run(self):
        self.process()

    def bindcsock( self ):
        print '[Control] Listening on port 9091...'

        self.dataSock.listen(1)

        self.dataConn, self.dataAddr = self.dataSock.accept()
        print '[Control] Got connection from', self.dataAddr

        data = self.dataConn.recv(1024)
        if data[0:4] == "SEND": self.filename = data[5:]
        print '[Control] Getting ready to receive "%s"' % self.filename


    def checkrequest ( self ):
        if self.dataConn:
            if self.notification:
                self.notification.close()
            self.notification = KNotification("Updates")
            self.notification.setText(i18n("There are <b>%s</b> waiting for answer!", self.filename))
            self.notification.setActions(QStringList((i18n("Yes"), i18n("Ignore"))))
            self.notification.setFlags(KNotification.Persistent)
            self.notification.setComponentData(KComponentData("package-manager","package-manager"))
            self.connect(self.notification, SIGNAL("action1Activated()"), self.receiverAccepted)
            self.notification.sendEvent()

    def receiverAccepted( self ):
        print "Accepted!"
        self.sendInfo()
        self.transfer()

    def receiverDenied( self ):
        print "Denied!"

    def sendInfo( self ):
        self.senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.senderSock.connect((self.dataAddr[0], 9091))
        self.senderSock.send(self.requestCheck)

    def transfer( self ):
        f = open(self.filename,"wb")
        self.KdeN.Notify(self.filename, self.dataAddr, "Dosya karşı taraftan alınıyor...")
        while 1:
            data = self.dataConn.recv(1024)
            if not data: break
            f.write(data)
        f.close()
        self.KdeN.Notify(self.filename, self.dataAddr, "Dosya karşı taraftan başarıyla alındı.")

        print '[Media] Got "%s"' % self.filename
        print '[Media] Closing media transfer for "%s"' % self.filename

    def process( self ):
        while 1:
            self.bindcsock()
            self.checkrequest()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = StreamHandler() 
    instance.start()
    app.exec_()

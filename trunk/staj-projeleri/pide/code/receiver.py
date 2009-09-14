#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, time, string, sys, urlparse
from threading import *
from PyQt4.QtGui import QApplication

# Application
from knotify import KNotification

class StreamHandler ( Thread ):

    def __init__( this ):
        Thread.__init__( this )
        this.KdeN = KNotification()
        this.receiverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(this):
        this.process()

    def bindcsock( this ):
        this.receiverSock.bind(('', 9091))
        this.receiverSock.listen(1)
        print '[Control] Listening on port 9091'
        this.senderConn, this.senderAddr = this.receiverSock.accept()
        print '[Control] Got connection from', this.senderAddr

        data = this.senderConn.recv(1024)
        if data[0:4] == "SEND": this.filename = data[5:]
        print '[Control] Getting ready to receive "%s"' % this.filename

    def checkrequest ( this ):
        m = "message"
        this.KdeN.Notify(this.filename, this.senderAddr, m)
        if this.senderConn:
            this.requestCheck = raw_input('Are You Sure (yes/no)? ')
            if this.requestCheck == "yes":
                this.sendInfo()
                this.transfer()
            else:
                print "Denied!"

    def sendInfo( this ):
        this.senderSock.connect(('10.10.1.26', 9091))
        this.senderSock.send(this.requestCheck)

    def transfer( this ):
        this.senderSock.listen(1)
        f = open(this.filename,"wb")
        while 1:
            data = this.receiverSock.recv(1024)
            if not data: break
            f.write(data)
        f.close()

        print '[Media] Got "%s"' % this.filename
        print '[Media] Closing media transfer for "%s"' % this.filename
    

    def process( this ):
        while 1:
            this.bindcsock()
            this.checkrequest()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = StreamHandler() 
    instance.start()
    app.exec_()

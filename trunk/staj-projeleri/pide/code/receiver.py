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
        this.dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.dataSock.bind(('', 9091))

    def run(this):
        this.process()

    def bindcsock( this ):
        print '[Control] Listening on port 9091...'

        this.dataSock.listen(1)

        this.dataConn, this.dataAddr = this.dataSock.accept()
        print '[Control] Got connection from', this.dataAddr

        data = this.dataConn.recv(1024)
        if data[0:4] == "SEND": this.filename = data[5:]
        print '[Control] Getting ready to receive "%s"' % this.filename


    def checkrequest ( this ):
        m = "message"
        this.KdeN.Notify(this.filename, this.dataAddr, m)
        if this.dataConn:
            this.requestCheck = raw_input('Are You Sure (yes/no)? ')
            if this.requestCheck == "yes":
                this.sendInfo()
                this.transfer()
            else:
                print "Denied!"

    def sendInfo( this ):
        this.senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.senderSock.connect(('10.10.1.26', 9091))
        this.senderSock.send(this.requestCheck)

    def transfer( this ):
        f = open(this.filename,"wb")
        while 1:
            data = this.dataConn.recv(1024)
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

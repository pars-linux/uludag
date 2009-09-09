#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, time, string, sys, urlparse
from threading import *
from PyQt4.QtGui import QApplication


class StreamHandler ( Thread ):

    def __init__( this ):
        Thread.__init__( this )

    def run(this):
        this.process()

    def bindmsock( this ):
        this.msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.msock.bind(('', 9081))
        this.msock.listen(1)
        print '[Media] Listening on port 9081'

    def acceptmsock( this ):
        this.mconn, this.maddr = this.msock.accept()
        print '[Media] Got connection from', this.maddr
    
    def bindcsock( this ):
        this.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.csock.bind(('', 9091))
        this.csock.listen(1)
        print '[Control] Listening on port 9091'

    def acceptcsock( this ):
        this.cconn, this.maddr = this.csock.accept()
        print '[Control] Got connection from', this.maddr

        data = this.cconn.recv(1024)
        if data[0:4] == "SEND": this.filename = data[5:]
        print '[Control] Getting ready to receive "%s"' % this.filename

    def checkrequest ( this ):
        print "Checking......"
        this.requestCheck = raw_input('Are You Sure(yes/no)? ')
        this.requestSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.requestSock.connect(('10.10.1.57', 9071))
        if this.requestCheck == "yes":
            this.requestSock.send('1')
            print '[Control] Accepted'
        else:
            this.requestSock.connect(('10.10.1.57', 9061))
            this.requestSock.send('0')
            print '[Control] Denied'

    def transfer( this ):
        print '[Media] Starting media transfer for "%s"' % this.filename

        f = open(this.filename,"wb")
        while 1:
            data = this.mconn.recv(1024)
            if not data: break
            f.write(data)
        f.close()

        print '[Media] Got "%s"' % this.filename
        print '[Media] Closing media transfer for "%s"' % this.filename
    
    def close( this ):
        this.cconn.close()
        this.csock.close()
        this.mconn.close()
        this.msock.close()

    def process( this ):
        while 1:
            this.bindcsock()
            this.acceptcsock()
            this.checkrequest()
            this.bindmsock()
            this.acceptmsock()
            this.transfer()
            this.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = StreamHandler() 
    instance.start()
    app.exec_()

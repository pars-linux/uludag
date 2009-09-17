#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, socket
from threading import *
from PyQt4.QtGui import QApplication


class FileSender( Thread ):

    def __init__(this, FILE, HOST):
        Thread.__init__( this )
        this.port = 9091
        this.file = FILE
        this.host = HOST

        this.senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.selfSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(this):
        this.process()

    def sendFile( this ):
        this.senderSock.connect((this.host, this.port))
        this.senderSock.send("SEND " + this.file)

    def waitforcheck( this ):
        print '[Media] Waiting For Acception On Visitor'
        this.selfSock.bind(('', this.port))
        this.selfSock.listen(1)
        this.selfConn, this.selfAddr = this.selfSock.accept()
        if this.selfAddr:
            f = open(this.file, "rb")
            print '[Media] Accepted! Starting File Transfer...'
            this.data = f.read()
            this.senderSock.send(this.data)
            f.close()

    def process( this ):
        while 1:
            this.sendFile()
            this.waitforcheck()

    def close( this ):
        this.senderSock.close()
        this.selfSock.close()

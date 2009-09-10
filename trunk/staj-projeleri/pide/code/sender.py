#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, socket
from PyQt4.QtGui import QApplication


class FileSender:
    def __init__(self, FILE, HOST):
        self.CPORT = 9091
        self.MPORT = 9081
        self.file = FILE
        self.host = HOST
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendFile(self):
        self.cs.connect((self.host, self.CPORT))
        self.cs.send("SEND " + self.file)

    def waitforcheck(self):
        self.acceptedSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.acceptedSocket.bind(('', 9071))
        self.acceptedSocket.listen(1)
        #self.deniedSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.deniedSocket.bind(('', 9061))
        #self.deniedSocket.listen(1)
        print '[Media] Listening on port 9071'
        self.raconn, self.raddr = self.acceptedSocket.accept()
        if self.raddr:
            print '[Media] Got Connection from:', self.raddr
        #self.rdconn = self.deniedSocket.accept()
        #if self.rdconn:
        #    print "Not Requested"

    def sendContent(self):
        self.ms.connect((self.host, self.MPORT))
        f = open(self.file, "rb")
        self.data = f.read()
        f.close()
        self.ms.send(self.data)


    def infoSocket(self):
        self.host = '10.10.0.26'
        self.port = 9001
        self.addr = (self.host, self.port)
        msgSocket = socket(AF_INET,SOCK_DGRAM)
        msgSocket.bind(addr)
        print "[Control] Connected To 9001"

    def getInfo(self):
        self.msg = "test 123"
        while (1):
            self.data = raw_input('>>')
            if not data:
                    break
            else:
                if(UDPSock.sendto(self.data,self.addr)):
                    print "Sending message '",data,"'....."

    def close(self):
        self.cs.close()
        self.ms.close()
        self.acceptedSocket.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    instance = FileSender('sender.py', '10.10.1.26')
    instance.sendFile()
    instance.waitforcheck()
    instance.sendContent()
    instance.close()
    app.exec_()

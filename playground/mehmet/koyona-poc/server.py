#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import thread
from socket import *
from threading import *

import shutil

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

APACHE_VHOST_CONF_FILE = "conf"
APACHE_VHOST_INSERT_AFTER = "class deneme {\n"

def handler(clientsock, addr):
    while 1:
        data = clientsock.recv(BUFFER_SIZE)
        if not data:
            break
        cmd = data.split(":=:")
        if cmd[0] == "savevhost":
            savevhost(clientsock, cmd[1])
        elif cmd[0] == "getlog":
            sendlog(clientsock)
        clientsock.send(data.upper())

    clientsock.close()

def savevhost(clientsock, params):
    #print "savechost func"
    pa = params.split(":")
    fd = open(APACHE_VHOST_CONF_FILE, "r")
    fdout = open("tmp", "w+")
    for line in fd:
        line.rstrip()
        if line == APACHE_VHOST_INSERT_AFTER:
            fdout.write(line)
            fdout.write("\tapache::vhost { \""+pa[2]+"."+pa[3]+"\":\n")
            fdout.write("\t\tid => \""+pa[0]+"\",\n")
            fdout.write("\t\tport => \""+pa[1]+"\",\n")
            fdout.write("\t\tvhost => \""+pa[2]+"\",\n")
            fdout.write("\t\tdomain => \""+pa[3]+"\",\n")
            fdout.write("\t\taliases => \""+pa[4]+"\",\n")
            fdout.write("\t}\n\n")
        else:
            fdout.write(line)
    shutil.move("tmp", APACHE_VHOST_CONF_FILE)
    fd.close()
    fdout.close()

def sendlog(clientsock):
    print "send log"

def main(args):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)#adres already in use için
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while 1:
        print "bağlantı bekleniyor..."
        conn, addr = s.accept()
        print 'Connection address:', addr
        thread.start_new_thread(handler, (conn, addr))

if __name__=="__main__":
    main(sys.argv)


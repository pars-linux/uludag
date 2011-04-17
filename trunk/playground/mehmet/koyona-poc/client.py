#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
import re
import time
import socket
from qt import *

import dbus
import dbus.mainloop.qt3

from kdecore import *
from kdeui import *
import kdedesigner

import thread

from threading import Thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

def getIcon(name, group=KIcon.Small):
    return KGlobal.iconLoader().loadIcon(name, group)

def AboutData():
    global version, description

    about_data = KAboutData("sample-application",
                            "Sample",
                            "1.0.2",
                            "A sample application",
                            KAboutData.License_GPL,
                            '(C) 2005-2011 UEKAE/TUBITAK',
                            None, None,
                            'mehmet@pardus.org.tr')

    about_data.addAuthor('Mehmet Özdemir', None, 'mehmet@pardus.org.tr')

    return about_data

class MainApplication(QDialog):
    def __init__(self, parent=None, name=None):
        QDialog.__init__(self, parent, name)
        self.setCaption("Proof of concept")

        #mainLayout = QHBoxLayout(self)

        self.isConnected = False
        self.inOperation = False

        mainLayout = QGridLayout(self, 0, 0, 4, 4)
        topRow = mainLayout.numRows()
        self.ipedit = QLineEdit(self)
        self.ipedit.setText("127.0.0.1")
        self.tab = QTabWidget(self)

        self.log = QTextEdit(self)

        vhostWidget = QWidget(self)
        vhostLayout = QGridLayout(vhostWidget, 0, 0)

        self.id = QLineEdit(vhostWidget)
        self.port = QLineEdit(vhostWidget)
        self.vhost = QLineEdit(vhostWidget)
        self.domain = QLineEdit(vhostWidget)
        self.aliases = QLineEdit(vhostWidget)

        idRow = 0
        vhostLayout.addMultiCellWidget(QLabel("ID:", vhostWidget), idRow, idRow, 0, 0)
        vhostLayout.addMultiCellWidget(self.id, idRow, idRow, 1, 2)

        portRow = 1
        vhostLayout.addMultiCellWidget(QLabel("Port:", vhostWidget), portRow, portRow, 0, 0)
        vhostLayout.addMultiCellWidget(self.port, portRow, portRow, 1, 2)

        vhostRow = 2
        vhostLayout.addMultiCellWidget(QLabel("Vrtiual Host:", vhostWidget), vhostRow, vhostRow, 0, 0)
        vhostLayout.addMultiCellWidget(self.vhost, vhostRow, vhostRow, 1, 2)

        domainRow = 3
        vhostLayout.addMultiCellWidget(QLabel("Domain:", vhostWidget), domainRow, domainRow, 0, 0)
        vhostLayout.addMultiCellWidget(self.domain, domainRow, domainRow, 1, 2)

        aliasesRow = 4
        vhostLayout.addMultiCellWidget(QLabel("Aliases:", vhostWidget), aliasesRow, aliasesRow, 0, 0)
        vhostLayout.addMultiCellWidget(self.aliases, aliasesRow, aliasesRow, 1, 2)

        self.saveButton = QPushButton("Save", vhostWidget)
        vhostLayout.addMultiCellWidget(self.saveButton, 5, 5, 2, 2)

        self.tab.addTab(vhostWidget, "Apache - Virtual Host")
        self.tab.addTab(self.log, "Log")

        self.connect(self.tab, SIGNAL("currentChanged(QWidget*)"), self.slotTabChanged)
        self.connectButton = QPushButton("Connect", self)

        self.info = QLabel("...", self)
        self.info.setPaletteForegroundColor(QColor(41, 182, 31))


        self.connect(self.saveButton, SIGNAL("clicked()"), self.slotSave)
        self.connect(self.connectButton, SIGNAL("clicked()"), self.slotConnect)

        mainLayout.addWidget(QLabel("Server:", self), topRow, 0)
        mainLayout.addWidget(self.ipedit, topRow, 1)
        mainLayout.addWidget(self.connectButton, topRow, 2)

        tabRow = mainLayout.numRows()
        mainLayout.addMultiCellWidget(self.tab, tabRow, tabRow, 0, 2)

        infoRow = mainLayout.numRows()
        mainLayout.addMultiCellWidget(self.info, infoRow, infoRow, 0, 2)

    def receiver(self):
        while 1:
            received = self.sock.recv(1024)
            if not received:
                print "breaked"
                break
            print 'received', len(received), 'bytes'
            print received
            self.connectButton.setEnabled(True)

    def slotTabChanged(self, w):
        self.info.setPaletteForegroundColor(QColor(41, 182, 31))
        self.info.setText("selected tab = %s" % w)

    def checkValues(self):
        self.info.setPaletteForegroundColor(QColor(255, 0, 0))
        if not self.isConnected:
            self.info.setText("Error: No connection")
            return True

        if not self.id.text():
            self.info.setText("Error: ID is needed")
            return True

        if not self.vhost.text():
            self.info.setText("Error: Virtual host is needed")
            return True

        if not self.domain.text():
            self.info.setText("Error: Domain is needed")
            return True

        if not self.aliases.text():
            self.info.setText("Error: Aliases is needed")
            return True

        self.info.setPaletteForegroundColor(QColor(41, 182, 31))
        return False

    def slotSave(self):
        if self.checkValues():
            return
        self.connectButton.setEnabled(False)
        if not self.port.text():
            port = "*"
        else:
            port = self.port.text()
        data = "savevhost:=:"+self.id.text()+":"+port+":"+self.vhost.text()+":"+self.domain.text()+":"+self.aliases.text()
        #data += 
        self.sock.send(bytes(data).decode('utf-8'))
        return

    def slotConnect(self):
        if self.connectButton.text() == "&Connect":

            if not self.ipedit.text():
                self.info.setPaletteForegroundColor(QColor(255, 0, 0))
                self.info.setText("Error: Write an IP address for server")
                return

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.sock.connect((TCP_IP, TCP_PORT))
                KMessageBox.sorry(self, unicode("Bağlantı kuruldu"), 'Error')
            except Exception, e:
                KMessageBox.sorry(self, unicode(e), 'Error')
                return
            #self.sock.send("blah balhajjj")
            #data = self.sock.recv(BUFFER_SIZE)
            #s.close()

            #print "received data:", data

            self.connectButton.setText("Disconnect")
            self.isConnected = True

            thread.start_new_thread(self.receiver, ())

        else:
            self.sock.close()

            self.connectButton.setText("Connect")
            self.isConnected = False


def main(args):
    global kapp
    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print "This application already running"
        return
    kapp = KUniqueApplication(True, True, True)
    app = MainApplication()
    app.resize(QSize(600, 400).expandedTo(app.minimumSizeHint()))
    kapp.setMainWidget(app)
    sys.exit(app.exec_loop())

if __name__=="__main__":
        main(sys.argv)




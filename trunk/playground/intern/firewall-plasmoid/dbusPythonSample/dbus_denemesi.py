# -*- coding: utf-8 -*-
#! /usr/bin/python
#This file is cretead by Baris Akkurt to learn how to send a message over the bus in Python.
#self.powerdevil = self.sessionBus.get_object('org.kde.screensaver', '/App')  lines like this are messages that
#sent over d-bus. you can use d-bus or qdbusplasmoidviewe program to learn the interfaces.


import sys
 
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication
 
from PyQt4.QtGui import QLabel, QWidget, QPushButton, QBoxLayout
from PyQt4.QtCore import Qt, QObject, SIGNAL
 
import dbus
 
class MainWindow (QWidget):
    def __init__ (self):
        QWidget.__init__ (self)
        

        self.sessionBus = dbus.SessionBus()
        self.systemBus = dbus.SystemBus()
        
        self.powerdevil = self.sessionBus.get_object('org.kde.screensaver', '/App') 
        self.powerdevil2 = self.sessionBus.get_object('org.kde.screensaver', '/ScreenSaver') 
        #self.powerdevil3 = self.sessionBus.get_object('org.kde.kopete', '/Kopete') 
        #self.powerdevil4 = self.sessionBus.get_object('org.kde.kopete', '/Kopete') 
        #self.powerdevil5 = self.sessionBus.get_object('org.kde.kopete', '/Kopete') 
        self.powerdevil6 = self.sessionBus.get_object('org.kde.plasma-desktop', '/App') 
        #self.powerdevil7 = self.sessionBus.get_object('org.kde.yakuake', '/yakuake/MainWindow_1') 
        #self.powerdevil8 = self.sessionBus.get_object('org.kde.amarok', '/Player') 
        #self.sistemeGonder=self.systemBus.get_object('tr.org.pardus.comar','/package/iptables')
        self.sistemeGonder=self.systemBus.get_object('tr.org.pardus.comar','/package/openssh')
        
        
        self.layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.setLayout(self.layout)
        
        label = QLabel ("bir program", self)
        self.layout.addWidget(label)
 
	button0 = QPushButton("comarrr!", self)
        self.layout.addWidget(button0)
        button = QPushButton("yazdir!", self)
        self.layout.addWidget(button)
        button2 = QPushButton("ekrani kilitle!", self)
        self.layout.addWidget(button2)
        button3 = QPushButton("kopete baglantisini kes!", self)
        self.layout.addWidget(button3)
        button4 = QPushButton("canerle sohbet baslat!", self)
        self.layout.addWidget(button4)
        button6 = QPushButton("dashboardı goster!", self)
        self.layout.addWidget(button6)
        button7 = QPushButton("yakuake yi toogle et!", self)
        self.layout.addWidget(button7)
        button8 = QPushButton("amarok baslat/duraklat!", self)
        self.layout.addWidget(button8)
 
	QObject.connect(button0, SIGNAL("clicked()"), self.screenOff0)
        QObject.connect(button, SIGNAL("clicked()"), self.screenOff)
        QObject.connect(button2, SIGNAL("clicked()"), self.screenOff2)
        QObject.connect(button3, SIGNAL("clicked()"), self.screenOff3)
        QObject.connect(button4, SIGNAL("clicked()"), self.screenOff4)
        QObject.connect(button6, SIGNAL("clicked()"), self.screenOff6)
        QObject.connect(button7, SIGNAL("clicked()"), self.screenOff7)
        QObject.connect(button8, SIGNAL("clicked()"), self.screenOff8)
        
        self.resize (640, 480)
 
    def screenOff(self):
        self.powerdevil.showTaskManager(dbus_interface='org.kde.krunner.App')
    def screenOff2(self):
        self.powerdevil2.Lock(dbus_interface='org.freedesktop.ScreenSaver')
    def screenOff3(self):
        self.powerdevil3.disconnectAll(dbus_interface='org.kde.Kopete')
    def screenOff4(self):
        self.powerdevil3.openChat("canerbasaran@jabber.pardus.org.tr", dbus_interface='org.kde.Kopete')
    def screenOff6(self):
        self.powerdevil6.showDashboard(True, dbus_interface='local.PlasmaApp')
    def screenOff7(self):
        self.powerdevil7.toggleWindowState(dbus_interface='org.kde.yakuake')
    def screenOff8(self):
        self.powerdevil8.PlayPause(dbus_interface='org.freedesktop.MediaPlayer')
    def screenOff0(self):
	#self.sistemeGonder.start(dbus_interface='tr.pardus.comar.System.Service')
	self.sistemeGonder.start(dbus_interface='tr.pardus.comar.System.Service')
        
if __name__ == '__main__':
    appName     = "DBusApp"
    catalog     = ""
    programName = ki18n ("DBus Example Application")
    version     = "1.0"
    description = ki18n ("DBus Example")
    license     = KAboutData.License_GPL
    copyright   = ki18n ("(c) 2009 Andrew Stromme")
    text        = ki18n ("none")
    homePage    = "http://blog.chatonka.com"
    bugEmail    = "astromme@chatonka.com"
 
    aboutData   = KAboutData (appName, catalog, programName, version, description,
                                license, copyright, text, homePage, bugEmail)

    KCmdLineArgs.init (sys.argv, aboutData)
 
    app = KApplication ()
    mainWindow = MainWindow ()
    mainWindow.show ()
    app.exec_ ()
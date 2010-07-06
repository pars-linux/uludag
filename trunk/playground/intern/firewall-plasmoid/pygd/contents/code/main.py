# -*- coding: utf-8 -*-
# Copyright stuff

#Firewall plasmoid try in Python by Baris Akkurt

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout
from PyQt4.QtGui import QGridLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import comar
import dbus
from PyQt4.QtCore import *


if not dbus.get_default_main_loop():
    from dbus.mainloop.qt import DBusQtMainLoop
    DBusQtMainLoop(set_as_default=True)

 
class HelloWorldApplet(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
        
    def baslat(self):
	link=comar.Link()#comar baglantisi
	#link.System.Service[dbus.String("iptables")].start()#onemli satirlar bunlar
	link.Network.Firewall[dbus.String("iptables")].setState("on")
	#link.System.Service[dbus.String("iptables")].start(async=self.handler)
	self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")

    def durdur(self):
	link=comar.Link()
	#link.System.Service[dbus.String("iptables")].stop()
	link.Network.Firewall[dbus.String("iptables")].setState("off")
	#link.System.Service[dbus.String("iptables")].start(async=self.handler)
	self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
	
 
    def init(self):
	link=comar.Link()
	#gs=link.Network.Firewall[dbus.String("iptables")].getState()
	#print gs
	self.typeOf, self.description, self.stateOfFirewall=link.System.Service[dbus.String("iptables")].info()
	#print self.stateOfFirewall
	#print type(self.stateOfFirewall)
        self.setHasConfigurationInterface(True)#burası true olacak sanırım ayar penceresi için
        self.setAspectRatioMode(Plasma.Square)
 
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        label = Plasma.Label(self.applet)
        label.setText("<h1>Firewall Plasmoid</h1>")
        
        self.bilgi_label=Plasma.Label(self.applet)
        #self.bilgi_label.setText("")
        #link.Network.Firewall[dbus.String("iptables")].getState()
        if link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):      #self.stateOfFirewall==dbus.String("on"):
	    self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")
	else:
	    self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
        baslat_pb=Plasma.PushButton(self.applet)
        baslat_pb.setText("Start")
        durdur_pb=Plasma.PushButton(self.applet)
        durdur_pb.setText("Stop")
        self.layout.addItem(label)
        self.layout.addItem(baslat_pb)
        self.layout.addItem(durdur_pb)
        self.layout.addItem(self.bilgi_label)
        self.applet.setLayout(self.layout)
        self.resize(125,125)
        
        QObject.connect(baslat_pb, SIGNAL("clicked()"), self.baslat)
        QObject.connect(durdur_pb, SIGNAL("clicked()"), self.durdur)
        
        link.listenSignals("Network.Firewall", self.handler)

    def handler(self, *args):
	link=comar.Link()
	if link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):      #self.stateOfFirewall==dbus.String("on"):
	    self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")
	else:
	    self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
	#pass
      
 
def CreateApplet(parent):
    return HelloWorldApplet(parent) 

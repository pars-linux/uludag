# -*- coding: utf-8 -*-
from PyQt4.QtCore import Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import QGraphicsGridLayout
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QPixmap
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import comar, dbus

if not dbus.get_default_main_loop():
    from dbus.mainloop.qt import DBusQtMainLoop
    DBusQtMainLoop(set_as_default=True)
 
class HelloWorldApplet(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
	
    def init(self):
	#self.moduller=self.link.Network.Firewall[dbus.String("iptables")].listModules()
	
	self.tahta=[[0,0,0],[0,0,0],[0,0,0]]
	
        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.Square)
        self.resize(450,250)
 
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.layout=QGraphicsGridLayout(self.applet)
        
        #label = Plasma.Label(self.applet)
        #label.setText("<h1>Firewall Plasmoid</h1>")
        #self.kilit=Plasma.IconWidget(self.applet)
        #self.bilgi_label=Plasma.Label(self.applet)
        
        #self.baslat_pb=Plasma.PushButton(self.applet)
        #self.baslat_pb.setText("Start")
        #self.durdur_pb=Plasma.PushButton(self.applet)
        #self.durdur_pb.setText("Stop")
        
        self.tus1=Plasma.PushButton(self.applet)
	self.tus1.setText("")
	self.tus2=Plasma.PushButton(self.applet)
	self.tus2.setText("")
	self.tus3=Plasma.PushButton(self.applet)
	self.tus3.setText("")
	
	self.tus4=Plasma.PushButton(self.applet)
	self.tus4.setText("")
	self.tus5=Plasma.PushButton(self.applet)
	self.tus5.setText("")
	self.tus6=Plasma.PushButton(self.applet)
	self.tus6.setText("")
	
	self.tus7=Plasma.PushButton(self.applet)
	self.tus7.setText("")
	self.tus8=Plasma.PushButton(self.applet)
	self.tus8.setText("")
	self.tus9=Plasma.PushButton(self.applet)
	self.tus9.setText("")
        
        self.layout.addItem(self.tus1, 0, 0)
        self.layout.addItem(self.tus2, 0, 1)
        self.layout.addItem(self.tus3, 0, 2)
        self.layout.addItem(self.tus4, 1, 0)
        self.layout.addItem(self.tus5, 1, 1)
        self.layout.addItem(self.tus6, 1, 2)
        self.layout.addItem(self.tus7, 2, 0)
        self.layout.addItem(self.tus8, 2, 1)
        self.layout.addItem(self.tus9, 2, 2)
        self.applet.setLayout(self.layout)        
        
        #QObject.connect(self.baslat_pb, SIGNAL("clicked()"), self.baslat)
        #QObject.connect(self.durdur_pb, SIGNAL("clicked()"), self.durdur)
        
    def hamle_yap(self):
	pass
    
def CreateApplet(parent):
    return HelloWorldApplet(parent) 

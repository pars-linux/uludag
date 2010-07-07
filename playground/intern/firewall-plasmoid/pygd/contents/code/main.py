# -*- coding: utf-8 -*-
#
# Copyright 2010 D. Barış Akkurt <dbarisakkurt@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation; either version 2, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details
#
# You should have received a copy of the GNU Library General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

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
	"""Regular init method for the class of the plasmoid"""
        plasmascript.Applet.__init__(self,parent)
        
    def baslat(self):
	"""Method for openning the firewall manager"""
	link=comar.Link()
	link.Network.Firewall[dbus.String("iptables")].setState("on")
	self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")

    def durdur(self):
	"""Method for closing the firewall manager"""
	link=comar.Link()
	link.Network.Firewall[dbus.String("iptables")].setState("off")
	self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
	
    def blockGelen(self, value):
        if self.incoming_cb.isChecked():
	    link=comar.Link()
	    link.Network.Firewall[dbus.String("iptables")].setModuleState("block_incoming","on")
	else:
	    link=comar.Link()
	    link.Network.Firewall[dbus.String("iptables")].setModuleState("block_incoming","off")
	    
    def paylasim(self, value):
        if self.incoming_cb.isChecked():
	    #print "cek edilmis2"
	    link=comar.Link()
	    link.Network.Firewall[dbus.String("iptables")].setModuleState("internet_sharing","on")
	else:
	    link=comar.Link()
	    link.Network.Firewall[dbus.String("iptables")].setModuleState("internet_sharing","off")
	    #print "edilmemis2"

    def blockGiden(self, value):
        if self.incoming_cb.isChecked():
	    link=comar.Link()
	    link.Network.Firewall[dbus.String("iptables")].setModuleState("block_outgoing","on")
	    #print "cek edilmis3"
	else:
	    link=comar.Link()
	    link.Network.Firewall[dbus.String("iptables")].setModuleState("block_outgoing","off")
	    #print "edilmemis3"

	
    def init(self):
	"""init method for the plasmoid. GUI stuff is located here."""
	link=comar.Link()

        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.Square)
        self.resize(400,200)
 
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.layout=QGraphicsGridLayout(self.applet)
        
        label = Plasma.Label(self.applet)
        label.setText("<h1>Firewall Plasmoid</h1>")
        self.kilit=Plasma.IconWidget(self.applet)
        self.bilgi_label=Plasma.Label(self.applet)

        if link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):
	    self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")
	    self.kilit.setIcon("object-locked")
	    self.kilit.setMaximumWidth(40)
	else:
	    self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
	    self.kilit.setMaximumWidth(40)
	    self.kilit.setIcon("object-unlocked")

        baslat_pb=Plasma.PushButton(self.applet)
        baslat_pb.setText("Start")
        durdur_pb=Plasma.PushButton(self.applet)
        durdur_pb.setText("Stop")
        
        gelen_simge=Plasma.IconWidget(self.applet)
        gelen_simge.setIcon("application-x-smb-workgroup")
        paylasim_simge=Plasma.IconWidget(self.applet)
        paylasim_simge.setIcon("application-x-smb-server")
        giden_simge=Plasma.IconWidget(self.applet)
        giden_simge.setIcon("security-medium")
        
        self.incoming_cb=Plasma.CheckBox(self.applet)
        self.incoming_cb.setText("Block incoming connections")
        self.shareint_cb=Plasma.CheckBox(self.applet)
        self.shareint_cb.setText("Sharing internet")
        self.outgoing_cb=Plasma.CheckBox(self.applet)
        self.outgoing_cb.setText("Block outgoing connections")
        
        self.layout.addItem(label, 0, 0,1,4)
        self.layout.addItem(self.kilit, 1,0)
        self.layout.addItem(self.bilgi_label,1,1)
        self.layout.addItem(baslat_pb,1,2)
        self.layout.addItem(durdur_pb,1,3)
        self.layout.addItem(gelen_simge,2,0,1,1)
        self.layout.addItem(paylasim_simge,3,0,1,1)
        self.layout.addItem(giden_simge,4,0,1,1)
        self.layout.addItem(self.incoming_cb,2,1,1,4)
        self.layout.addItem(self.shareint_cb,3,1,1,4)
        self.layout.addItem(self.outgoing_cb,4,1,1,4)
        self.applet.setLayout(self.layout)        
        
        QObject.connect(baslat_pb, SIGNAL("clicked()"), self.baslat)
        QObject.connect(durdur_pb, SIGNAL("clicked()"), self.durdur)
        QObject.connect(self.incoming_cb, SIGNAL("toggled(bool)"), self.blockGelen)
        QObject.connect(self.shareint_cb, SIGNAL("toggled(bool)"), self.paylasim)
        QObject.connect(self.outgoing_cb, SIGNAL("toggled(bool)"), self.blockGiden)
        
        link.listenSignals("Network.Firewall", self.handler)
        
    def handler(self, *args):
	"""Handler method for receiving signals from Comar"""
	link=comar.Link()
	if link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):
	    self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")
	    self.kilit.setIcon("object-locked")
	else:
	    self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
	    self.kilit.setIcon("object-unlocked")
	
	if link.Network.Firewall[dbus.String("iptables")].getModuleState("block_incoming")==dbus.String(u"on"):
	    self.incoming_cb.setChecked(True)
	else:
	    self.incoming_cb.setChecked(False)
	    
	if link.Network.Firewall[dbus.String("iptables")].getModuleState("internet_sharing")==dbus.String(u"on"):
	    self.shareint_cb.setChecked(True)
	else:
	    self.shareint_cb.setChecked(False)
	
	if link.Network.Firewall[dbus.String("iptables")].getModuleState("block_outgoing")==dbus.String(u"on"):
	    self.outgoing_cb.setChecked(True)
	else:
	    self.outgoing_cb.setChecked(False)

def CreateApplet(parent):
    return HelloWorldApplet(parent) 

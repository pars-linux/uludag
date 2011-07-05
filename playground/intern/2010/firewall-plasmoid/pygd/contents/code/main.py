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
        self.link=comar.Link()
        
    def baslat(self):
	"""Method for openning the firewall manager"""
	try:#################try blogu eklendi burasi yapilacak.
	    self.link.Network.Firewall[dbus.String("iptables")].setState("on")
	    self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")
	    self.bilgilendirme.setText("Firewall has been started succesfully.")
	    self.baslat_pb.setEnabled(False)
	    self.durdur_pb.setEnabled(True)
	except dbus.exceptions.DBusException as hata:
	    self.bilgilendirme.setText(u"ERROR: Operation didn't perform.")
	    #print "HATA=",hata
	    

    def durdur(self):
	"""Method for closing the firewall manager"""
	try:
	    self.link.Network.Firewall[dbus.String("iptables")].setState("off")
	    self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
	    self.bilgilendirme.setText("Firewall has been stopped succesfully.")
	    self.durdur_pb.setEnabled(False)
	    self.baslat_pb.setEnabled(True)
	except dbus.exceptions.DBusException as hata:
	    self.bilgilendirme.setText(u"ERROR: Operation didn't perform.")
	    
	
    def blockGelen(self, value):
        if self.kutular[0].isChecked():
	    self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_incoming","on")
	    self.bilgilendirme.setText(self.bilgilendirme_iletileri[0])
	else:
	    self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_incoming","off")
	    self.bilgilendirme.setText("Incoming connection blocking was stopped")
	    
    def paylasim(self, value):
        if self.kutular[1].isChecked():
	    self.link.Network.Firewall[dbus.String("iptables")].setModuleState("internet_sharing","on")
	    self.bilgilendirme.setText(self.bilgilendirme_iletileri[1])
	else:
	    self.link.Network.Firewall[dbus.String("iptables")].setModuleState("internet_sharing","off")
	    self.bilgilendirme.setText("Sharing internet was stopped")

    def blockGiden(self, value):
        if self.kutular[2].isChecked():
	    self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_outgoing","on")
	    self.bilgilendirme.setText(self.bilgilendirme_iletileri[2])
	else:
	    self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_outgoing","off")
	    self.bilgilendirme.setText("Outgoing connection blocking was stopped")
	
    def init(self):
	"""init method for the plasmoid. GUI stuff is located here."""
	
	self.moduller=self.link.Network.Firewall[dbus.String("iptables")].listModules()
	
        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.Square)
        self.resize(450,250)
 
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.layout=QGraphicsGridLayout(self.applet)
        
        label = Plasma.Label(self.applet)
        label.setText("<h1>Firewall Plasmoid</h1>")
        self.kilit=Plasma.IconWidget(self.applet)
        self.bilgi_label=Plasma.Label(self.applet)
        
        self.baslat_pb=Plasma.PushButton(self.applet)
        self.baslat_pb.setText("Start")
        self.durdur_pb=Plasma.PushButton(self.applet)
        self.durdur_pb.setText("Stop")
	print "osman"
        if self.link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):
	    self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")
	    self.kilit.setIcon("object-locked")
	    self.kilit.setMaximumSize(32,32)
	    self.kilit.setMinimumSize(32,32)
	    self.baslat_pb.setEnabled(False)
	    
	else:
	    self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
	    self.kilit.setMaximumSize(32,32)
	    self.kilit.setMinimumSize(32,32)
	    self.kilit.setIcon("object-unlocked")
	    self.durdur_pb.setEnabled(False)
	
	self.bilgilendirme_baslik=Plasma.Label(self.applet)
	self.bilgilendirme_baslik.setText("Latest news:")
	
	self.bilgilendirme=Plasma.Label(self.applet)
	self.bilgilendirme.setText("Firewall Plasmoid has been started.")

        gelen_simge=Plasma.IconWidget(self.applet)
        gelen_simge.setIcon("application-x-smb-workgroup")
        paylasim_simge=Plasma.IconWidget(self.applet)
        paylasim_simge.setIcon("application-x-smb-server")
        giden_simge=Plasma.IconWidget(self.applet)
        giden_simge.setIcon("security-medium")
        
        self.kutular=[]
        sayi=0
        for i in self.moduller:
	    self.kutular.append(Plasma.CheckBox(self.applet))
	    self.kutular[sayi].setText(self.link.Network.Firewall[dbus.String("iptables")].moduleInfo(i)[0])
	    sayi+=1
	    
        
        self.layout.addItem(label, 0, 0,1,4)
        self.layout.addItem(self.kilit, 1,0)
        self.layout.addItem(self.bilgi_label,1,1)
        self.layout.addItem(self.baslat_pb,1,2)
        self.layout.addItem(self.durdur_pb,1,3)
        self.layout.addItem(gelen_simge,2,0,1,1)
        self.layout.addItem(paylasim_simge,3,0,1,1)
        self.layout.addItem(giden_simge,4,0,1,1)
        self.layout.addItem(self.bilgilendirme_baslik, 5,0,1,1)
        self.layout.addItem(self.bilgilendirme, 5,1,1,4)
        m=0
        for i in range(0,len(self.moduller)):
	    self.layout.addItem(self.kutular[m], m+2,1,1,4)
	    m+=1
        self.applet.setLayout(self.layout)        
        
        QObject.connect(self.baslat_pb, SIGNAL("clicked()"), self.baslat)
        QObject.connect(self.durdur_pb, SIGNAL("clicked()"), self.durdur)
        
        fonksiyonlar=[self.blockGelen, self.paylasim, self.blockGiden]
        for i in range(0, len(self.moduller)):
	    QObject.connect(self.kutular[i], SIGNAL("toggled(bool)"), fonksiyonlar[i])
	    
	self.bilgilendirme_iletileri=["Incoming connections was blocked successfully.",
	"Sharing internet is successful.",
	"Outgoing connections was blocked successfully."]
        
        self.link.listenSignals("Network.Firewall", self.handler)
        
        
    def handler(self, *args):
	"""Handler method for receiving signals from Comar"""
	if self.link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):
	    self.bilgi_label.setText("<p style='color:green'>Firewall is working now.</p>")
	    self.kilit.setIcon("object-locked")
	    self.durdur_pb.setEnabled(True)
	    self.baslat_pb.setEnabled(False)
	    #print "baslat sinyali"
	else:
	    self.bilgi_label.setText("<p style='color:red'>Firewall is stopped now.</p>")
	    self.kilit.setIcon("object-unlocked")
	    self.durdur_pb.setEnabled(False)
	    self.baslat_pb.setEnabled(True)
	    #print "durdur sinyali"
	
	if self.link.Network.Firewall[dbus.String("iptables")].getModuleState("block_incoming")==dbus.String(u"on"):
	    self.kutular[0].setChecked(True)
	    #print "ilk kutu tiklandi sinyali"
	else:
	    self.kutular[0].setChecked(False)
	    #print "ilk kutu tiki kaldirildi sinyali"
	    
	if self.link.Network.Firewall[dbus.String("iptables")].getModuleState("internet_sharing")==dbus.String(u"on"):
	    self.kutular[1].setChecked(True)
	    #print "ikinci kutu tiklandi sinyali"
	else:
	    self.kutular[1].setChecked(False)
	    #print "ikinci kutu tiki kaldirildi sinyali"
	
	if self.link.Network.Firewall[dbus.String("iptables")].getModuleState("block_outgoing")==dbus.String(u"on"):
	    self.kutular[2].setChecked(True)
	    #print "ucuncu kutu tiklandi sinyali"
	else:
	    self.kutular[2].setChecked(False)
	    #print "ucuncu kutu tiki kaldirildi sinyali"

def CreateApplet(parent):
    return HelloWorldApplet(parent) 

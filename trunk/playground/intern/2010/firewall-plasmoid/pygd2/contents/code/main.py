# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QCheckBox, QPixmap, QSizePolicy, QGraphicsGridLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import comar, dbus

if not dbus.get_default_main_loop():
    from dbus.mainloop.qt import DBusQtMainLoop
    DBusQtMainLoop(set_as_default=True)

class FirewallApplet(plasmascript.Applet):
    def __init__(self,parent,args=None):
	"""Regular init method for the class of the plasmoid"""
        plasmascript.Applet.__init__(self,parent)
        self.link=comar.Link()
    
    def onOff(self):
	"""Method for openning and closing the firewall manager"""
	if self.link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"off"):
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setState("on")
		self.onOff_pb.setText("Stop")
		self.lock_icon.setIcon("object-locked")
		self.onOffInfo_label.setText("<p style='color:green'><h3>Firewall status: ON</h3></p>")
		self.infoBar_label.setText("Firewall was started.")
	    except dbus.DBusException, e:
		self.onOff_pb.setText("Start")
		self.lock_icon.setIcon("object-unlocked")
		self.onOffInfo_label.setText("<p style='color:red'><h3>Firewall status: OFF</h3></p>")
		self.infoBar_label.setText("ERROR: Firewall didn't start.")
	else:
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setState("off")
		self.onOff_pb.setText("Start")
		self.lock_icon.setIcon("object-unlocked")
		self.onOffInfo_label.setText("<p style='color:red'><h3>Firewall status: OFF</h3></p>")
		self.infoBar_label.setText("Firewall was stopped.")
	    except dbus.DBusException:
		self.onOff_pb.setText("Stop")
		self.lock_icon.setIcon("object-locked")
		self.onOffInfo_label.setText("<p style='color:green'><h3>Firewall status: ON</h3></p>")
		self.infoBar_label.setText("ERROR: Firewall didn't stop.")
	      
    def blockIncoming(self):
	"""Blocks the incoming"""
	if self.checkboxes[0].isChecked():
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_incoming","on")
		self.infoBar_label.setText("Incoming connections were blocked.")
	    except dbus.DBusException:
		self.infoBar_label.setText("ERROR: Incoming connections couldn't be blocked.")
		self.checkboxes[0].setChecked(False)
	else:
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_incoming","off")
		self.infoBar_label.setText("Incoming connection blockade was cancelled.")
	    except dbus.DBusException:
		self.infoBar_label.setText("ERROR: Incoming connection blockade couldn't be cancelled.")
		self.checkboxes[1].setChecked(True)
      
    def sharingInternet(self):
	"""Method for sharing internet"""
	if self.checkboxes[1].isChecked():
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("internet_sharing","on")
		self.infoBar_label.setText("Sharing internet is successful.")
	    except dbus.DBusException:
		self.infoBar_label.setText("ERROR: Sharing internet isn't successful.")
		self.checkboxes[1].setChecked(False)
	else:
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("internet_sharing","off")
		self.infoBar_label.setText("Sharing internet was cancelled.")
	    except dbus.DBusException:
		self.infoBar_label.setText("ERROR: Sharing internet cancellation isn't successful.")
		self.checkboxes[1].setChecked(True)
      
    def blockOutgoing(self):
	"""Blocks the outgoing"""
	if self.checkboxes[2].isChecked():
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_outgoing","on")
		self.infoBar_label.setText("Outgoing connections were blocked.")
	    except dbus.DBusException:
		self.infoBar_label.setText("ERROR: Outgoing connections wasn't blocked.")
		self.checkboxes[2].setChecked(False)
	else:
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_outgoing","off")
		self.infoBar_label.setText("Outgoing connection blockade was cancelled.")
	    except dbus.DBusException:
		self.infoBar_label.setText("ERROR: Outgoing connection blockade wasn't cancelled.")
		self.checkboxes[2].setChecked(True)
	    
    def init(self):
	"""init method for the plasmoid. GUI stuff is located here."""
	self.setHasConfigurationInterface(False)
	self.setAspectRatioMode(Plasma.Square)#Plasma.IgnoreAspectRatio
        #self.resize(400,250)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        
        self.modules=self.link.Network.Firewall[dbus.String("iptables")].listModules()
        
        self.incoming_icon=Plasma.IconWidget(self.applet)
        self.incoming_icon.setIcon("application-x-smb-workgroup")
        self.incoming_icon.setMinimumWidth(100)
        self.incoming_icon.setMinimumHeight(40)
        self.incoming_icon.setMaximumHeight(40)
        self.sharing_icon=Plasma.IconWidget(self.applet)
        self.sharing_icon.setIcon("application-x-smb-server")
        self.sharing_icon.setMinimumWidth(100)
        self.sharing_icon.setMinimumHeight(40)
        self.sharing_icon.setMaximumHeight(40)
        self.outgoing_icon=Plasma.IconWidget(self.applet)
        self.outgoing_icon.setIcon("security-medium")
        self.outgoing_icon.setMinimumWidth(100)
        self.outgoing_icon.setMinimumHeight(40)
        self.outgoing_icon.setMaximumHeight(40)
        
        self.lock_icon=Plasma.IconWidget(self.applet)
        self.lock_icon.setMinimumWidth(40)
        self.lock_icon.setMinimumHeight(40)
        self.lock_icon.setMaximumHeight(40)
        self.onOff_pb=Plasma.PushButton(self.applet)
        self.onOff_pb.setMinimumWidth(100)
        self.onOff_pb.setMinimumHeight(40)
        self.onOff_pb.setMaximumHeight(40)
        self.onOffInfo_label=Plasma.Label(self.applet)
        self.onOffInfo_label.setMinimumWidth(200)
        self.onOffInfo_label.setMaximumHeight(50)
        
        if self.link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):
	    self.lock_icon.setIcon("object-locked")
	    self.onOff_pb.setText("Stop")
	    self.onOffInfo_label.setText("<p style='color:green'><h3>Firewall status: ON</h3></p>")
	else:
	    self.lock_icon.setIcon("object-unlocked")
	    self.onOff_pb.setText("Start")
	    self.onOffInfo_label.setText("<p style='color:red'><h3>Firewall status: OFF</h3></p>")
        
        self.checkboxes=[]
        counter=0
        for i in self.modules:
	    self.checkboxes.append(Plasma.CheckBox(self.applet))
	    self.checkboxes[counter].setText(self.link.Network.Firewall[dbus.String("iptables")].moduleInfo(i)[0])
	    self.checkboxes[counter].setMinimumWidth(120)
	    self.checkboxes[counter].setMaximumHeight(70)
	    counter+=1
	    
	counter=0
	for i in self.modules:
	    if self.link.Network.Firewall[dbus.String("iptables")].getModuleState(i)==dbus.String(u"on"):
		self.checkboxes[counter].setChecked(True)
	    else:
		self.checkboxes[counter].setChecked(False)
	    counter+=1
	    
	self.infoBarHeader_label=Plasma.Label(self.applet)
	self.infoBarHeader_label.setText("Latest news:")
	self.infoBarHeader_label.setMinimumWidth(60)
	self.infoBarHeader_label.setMaximumHeight(40)
	self.infoBar_label=Plasma.Label(self.applet)
	self.infoBar_label.setText("Plasmoid was loaded.")
	self.infoBar_label.setMinimumWidth(300)
	self.infoBar_label.setMaximumHeight(70)

        self.layout=QGraphicsGridLayout(self.applet)
        
        self.layout.addItem(self.lock_icon, 0,0)
        self.layout.addItem(self.onOffInfo_label, 0,1)
        self.layout.addItem(self.onOff_pb,0,2)
        self.layout.addItem(self.incoming_icon, 1,0)
        self.layout.addItem(self.checkboxes[0], 1,1)
        self.layout.addItem(self.sharing_icon, 2,0)
        self.layout.addItem(self.checkboxes[1], 2,1)
        self.layout.addItem(self.outgoing_icon, 3,0)
        self.layout.addItem(self.checkboxes[2], 3,1)
        self.layout.addItem(self.infoBarHeader_label, 4,0)
        self.layout.addItem(self.infoBar_label, 4,1)

	self.applet.setLayout(self.layout)
        
        QObject.connect(self.onOff_pb, SIGNAL("clicked()"), self.onOff)
        QObject.connect(self.checkboxes[0], SIGNAL("toggled(bool)"), self.blockIncoming)
        QObject.connect(self.checkboxes[1], SIGNAL("toggled(bool)"), self.sharingInternet)
        QObject.connect(self.checkboxes[2], SIGNAL("toggled(bool)"), self.blockOutgoing)
        
        self.link.listenSignals("Network.Firewall", self.handler)
    
    def handler(self, *args):
	"""Handler method for receiving signals from Comar"""
	if self.link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):
	    self.lock_icon.setIcon("object-locked")
	    self.onOff_pb.setText("Stop")
	    self.onOffInfo_label.setText("<p style='color:green'><h3>Firewall status: ON</h3></p>")
	    #self.infoBar_label.setText("Firewall was started.")
	    #print "ifin ici"
	else:
	    self.lock_icon.setIcon("object-unlocked")
	    self.onOff_pb.setText("Start")
	    self.onOffInfo_label.setText("<p style='color:red'><h3>Firewall status: OFF</h3></p>")
	    #self.infoBar_label.setText("Firewall was stopped.")
	    #print "elsin ici"
	counter=0
	for i in self.modules:
	    if self.link.Network.Firewall[dbus.String("iptables")].getModuleState(i)==dbus.String(u"on"):
		self.checkboxes[counter].setChecked(True)
	    else:
		self.checkboxes[counter].setChecked(False)
	    counter+=1
	    
def CreateApplet(parent):
    return FirewallApplet(parent) 
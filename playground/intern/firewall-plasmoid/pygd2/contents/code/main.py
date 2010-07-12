# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import QCheckBox, QPixmap, QGraphicsLinearLayout, QSizePolicy
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
		self.onOffInfo_label.setText("<p style='color:green'><h1>Firewall status: On</h1></p>")
		self.infoBar_label.setText("Firewall was started.")
	    except dbus.DBusException, e:
		print unicode(e)
		self.onOff_pb.setText("Start")
		self.lock_icon.setIcon("object-unlocked")
		self.onOffInfo_label.setText("<p style='color:red'><h1>Firewall status: Off</h1></p>")
		self.infoBar_label.setText("Firewall didn't start.")
	else:
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setState("off")
		self.onOff_pb.setText("Start")
		self.lock_icon.setIcon("object-unlocked")
		self.onOffInfo_label.setText("<p style='color:red'><h1>Firewall status: Off</h1></p>")
		self.infoBar_label.setText("Firewall was stopped.")
	    except dbus.DBusException:
		self.onOff_pb.setText("Stop")
		self.lock_icon.setIcon("object-locked")
		self.onOffInfo_label.setText("<p style='color:green'><h1>Firewall status: On</h1></p>")
		self.infoBar_label.setText("Firewall didn't stop..")
	      
    def blockIncoming(self):
	"""Blocks the incoming"""
	if self.checkboxes[0].isChecked():
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_incoming","on")
		self.infoBar_label.setText("Incomings were blocked.")
	    except dbus.DBusException:
		self.infoBar_label.setText("Incomings couldn't be blocked.")
		self.checkboxes[0].setChecked(False)
	else:
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_incoming","off")
		self.infoBar_label.setText("Block of incomings were cancelled.")
	    except dbus.DBusException:
		self.infoBar_label.setText("Incomings block couldn't be cancelled.")
		self.checkboxes[1].setChecked(True)
      
    def sharingInternet(self):
	"""Method for sharing internet"""
	if self.checkboxes[1].isChecked():
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("internet_sharing","on")
		self.infoBar_label.setText("Internet sharing is successful.")
	    except dbus.DBusException:
		self.infoBar_label.setText("Internet couldn't be shared.")
		self.checkboxes[1].setChecked(False)
	else:
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("internet_sharing","off")
		self.infoBar_label.setText("Internet sharing was cancelled.")
	    except dbus.DBusException:
		self.infoBar_label.setText("Internet share cancellation isn't successful.")
		self.checkboxes[1].setChecked(True)
      
    def blockOutgoing(self):
	"""Blocks the outgoing"""
	if self.checkboxes[2].isChecked():
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_outgoing","on")
		self.infoBar_label.setText("Outgoings were blocked.")
	    except dbus.DBusException:
		self.infoBar_label.setText("Outgoings couldn't be blocked.")
		self.checkboxes[2].setChecked(False)
	else:
	    try:
		self.link.Network.Firewall[dbus.String("iptables")].setModuleState("block_outgoing","off")
		self.infoBar_label.setText("Outgoing blockade was cancelled.")
	    except dbus.DBusException:
		self.infoBar_label.setText("Outgoing blockade wasn't cancelled.")
		self.checkboxes[2].setChecked(True)
	    
    def init(self):
	"""init method for the plasmoid. GUI stuff is located here."""
	self.setHasConfigurationInterface(False)
	self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.resize(700,300)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        
        self.modules=self.link.Network.Firewall[dbus.String("iptables")].listModules()
        
        incoming_icon=Plasma.IconWidget(self.applet)
        incoming_icon.setIcon("application-x-smb-workgroup")
        sharing_icon=Plasma.IconWidget(self.applet)
        sharing_icon.setIcon("application-x-smb-server")
        outgoing_icon=Plasma.IconWidget(self.applet)
        outgoing_icon.setIcon("security-medium")
        
        self.lock_icon=Plasma.IconWidget(self.applet)
        self.onOff_pb=Plasma.PushButton(self.applet)
        self.onOff_pb.setMinimumWidth(100)
        self.onOff_pb.setMaximumHeight(50)
        self.onOffInfo_label=Plasma.Label(self.applet)
        self.onOffInfo_label.setMinimumWidth(200)
        
        if self.link.Network.Firewall[dbus.String("iptables")].getState()==dbus.String(u"on"):
	    self.lock_icon.setIcon("object-locked")
	    self.onOff_pb.setText("Stop")
	    self.onOffInfo_label.setText("<p style='color:green'><h1>Firewall status: On</h1></p>")
	else:
	    self.lock_icon.setIcon("object-unlocked")
	    self.onOff_pb.setText("Start")
	    self.onOffInfo_label.setText("<p style='color:red'><h1>Firewall status: Off</h1></p>")
        
        self.checkboxes=[]
        counter=0
        for i in self.modules:
	    self.checkboxes.append(Plasma.CheckBox(self.applet))
	    self.checkboxes[counter].setText(self.link.Network.Firewall[dbus.String("iptables")].moduleInfo(i)[0])
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
	self.infoBar_label=Plasma.Label(self.applet)
	self.infoBar_label.setText("Plasmoid was loaded.")

        self.layout_general=QGraphicsLinearLayout(Qt.Vertical, self.applet)
        
        self.layout_top = QGraphicsLinearLayout(Qt.Horizontal)  
        self.layout_general.addItem(self.layout_top)
        self.layout_top.addItem(self.lock_icon)
        self.layout_top.addItem(self.onOffInfo_label)
        self.layout_top.addItem(self.onOff_pb)
        
        self.layout_line1=QGraphicsLinearLayout(Qt.Horizontal)  
        self.layout_general.addItem(self.layout_line1)
        self.layout_line1.addItem(incoming_icon)
        self.layout_line1.addItem(self.checkboxes[0])
        
        self.layout_line2=QGraphicsLinearLayout(Qt.Horizontal)  
        self.layout_general.addItem(self.layout_line2)
        self.layout_line2.addItem(sharing_icon))
        self.layout_line2.addItem(self.checkboxes[1])
        
        self.layout_line3=QGraphicsLinearLayout(Qt.Horizontal)  
        self.layout_general.addItem(self.layout_line3)
        self.layout_line3.addItem(outgoing_icon)
        self.layout_line3.addItem(self.checkboxes[2])
        
        self.layout_bottom=QGraphicsLinearLayout(Qt.Horizontal)  
        self.layout_general.addItem(self.layout_bottom)
        self.layout_bottom.addItem(self.infoBarHeader_label)
        self.layout_bottom.addItem(self.infoBar_label)
	
	#self.layout_general.setAlignment(self.layout_line2, Qt.AlignLeft)
	self.applet.setLayout(self.layout_general)
        
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
	    self.onOffInfo_label.setText("<p style='color:green'><h1>Firewall status: On</h1></p>")
	    #self.infoBar_label.setText("Firewall was started.")
	    #print "ifin ici"
	else:
	    self.lock_icon.setIcon("object-unlocked")
	    self.onOff_pb.setText("Start")
	    self.onOffInfo_label.setText("<p style='color:red'><h1>Firewall status: Off</h1></p>")
	    #self.infoBar_label.setText("Firewall was stopped.")
	    #print "elsin ici"
	
	sayici=0
	for i in self.modules:
	    print "for"
	    if self.link.Network.Firewall[dbus.String("iptables")].getModuleState(i)==dbus.String(u"on"):
		self.checkboxes[sayici].setChecked(True)
	    else:
		self.checkboxes[sayici].setChecked(False)
	    sayici+=1
	    
def CreateApplet(parent):
    return FirewallApplet(parent) 
#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import avahi
import os, sys, re 
from socket import gethostname
from dbus import DBusException


from dbus.mainloop.qt import DBusQtMainLoop
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_sinerjigui
import createsynergyconf
import parsesynergyconf


class SinerjiGui(QDialog, ui_sinerjigui.Ui_SinerjiGui):
    def __init__(self,  parent=None):
        super(SinerjiGui, self).__init__(parent)
        self.setupUi(self)
        self.cancelButton.setFocusPolicy(Qt.NoFocus)
        self.savequitButton.setFocusPolicy(Qt.NoFocus)
        self.discoveredHosts = set()
        self.durum = True
        self.serverboxdurum = None
        self.confdomain = []
        self.confdomaintop = None
        self.confdomainbottom = None
        self.confdomainright = None
        self.confdomainleft = None
        self.updateUi()
###############################################################
############           Gui Functions             ##############
###############################################################

        self.topComboBox.addItem('')
        self.bottomComboBox.addItem('')
        self.rightComboBox.addItem('')
        self.leftComboBox.addItem('')

    @pyqtSignature("QString")
    def on_topComboBox_activated(self, text):
        self.topComboBox.setEditable(True)
        if (text == '') or (text != gethostname()):
            if (text != ''):
                self.confdomaintop = ("top_bottom_%s" % text)
            else:
                pass
        else:
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.topComboBox.setCurrentIndex(0)


    @pyqtSignature("QString")
    def on_bottomComboBox_activated(self, text):
        self.bottomComboBox.setEditable(True)
        if (text == '') or (text != gethostname()):
            if (text != ''):
                self.confdomainbottom = ("bottom_top_%s" % text)
            else:
                pass
        else:
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.bottomComboBox.setCurrentIndex(0)
   

    @pyqtSignature("QString")
    def on_rightComboBox_activated(self, text):
        self.rightComboBox.setEditable(True)
        if (text == '') or (text != gethostname()):
            if (text != ''):
                self.confdomainright = ("right_left_%s" % text)
            else:
                pass
        else:
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.rightComboBox.setCurrentIndex(0)
    
    @pyqtSignature("QString")
    def on_leftComboBox_activated(self, text):
        self.leftComboBox.setEditable(True)
        if (text == '') or (text != gethostname()):
            if (text != ''):
                self.confdomainleft = ("left_right_%s" % text)
            else:
                pass
        else:
            QMessageBox.warning(self, u"Warning", u"The pc you have choosen is you own pc, please chose another pc")
            self.leftComboBox.setCurrentIndex(0)

## Svequit and Cancel button signals ##

    @pyqtSignature("")
    def on_cancelButton_clicked(self):
        self.reject()
    
    @pyqtSignature("")
    def on_savequitButton_clicked(self):
        if not self.confdomaintop:
            self.confdomaintop = ("top_bottom_%s" % self.topComboBox.currentText())
        elif not self.confdomainbottom:
            self.confdomainbottom = ("bottom_top_%s" % self.bottomComboBox.currentText())
        elif not self.confdomainright:
            self.confdomainright = ("right_left_%s" % self.rightComboBox.currentText())
        elif not self.confdomainleft:
            self.confdomainleft = ("left_right_%s" % self.leftComboBox.currentText())
        else:
            pass
        self.confdomain.append(self.confdomaintop)
        self.confdomain.append(self.confdomainbottom)
        self.confdomain.append(self.confdomainright)
        self.confdomain.append(self.confdomainleft)
        self.confdomain.append("host_host_%s" % gethostname())
        createsynergyconf.screens(self.confdomain)
        createsynergyconf.links(self.confdomain)
        self.reject()
            

## Only one checkbox has to be checked ##
    
    @pyqtSignature("")
    def on_serverBox_clicked(self):
        self.clientBox.toggle()
        if self.durum:
            self.browseDomain('_workstation._tcp')
            self.durum = None
            self.serverboxdurum = True


    @pyqtSignature("")
    def on_clientBox_clicked(self):
        self.serverBox.toggle()
        if self.serverboxdurum:
            pass
        #self.browser = sinerjiAvahi.SinerjiAvahi('_sinerji._tcp')


    def updateUi(self):
        if os.path.exists("synergy.conf"):
            self.parser = parsesynergyconf.parseSynergyConf("synergy.conf")
            for position in self.parser.getClients():
                if position[0] == "top":
                    self.topComboBox.insertItem(0, position[1])
                elif position[0] == "bottom":
                    self.bottomComboBox.insertItem(0, position[1])
                elif position[0] == "right":
                    self.rightComboBox.insertItem(0, position[1])
                elif position[0] == "left":
                    self.leftComboBox.insertItem(0, position[1])
                else:
                    pass
            
        
        
    #def save(self):
    #synergyconf.screens()

###############################################################
############           Avahi Services            ##############
###############################################################

    def browseDomain(self, servicename):

        DBusQtMainLoop( set_as_default=True )
        bus = dbus.SystemBus()
        self.server = dbus.Interface(
                bus.get_object(
                    avahi.DBUS_NAME, 
                    avahi.DBUS_PATH_SERVER), 
                avahi.DBUS_INTERFACE_SERVER)
        
        browser = dbus.Interface(bus.get_object(
            avahi.DBUS_NAME, 
            self.server.ServiceBrowserNew(
                avahi.IF_UNSPEC, 
                avahi.PROTO_UNSPEC,servicename,
                'local', 
                dbus.UInt32(0))),
            avahi.DBUS_INTERFACE_SERVICE_BROWSER)

        browser.connect_to_signal('ItemNew', self.addService)
        browser.connect_to_signal('ItemRemove', self.removeService)
        browser.connect_to_signal('AllForNow', self.allDone)


    def allDone(self):
        for domain in self.get_domains():
            self.topComboBox.addItem(domain)
            self.bottomComboBox.addItem(domain)
            self.rightComboBox.addItem(domain)
            self.leftComboBox.addItem(domain)

    def addService(self, interface, protocol, name, stype, domain, flags):

        #print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)
        self.server.ResolveService(interface, protocol, name, stype,
                              domain, avahi.PROTO_UNSPEC, dbus.UInt32(0),
                              reply_handler=self.service_resolved, error_handler=self.print_error)


    def removeService(self, interface, protocol, name, stype, domain, flags):
        hostadded = re.sub(r'\.%s$' % domain, '', host)
        self.discoveredHosts.remove(hostadded)

    def service_resolved(self, interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags):
        #print "******", interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags
        hostremoved = re.sub(r'\.%s$' % domain, '', host)
        self.discoveredHosts.add(hostremoved)
    
    def get_domains(self):
        return list(self.discoveredHosts)

    def print_error(self, *args):
        print 'error_handler'
        print args[0]


    def publishService(self):
        
        DBusQtMainLoop( set_as_default=True )
        bus = dbus.SystemBus()
        server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), avahi.DBUS_INTERFACE_SERVER)

        txt = ['os=linux']
        group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()), avahi.DBUS_INTERFACE_ENTRY_GROUP)
        group.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC, dbus.UInt32(0),
                         'Synergy at %s' % gethostname(), '_synergy._tcp', '', '',
                         dbus.UInt16(24800), avahi.string_array_to_txt_array(txt))
        group.Commit()

###############################################################
############                Main                 ##############
###############################################################


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    form = SinerjiGui()
    form.show()
    app.exec_()



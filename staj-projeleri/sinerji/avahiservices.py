#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import gethostname
from dbus.mainloop.qt import DBusQtMainLoop
from PyQt4.QtGui import QApplication
import sys
import dbus
import avahi
import re


class avahiSinerji:
    def __init__(self, host):
        self.avahi = None
        self.domain = None
        self.stype = "_workstation._tcp"
        self.host = host
        self.txt = {}
        self.domainBrowser = None
        self.serviceBrowser = None
        self.bus = None
        self.server = None
        self.discoveredHosts = set()
        self.entrygroup = None
        self.connected = False
        self.announced = False
        self.avahi = avahi
        self.name = "Sinerji"
        self.port = "24800"

##############################################################
################## Error functions ###########################
##############################################################

    def entrygroupCommitError(self, err):
        # left blank for possible later usage
        pass

    def errorCallbackResolving(self, err):
        print 'Error while resolving: ' + str(err)

    def errorCallback(self, err):
        print "str(err)"
        # timeouts are non-critical
        if str(err) != 'Timeout reached':
            self.disconnect()

##############################################################
################# Browsing Services ##########################
##############################################################

    def newService(self, interface, protocol, name, stype, domain, flags):
        if not self.connected:
            return
        # synchronous resolving
        # print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)
        self.server.ResolveService( int(interface), int(protocol), name, stype, \
                domain, self.avahi.PROTO_UNSPEC, dbus.UInt32(0), \
                        reply_handler=self.serviceResolvedCallback, error_handler=self.errorCallbackResolving)
        print "--------- service resolving"

    def removeService(self, interface, protocol, name, stype, domain, flags):
        if not self.connected:
            return
        hostremoved = re.sub(r'\.%s$' % domain, '', host)
        self.discoveredHosts.remove(hostremoved)

    def getDomains(self):
        return list(sorted(self.discoveredHosts))
    
    def serviceResolvedCallback(self, interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags):
        if not self.connected:
            return
        hostadded = re.sub(r'\.%s$' % domain, '', host)
        #self.discoveredHosts.add(hostadded)
        print "*************", hostadded
        #print 'Service data for service %s in domain %s on %i.%i:' % (name, domain, interface, protocol)
        

##############################################################
################# Connecting to interfaces ###################
##############################################################


    def avahiDbusConnect(self, a, connect, disconnect):
        if connect != "":
            print 'Lost connection to avahi-daemon'
            self.disconnect()
        else:
            print 'We are connected to avahi-daemon'

    def connectDbus(self):
        if self.bus:
            return True
        try:
            print "--------- connecting dbus"
            self.bus = dbus.SystemBus()
            self.bus.add_signal_receiver(self.avahiDbusConnect, "NameOwnerChanged", "org.freedesktop.DBus", arg0="org.freedesktop.Avahi")
        except Exception, e:
            print e
            return False
        else:
            return True

    def connectAvahi(self):
        if not self.connectDbus():
            return False
        if self.server:
            return True 
        try:
            print "--------- connecting avahi"
            self.server = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, \
                self.avahi.DBUS_PATH_SERVER), self.avahi.DBUS_INTERFACE_SERVER) 
            self.server.connect_to_signal('StateChanged', self.serverStateChangedCallback)
        except Exception, e:
            # Avahi service is not present
            self.server = None
            print e
            return False
        else:
            return True

    def connect(self):
        if not self.connectAvahi():
            return False
        self.connected = True

        print "--------- browsing domain"
        if self.serviceBrowser:
            return

        print "--------- new service type -------------"
        object_path = self.server.ServiceBrowserNew(avahi.IF_UNSPEC,avahi.PROTO_UNSPEC, self.stype, 'local', dbus.UInt32(0))

        self.serviceBrowser = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, \
            object_path) , self.avahi.DBUS_INTERFACE_SERVICE_BROWSER)
        self.serviceBrowser.connect_to_signal('ItemNew', self.newService)
        self.serviceBrowser.connect_to_signal('ItemRemove', self.removeService)
        self.serviceBrowser.connect_to_signal('Failure', self.errorCallback)

    def disconnect(self):
        if self.connected:
            self.connected = False
            if self.serviceBrowser:
                self.serviceBrowser.Free()
                self.serviceBrowser._obj._bus = None
                self.serviceBrowser._obj = None
            if self.domainBrowser:
                self.domainBrowser.Free()
                self.domainBrowser._obj._bus = None
                self.domainBrowser._obj = None
            self.removeAnnounce()
            self.server._obj._bus = None
            self.server._obj = None
        self.server = None
        self.serviceBrowser = None
        self.domainBrowser = None
        print"--------- disconnecting"


##############################################################
################  Creating services ##########################
##############################################################


    def announce(self):
        if not self.connected:
            return False
        state = self.server.GetState()
        if state == self.avahi.SERVER_RUNNING:
            self.createService()
            self.announced = True
            return True

    def removeAnnounce(self):
        if self.announced == False:
            return False
        try:
            if self.entrygroup.GetState() != self.avahi.ENTRY_GROUP_FAILURE:
                self.entrygroup.Reset()
                self.entrygroup.Free()
                # .Free() has mem leaks
                self.entrygroup._obj._bus = None
                self.entrygroup._obj = None
                self.entrygroup = None
                self.announced = False

                return True
            else:
                return False
        except dbus.DBusException, e:
            print "Can't remove service. That should not happen"

    def clientTxt(self):
        domainlist = {"deneme":1, "deneme1":2}
        return self.avahi.dict_to_txt_array(domainlist)

    def createService(self):
        try:
            if not self.entrygroup:
                # create an EntryGroup for publishing
                self.entrygroup = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, 
                    self.server.EntryGroupNew()), 
                    self.avahi.DBUS_INTERFACE_ENTRY_GROUP)

                self.entrygroup.connect_to_signal('StateChanged', self.entrygroupStateChangedCallback)


            print 'Publishing service %s of type _sinerji._tcp' % (self.name)

            self.entrygroup.AddService(self.avahi.IF_UNSPEC,
                self.avahi.PROTO_UNSPEC, dbus.UInt32(0), self.name, '_sinerji._tcp', '',
                '', dbus.UInt16(self.port), self.clientTxt(),
                reply_handler=self.serviceAddedCallback,
                error_handler=self.serviceAddFailCallback)

            self.entrygroup.Commit(reply_handler=self.serviceCommittedCallback,
                error_handler=self.entrygroupCommitError)

            return True

        except dbus.DBusException, e:
            print str(e)
            return False


##############################################################
############### Callback functions ###########################
##############################################################

    def serviceAddFailCallback(self, err):
        print "Error while adding service. %s' % str(err)"
        if 'Local name collision' in str(err):
            alternative_name = self.server.GetAlternativeServiceName(self.name)
            return
        self.disconnect()

    def serviceAddedCallback(self):
        print 'Service successfully added'

    def serviceCommittedCallback(self):
        print 'Service successfully committed'

    def serverStateChangedCallback(self, state, error):
        print "Server state changed to %s" % state
        if state == self.avahi.SERVER_RUNNING:
            self.createService()
        elif state in (self.avahi.SERVER_COLLISION,
                self.avahi.SERVER_REGISTERING):
            self.disconnect()
            self.entrygroup.Reset()
        elif state == self.avahi.CLIENT_FAILURE:
            print 'CLIENT FAILURE'

    def entrygroupStateChangedCallback(self, state, error):
        if state == self.avahi.ENTRY_GROUP_COLLISION:
            print "avahiservices.py: local name collision"
            self.serviceAddFailCallback('Local name collision')
        elif state == self.avahi.ENTRY_GROUP_FAILURE:
            self.disconnect()
            self.entrygroup.Reset()
            print "avahiservices.py: ENTRY_GROUP_FAILURE reached (that should not happen)"


##############################################################
###################### Main ##################################
##############################################################
if __name__ == "__main__":

    app = QApplication(sys.argv)
    DBusQtMainLoop(set_as_default=True)
    
    instance = avahiSinerji(gethostname())
    instance.connectDbus()
    instance.connectAvahi()
    instance.connect()
    if instance.discoveredHosts:
        print instance.discoveredHosts
        instance.disconnect()
    try:
        app.exec_()
    except KeyboardInterrupt:
        pass




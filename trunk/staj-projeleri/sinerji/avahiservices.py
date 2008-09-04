#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import gethostname
from dbus.mainloop.qt import DBusQtMainLoop
from PyQt4.QtGui import QApplication
import sys
import dbus
import avahi

class avahiSinerji:
    def __init__(self, host):
        self.avahi = None
        self.domain = None
        self.stype = "_sinerji._tcp"
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

    
    def printError(self, *args):
        print 'error_handler'
        print args[0]

    def newService(self, interface, protocol, name, stype, domain, flags):
        #print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)
        
        if not self.connected:
            return
        # synchronous resolving
        self.server.ResolveService( int(interface), int(protocol), name, stype, \
                domain, self.avahi.PROTO_UNSPEC, dbus.UInt32(0), \
                        reply_handler=self.service_resolved_callback, error_handler=self.error_callback1)
       

    def removeService(self, interface, protocol, name, stype, domain, flags):
        if not self.connected:
            return

        hostremoved = re.sub(r'\.%s$' % domain, '', host)
        print hostremoved
        self.discoveredHosts.remove(removed)


    def service_resolved_callback(self, interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags):
        print 'Service data for service %s in domain %s on %i.%i:' % name, domain, interface, protocol
        print 'Host %s (%s), port %i, TXT data: %s' % (host, address, port, self.txt_array_to_dict(txt))
        
        if not self.connected:
            return
        hostadded = re.sub(r'\.%s$' % domain, '', host)
        print hostadded
        self.discoveredHosts.remove(hostadded)


    def newServiceType(self, interface, protocol, stype, domain, flags):
        if self.serviceBrowser:
            return
        
        object_path = self.server.ServiceBrowserNew(interface, protocol, \
                stype, domain, dbus.UInt32(0))

        self.service_browser = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, \
            object_path) , self.avahi.DBUS_INTERFACE_SERVICE_BROWSER)
        self.service_browser.connect_to_signal('ItemNew', self.newService)
        self.service_browser.connect_to_signal('ItemRemove', self.removeService)
        self.service_browser.connect_to_signal('Failure', self.errorService)

    def newDomainCallback(self,interface, protocol, domain, flags):
        if domain != "local":
            self.browse_domain(interface, protocol, domain)



    def avahi_dbus_connect_cb(self, connect, disconnect):
        if connect != "":
            print 'Lost connection to avahi-daemon'
            self.disconnect()
        else:
            print 'We are connected to avahi-daemon'

    
    def connectDbus(self):
        if self.bus:
            return True
        try:

            self.bus = dbus.SystemBus()
            self.bus.add_signal_receiver(self.avahi_dbus_connect_cb, "NameOwnerChanged", "org.freedesktop.DBus", arg0="org.freedesktop.Avahi")
            print " dbus connecting"
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
            self.server = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, 
                self.avahi.DBUS_PATH_SERVER), self.avahi.DBUS_INTERFACE_SERVER), 
            self.server.connect_to_signal('StateChanged', self.server_state_changed_callback)
            print "avahi connecting"
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

            print "browse domain"
        self.connected = True
        
        if self.domain is None:
            # Explicitly browse .local
            self.browse_domain(self.avahi.IF_UNSPEC, self.avahi.PROTO_UNSPEC, "local")
            print "browse domain"
            # Browse for other browsable domains
            self.domain_browser = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, \
                    self.server.DomainBrowserNew(self.avahi.IF_UNSPEC, \
                    self.avahi.PROTO_UNSPEC, '', self.avahi.DOMAIN_BROWSER_BROWSE,\
                    dbus.UInt32(0))), self.avahi.DBUS_INTERFACE_DOMAIN_BROWSER)
            self.domain_browser.connect_to_signal('ItemNew', self.new_domain_callback)
            self.domain_browser.connect_to_signal('Failure', self.error_callback)
        else:
            self.browse_domain(self.avahi.IF_UNSPEC, self.avahi.PROTO_UNSPEC, self.domain)

        return True
    
    def browse_domain(self, interface, protocol, domain):
        self.newServiceType(interface, protocol, self.stype, domain, '')

    def disconnect(self):
        if self.connected:
            self.connected = False
            if self.service_browser:
                self.service_browser.Free()
                self.service_browser._obj._bus = None
                self.service_browser._obj = None
            if self.domain_browser:
                self.domain_browser.Free()
                self.domain_browser._obj._bus = None
                self.domain_browser._obj = None
            self.remove_announce()
            self.server._obj._bus = None
            self.server._obj = None
        self.server = None
        self.service_browser = None
        self.domain_browser = None 
    
    def announce(self):
        if not self.connected:
            return False

        state = self.server.GetState()
        if state == self.avahi.SERVER_RUNNING:
            self.create_service()
            self.announced = True
            return True

    def remove_announce(self):
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
            gajim.log.debug("Can't remove service. That should not happen")

    def createService(self):
        try:
            if not self.entrygroup:
                # create an EntryGroup for publishing
                self.entrygroup = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, 
                    self.server.EntryGroupNew()), 
                    self.avahi.DBUS_INTERFACE_ENTRY_GROUP)

                self.entrygroup.connect_to_signal('StateChanged', self.entrygroup_state_changed_callback)


            self.txt = txt
            print 'Publishing service %s of type %s' % self.name, self.stype

            self.entrygroup.AddService(self.avahi.IF_UNSPEC,
                self.avahi.PROTO_UNSPEC, dbus.UInt32(0), self.name, self.stype, '',
                '', dbus.UInt16(self.port), self.clientTxt(),
                reply_handler=self.service_added_callback,
                error_handler=self.service_add_fail_callback)

            self.entrygroup.Commit(reply_handler=self.service_committed_callback,
                error_handler=self.entrygroup_commit_error_CB)

            return True

        except dbus.DBusException, e:
            gajim.log.debug(str(e))
            return False

    def service_added_callback(self):
        print 'Service successfully added'

    def service_committed_callback(self):
        print 'Service successfully committed'

    def server_state_changed_callback(self, state, error):
        print "Server state changed to %s" % state
        if state == self.avahi.SERVER_RUNNING:
            self.create_service()
        elif state in (self.avahi.SERVER_COLLISION,
                self.avahi.SERVER_REGISTERING):
            self.disconnect()
            self.entrygroup.Reset()
        elif state == self.avahi.CLIENT_FAILURE:
            print 'CLIENT FAILURE'

    def entrygroup_state_changed_callback(self, state, error):
        if state == self.avahi.ENTRY_GROUP_COLLISION:
            gajim.log.debug('zeroconf.py: local name collision')
            self.service_add_fail_callback('Local name collision')
        elif state == self.avahi.ENTRY_GROUP_FAILURE:
            self.disconnect()
            self.entrygroup.Reset()
            gajim.log.debug('zeroconf.py: ENTRY_GROUP_FAILURE reached(that'
                ' should not happen)')

if __name__ == "__main__":

    app = QApplication(sys.argv)
    DBusQtMainLoop(set_as_default=True)
    
    instance = avahiSinerji(gethostname())
    instance.connectDbus()
    instance.connectAvahi()
    instance.connect()
    instance.announce()
    app.exec_()




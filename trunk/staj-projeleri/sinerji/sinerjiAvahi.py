import dbus
import avahi
import re
from dbus.mainloop.qt import DBusQtMainLoop
from socket import gethostname
from dbus import DBusException
import os, sys

class SinerjiAvahi:
    def __init__(self, service):
        self.discoveredHosts = set()
        self.browseDomain(service)

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

    def service_resolved(self, interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags):
        #print "******", interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags
        host = re.sub(r'\.%s$' % domain, '', host)
        self.discoveredHosts.add(host)

    def get_domains(self):
        return list(self.discoveredHosts)

    def print_error(self, *args):
        print 'error_handler'
        print args[0]

    def addService(self, interface, protocol, name, stype, domain, flags):
        #print "Found service '%s' type '%s' domain '%s' " % (name, stype, domain)
        self.server.ResolveService(interface, protocol, name, stype,
                              domain, avahi.PROTO_UNSPEC, dbus.UInt32(0),
                              reply_handler=self.service_resolved, error_handler=self.print_error)

    def removeService(self, interface, protocol, name, stype, domain, flags):
        host = re.sub(r'\.%s$' % domain, '', host)
        self.discoveredHosts.remove(host)

    def browseDomain(self, servicename):
        
        DBusQtMainLoop( set_as_default=True )
        bus = dbus.SystemBus()
        self.server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
                                 'org.freedesktop.Avahi.Server')
        b = dbus.Interface(bus.get_object(avahi.DBUS_NAME, self.server.ServiceBrowserNew(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC,
                                                                                    servicename,'local', dbus.UInt32(0))),
                           avahi.DBUS_INTERFACE_SERVICE_BROWSER)
        b.connect_to_signal('ItemNew', self.addService)
        b.connect_to_signal('ItemRemove', self.removeService)


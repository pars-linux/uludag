#!/usr/bin/python
# -*- coding: utf-8 -*-    from socket import gethostname


from PyQt4.QtGui import QApplication
from socket import gethostname
from dbus.mainloop.qt import DBusQtMainLoop
import sys
import dbus
import avahi
import re
from textview import Logging

C_NAME, C_DOMAIN, C_INTERFACE, C_PROTOCOL, C_HOST, \
C_ADDRESS, C_PORT, C_BARE_NAME, C_TXT = range(9)

class Zeroconf:
    def __init__(self, name, host, port):
        self.avahi = None
        self.debugmode = False
        self.domain = None   # specific domain to browse
        self.stype = '_ssh._tcp'
        self.port = port     # listening port that gets announced
        self.username = name
        self.host = host
        self.txt = {}        # service data
        self.log = Logging()

        #XXX these CBs should be set to None when we destroy the object·
        # (go offline), because they create a circular reference·

        self.service_browser = None
        self.domain_browser = None
        self.bus = None
        self.server = None
        self.contacts = {}    # all current local contacts with data
        self.entrygroup = None
        self.connected = False
        self.users = []
        self.NetworkUsers = []
        self.announced = False
        self.invalid_self_contact = {}

    def error_callback1(self, err):
        self.log.debug('Error while resolving: ' + str(err))

    def error_callback(self, err):
        self.log.debug(str(err))
        # timeouts are non-critical
        if str(err) != 'Timeout reached':
            self.disconnect()

    def new_service_callback(self, interface, protocol, name, stype, domain, flags):
        if self.debugmode:
            self.log.debug('Found service %s in domain %s on %i.%i.' % (name, domain, interface, protocol))
        if not self.connected:
            return

        # synchronous resolving
        self.server.ResolveService( int(interface), int(protocol), name, stype, \
                    domain, self.avahi.PROTO_UNSPEC, dbus.UInt32(0), \
                    reply_handler=self.service_resolved_callback, error_handler=self.error_callback1)


    def remove_service_callback(self, interface, protocol, name, stype, domain, flags):
        if self.debugmode:
            self.log.debug('Service %s in domain %s on %i.%i disappeared.' % (name, domain, interface, protocol))
        if not self.connected:
            return
        if name != self.name:
            for key in self.contacts.keys():
                if self.contacts[key][C_BARE_NAME] == name:
                    del self.contacts[key]
                    return

    def new_service_type(self, interface, protocol, stype, domain, flags):
        # Are we already browsing this domain for this type? 
        if self.service_browser:
            return

        object_path = self.server.ServiceBrowserNew(interface, protocol, \
                stype, domain, dbus.UInt32(0))

        self.service_browser = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, \
            object_path) , self.avahi.DBUS_INTERFACE_SERVICE_BROWSER)
        self.service_browser.connect_to_signal('ItemNew', self.new_service_callback)
        self.service_browser.connect_to_signal('ItemRemove', self.remove_service_callback)
        self.service_browser.connect_to_signal('Failure', self.error_callback)

    def new_domain_callback(self,interface, protocol, domain, flags):
        if domain != "local":
            self.browse_domain(interface, protocol, domain)

    def txt_array_to_dict(self, txt_array):
        txt_dict = {}
        for els in txt_array:
            key, val = '', None
            for c in els:
                    c = chr(c)
                    if val is None:
                        if c == '=':
                            val = ''
                        else:
                            key += c
                    else:
                        val += c
            if val is None: # missing '='
                val = ''
            txt_dict[key] = val.decode('utf-8', 'ignore')
        return txt_dict

    def service_resolved_callback(self, interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags):
        if self.debugmode:
            self.log.debug('Service data for service %s in domain %s on %i.%i:' % (name, domain, interface, protocol))
            self.log.debug('Host %s (%s), port %i, TXT data: %s' % (host, address, port, self.txt_array_to_dict(txt)))
        self.networkUsers(name, address)
        if not self.connected:
            return
        bare_name = name
        if name.find('@') == -1:
            name = name + '@' + name

        # we don't want to see ourselves in the list
        if name != self.name:
            self.contacts[name] = (name, domain, interface, protocol, host, address, port, bare_name, txt)
        else:
            self.invalid_self_contact[name] = (name, domain, interface, protocol, host, address, port, bare_name, txt)

    def networkUsers(self, name, address):
        self.users.append('%s (%s)' % (name, address))
        self.NetworkUsers = self.users
        print self.NetworkUsers


    def service_resolved_all_callback(self, interface, protocol, name, stype, domain, host, aprotocol, address, port, txt, flags):
        if not self.connected:
            return
        bare_name = name
        if name.find('@') == -1:
            name = name + '@' + name
        self.contacts[name] = (name, domain, interface, protocol, host, address, port, bare_name, txt)


    def service_added_callback(self):
        self.log.debug('Service successfully added')

    def service_committed_callback(self):
        self.log.debug('Service successfully committed')

    def service_updated_callback(self):
        self.log.debug('Service successfully updated')

    def service_add_fail_callback(self, err):
        self.log.debug('Error while adding service. %s' % str(err))
        if 'Local name collision' in str(err):
            alternative_name = self.server.GetAlternativeServiceName(self.username)
            return
        self.disconnect()

    def server_state_changed_callback(self, state, error):
        self.log.debug('server state changed to %s' % state)
        if state == self.avahi.SERVER_RUNNING:
            self.create_service()
        elif state in (self.avahi.SERVER_COLLISION,
                self.avahi.SERVER_REGISTERING):
            self.disconnect()
            self.entrygroup.Reset()
        elif state == self.avahi.CLIENT_FAILURE:
            # does it ever go here?
            self.log.debug('CLIENT FAILURE')

    def entrygroup_state_changed_callback(self, state, error):
        # the name is already present, so recreate
        if state == self.avahi.ENTRY_GROUP_COLLISION:
            self.log.debug('avahiservices.py: local name collision')
            self.service_add_fail_callback('Local name collision')
        elif state == self.avahi.ENTRY_GROUP_FAILURE:
            self.disconnect()
            self.entrygroup.Reset()
            self.log.debug('avahiservices.py: ENTRY_GROUP_FAILURE reached(that'
                ' should not happen)')


    def create_service(self):
        try:
            if not self.entrygroup:
                # create an EntryGroup for publishing
                self.entrygroup = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, self.server.EntryGroupNew()), self.avahi.DBUS_INTERFACE_ENTRY_GROUP)
                self.entrygroup.connect_to_signal('StateChanged', self.entrygroup_state_changed_callback)

            txt = {}

            #remove empty keys
            for key,val in self.txt.iteritems():
                if val:
                    txt[key] = val

            txt['port.p2pj'] = self.port
            txt['version'] = 1
            txt['txtvers'] = 1

            # replace gajim's show messages with compatible ones
            if 'status' in self.txt:
                txt['status'] = self.replace_show(self.txt['status'])
            else:
                txt['status'] = 'avail'

            self.txt = txt
            self.log.debug('Publishing service %s of type %s' % (self.name,
                self.stype))
            self.entrygroup.AddService(self.avahi.IF_UNSPEC,
                self.avahi.PROTO_UNSPEC, dbus.UInt32(0), self.name, self.stype, '',
                '', dbus.UInt16(self.port), self.avahi_txt(),
                reply_handler=self.service_added_callback,
                error_handler=self.service_add_fail_callback)

            self.entrygroup.Commit(reply_handler=self.service_committed_callback, 
                error_handler=self.entrygroup_commit_error_CB)

            return True

        except dbus.DBusException, e:
            self.log.debug(str(e))
            return False

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
            self.log.debug("Can't remove service. That should not happen")

    def browse_domain(self, interface, protocol, domain):
        self.new_service_type(interface, protocol, self.stype, domain, '')

    def avahi_dbus_connect_cb(self, a, connect, disconnect):
        if connect != "":
            self.log.debug('Lost connection to avahi-daemon')
            self.disconnect()
            if self.disconnected_CB:
                self.disconnected_CB()
        else:
            self.log.debug('We are connected to avahi-daemon')

    # connect to dbus
    def connect_dbus(self):
        try:
            import dbus
        except ImportError:
            self.log.debug('Error: python-dbus needs to be installed. No zeroconf support.')
            return False
        if self.bus:
            return True
        try:
            self.bus = dbus.SystemBus()
            self.bus.add_signal_receiver(self.avahi_dbus_connect_cb, 
                "NameOwnerChanged", "org.freedesktop.DBus", 
                arg0="org.freedesktop.Avahi")
        except Exception, e:
            # System bus is not present
            self.bus = None
            self.log.debug(str(e))
            return False
        else:
            return True

    # connect to avahi
    def connect_avahi(self):
        if not self.connect_dbus():
            return False
        try:
            import avahi
            self.avahi = avahi
        except ImportError:
            self.log.debug('Error: python-avahi needs to be installed. No zeroconf support.')
            return False

        if self.server:
            return True
        try:
            self.server = dbus.Interface(self.bus.get_object(self.avahi.DBUS_NAME, \
            self.avahi.DBUS_PATH_SERVER), self.avahi.DBUS_INTERFACE_SERVER)
            self.server.connect_to_signal('StateChanged', 
                self.server_state_changed_callback)
        except Exception, e:
            # Avahi service is not present
            self.server = None
            self.log.debug(str(e))
            return False
        else:
            return True

    def connect(self):
        self.name = self.username + '@' + self.host # service name
        if not self.connect_avahi():
            return False

        self.connected = True
        # start browsing
        if self.domain is None:
            # Explicitly browse .local
            self.browse_domain(self.avahi.IF_UNSPEC, self.avahi.PROTO_UNSPEC, "local")

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

    # refresh txt data of all contacts manually (no callback available)
    def resolve_all(self):
        if not self.connected:
            return
        for val in self.contacts.values():
            self.server.ResolveService(int(val[C_INTERFACE]), int(val[C_PROTOCOL]),
                val[C_BARE_NAME], self.stype, val[C_DOMAIN],
                self.avahi.PROTO_UNSPEC, dbus.UInt32(0),
                reply_handler=self.service_resolved_all_callback,
                error_handler=self.error_callback)

    def get_contacts(self):
        return self.contacts

    def get_contact(self, jid):
        if not jid in self.contacts:
            return None
        return self.contacts[jid]

    def update_txt(self, show = None):
        if show:
            self.txt['status'] = self.replace_show(show)

        txt = self.avahi_txt()
        if self.connected and self.entrygroup:
            self.entrygroup.UpdateServiceTxt(self.avahi.IF_UNSPEC, self.avahi.PROTO_UNSPEC, dbus.UInt32(0), self.name, self.stype,'', txt, reply_handler=self.service_updated_callback, error_handler=self.error_callback)
            return True
        else:
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    DBusQtMainLoop(set_as_default=True)
    instance = Zeroconf("moon", gethostname(), "_presence._tcp")
    instance.connect_dbus()
    instance.connect_avahi()
    instance.connect()
    app.exec_()


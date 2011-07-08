#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Network configuration tool for NetworkManager
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

"""Interactive network configuration tool for NetworkManager"""

import sys
import uuid
from optparse import OptionParser

from networkmanager import NetworkManager, WiredSettings, WirelessSettings,WPAWirelessSettings,WEP40128WirelessSettings,WEP128WirelessSettings, DeviceType, DeviceState

# Color characters
COLORS = {
            'red'        : '\x1b[31;01m',
            'blue'       : '\x1b[34;01m',
            'cyan'       : '\x1b[36;01m',
            'gray'       : '\x1b[30;01m',
            'green'      : '\x1b[32;01m',
            'light'      : '\x1b[37;01m',
            'yellow'     : '\x1b[33;01m',
            'magenta'    : '\x1b[35;01m',
            'reddark'    : '\x1b[31;0m',
            'bluedark'   : '\x1b[34;0m',
            'cyandark'   : '\x1b[36;0m',
            'graydark'   : '\x1b[30;0m',
            'greendark'  : '\x1b[32;0m',
            'magentadark': '\x1b[35;0m',
            'normal'     : '\x1b[0m'
         }

USE_COLOR = True
GUDEV_HANDLE = None

from networkmanager.ipaddr import IPv4IpValidationError as IPv4IpValidationError
from networkmanager.ipaddr import IPv6IpValidationError as IPv6IpValidationError

ACTIVATED, DEACTIVATED = range(2)

def colorize(msg, color):
    """Colorize the given message if requested."""
    if not USE_COLOR:
        return msg
    else:
        return "%s%s%s" % (COLORS[color], msg, COLORS['normal'])

def get_input_atleast(label,min_):
    data=get_input(label)
    if min_>=len(data):
        return None
    return data

def get_input(label):
    """Get input from the terminal."""
    try:
        return raw_input(colorize(("%s > " % label), 'light'))
    except (KeyboardInterrupt, EOFError):
        print
        sys.exit(1)

def get_number(label, min_, max_):
    """Get a number from the terminal."""
    index_ = min_ - 1
    while index_ < min_ or index_ > max_:
        try:
            index_ = int(raw_input(colorize(("%s > " % label), 'light')))
        except ValueError:
            pass
        except (KeyboardInterrupt, EOFError):
            print
            sys.exit(1)
    return index_

def print_connection(state, nm_settings, devices=[]):
    """Print a specific connection."""
    state = "X" if state == ACTIVATED else " "
    print "[%s]  %s%s    %s" % (colorize(state, 'green'),
                                colorize(nm_settings.id, 'cyan'),
                                "",
                                "")
    import dbus.exceptions
    try:
        for dev in devices:
            ip4address = dev.ip4config.addresses[0][0]
            netmask = dev.ip4config.addresses[0][1]
            gateway = dev.ip4config.addresses[0][2]
            print "\tInterface: %s" % dev.interface
            print "\tAddress: %s\n\tNetmask: %s\n\tDefault Gateway: %s"\
                                            % (ip4address, netmask, gateway)
            print "\tName Servers: %s" % ", ".join(dev.ip4config.name_servers)
    except dbus.exceptions.DBusException:
        pass

def print_connections(nm_handle):
    """Print connection list."""
    connections = {
                '802-11-wireless'   : [],
                '802-3-ethernet'    : [],
                'cdma'              : [],
                'gsm'               : [],
                'pppoe'             : [],
                'vpn'               : [],
                'unknown'           : [],
            }

    for connection in nm_handle.connections:
        connections[connection.settings.type].append(connection)

    for connection_key in connections:
        if len(connections[connection_key]) > 0:
            # Convert ethernet->Ethernet, wireless->Wireless, etc.
            conn_interface = connection_key.split("-")[-1].capitalize()
            print colorize("%s connections" % conn_interface, 'green')

            for connection in connections[connection_key]:
                devices = []
                state = DEACTIVATED
                for active in nm_handle.active_connections:
                    if active.connection.settings.uuid == connection.settings.uuid:
                        state = ACTIVATED
                        devices = active.devices
                print_connection(state, connection.settings, devices)

def print_device(nm_device, index = -1):
    """Pretty print a specific device."""
    vendor = ""
    model = ""
    if GUDEV_HANDLE is not None:
        udev_device = \
                GUDEV_HANDLE.query_by_subsystem_and_name("net",
                                                         nm_device.interface)
        if udev_device:
            vendor = udev_device.get_property("ID_VENDOR_FROM_DATABASE")
            model = udev_device.get_property("ID_MODEL_FROM_DATABASE")
    if index > 0:
        print "  [%s]" % index,
    print " %6s %s %s [driver: %s]" % (colorize(nm_device.interface, "light"),
                                       vendor, model,
                                       colorize(nm_device.driver, "yellow"))

def print_devices(nm_handle):
    """Print the device list."""
    for device_type in nm_handle.devices_map:
        print colorize("%s devices"\
                % str(device_type).split("-")[-1].capitalize(), 'green')
        for device in nm_handle.devices_map[device_type]:
            print_device(device)

def get_connection(nm_handle, text = "connection"):
    """Get a connection from user"""
    connections = {
                '802-11-wireless'   : [],
                '802-3-ethernet'    : [],
                'cdma'              : [],
                'gsm'               : [],
                'pppoe'             : [],
                'vpn'               : [],
                'unknown'           : [],
            }

    for connection in nm_handle.connections:
        connections[connection.settings.type].append(connection)

    connection_list = []
    index = 0
    for connection_type in connections:
        if len(connections[connection_type]) > 0:
            conn_interface = connection_type.split("-")[-1].capitalize()
            print colorize("%s connections" % conn_interface, 'green')
            for (_index, connection) in enumerate(connections[connection_type]):
                print "  [%s] %s" % ((index + 1 + _index), connection.settings.id)
                connection_list.append(connection)
            index = len(connection_list)

    connection_num = get_number(text, 1, len(connection_list)) - 1
    connection = connection_list[connection_num]
    return connection


def remove_connection(nm_handle):
    """Delete a connection."""
    if not len(nm_handle.connections) > 0:
        return
    connection = get_connection(nm_handle, "Remove")
    connection.delete()

def get_ip_assignment(settings):
    """Get IP assignment method from user"""
    print colorize("Select IP assignment method:", "yellow")
    print "  [1] Enter an IP address manually"
    print "  [2] Automatically obtain an IP address"
    if get_number("Type", 1, 2) == 2:
        ignore_auto_dns = False
        if "ignore-auto-dns" in settings._settings["ipv4"].keys():
            ignore_auto_dns = settings._settings["ipv4"]["ignore-auto-dns"]
        settings.set_auto()
        settings._settings["ipv4"]["ignore-auto-dns"] = ignore_auto_dns
    else:
        validaddress=False
        while not validaddress:
            try:
                settings.address = get_input_atleast("Address",4) 
                validaddress=True
            except IPv4IpValidationError ,  IPv6IpValidationError:
                valid=False
        validnetmask=False
        while not validnetmask:
            try:
                settings.netmask = get_input_atleast("Mask",4)
                validnetmask=True
            except IPv4IpValidationError ,  IPv6IpValidationError:
                validnetmask=False
            except ValueError:
                validnetmask=False
        validgateway=False
        while not validgateway:
            try:
                settings.gateway = get_input_atleast("Gateway",4)
                validgateway=True
            except IPv4IpValidationError ,  IPv6IpValidationError:
                validgateway=False


    return settings

def split_dnses(dnses):
    return dnses.split(',')

def get_dns_assignment(settings):
    """Get DNS assignment method from user"""
    print colorize("Select Name server (DNS) assignment method:", "yellow")
    print "  [1] Enter an name server address manually"
    print "  [2] Automatically obtain from DHCP"
    dns = get_number("Type", 1, 2)
    if dns == 1:
        print("Use commas to separate DNSes")
        print("Usage example 4.2.2.1,4.2.2.2")
        validdnses=False
        while not validdnses:
            try:
                dnses = get_input_atleast("DNSes",4)
                splitted_dnses=split_dnses(dnses)
                settings._settings["ipv4"]["ignore-auto-dns"] = True
                settings.dns = splitted_dnses
                validdnses=True
            except IPv4IpValidationError,IPv6IpValidationError:
                validdnses=False
            except AttributeError:
                validdnses=False
        

    elif dns == 2:
        settings._settings["ipv4"]["ignore-auto-dns"] = False
        #settings.dns = None

    return settings

def create_ethernet_connection(nm_handle, _device):
    """Create an ethernet connection."""

    settings = None
    settings = WiredSettings()
    settings.uuid = uuid.uuid4()
    settings.device = _device
    settings.mac_address = _device.hwaddress
    settings = get_ip_assignment(settings)
    settings = get_dns_assignment(settings)
    connection_id = None
    print
    while not connection_id:
        connection_id = get_input("Profile name").strip()
        if nm_handle.get_connections_by_id(connection_id) is not None:
            print "There is already a connection named '%s'" % connection_id
            print
            connection_id = None

    settings.id = connection_id
    nm_handle.add_connection(settings)

def dbus_byte_array_to_string(array):
    import dbus
    cikti = ""
    for i in array:
        cikti += chr(i)
    return cikti

def get_wep_inf():
    auth=("open","shared")
    index=1
    print colorize("Wep index 1-2-3-4 |  Default 1","yellow")
    index=get_number("Index",1,4)
    print colorize("Authorization","yellow")
    print "[1] Open"
    print "[2] Shared"
    authindex=get_number("Authorization",1,2)-1
    return {"index":index-1,"auth":auth[authindex]}

def get_password(stype):
    import getpass
    valid=False
    while not valid:
        passw=getpass.getpass()
        if is_pass_valid(passw,stype):
            valid=True
    return passw
        

def is_hex(passw):
    import string
    for x in passw:
        if x not in string.hexdigits:
            return False
    return True

def is_pass_valid(passw,stype):
    length=len(passw)
    if stype == "WEP 40/128":
        if length>0 and length <=64:
            return True
        else:
            return False
        """
        if length==5:
            #ascii40
            return True
        elif length==10:
            #hex40
            if is_hex(passw):
                return True
                #valid
        elif length==13:
            #ascii128
            return True
        elif length==26:
            #hex128
            if is_hex(passw):
                #valid
                return True
        else:
            #invalid
            return False
        """
    elif stype == "WEP 128":
        if length==13:
            #ascii128
            return True
        elif length==26:
            #hex128
            if is_hex(passw):
                #valid
                return True
        else:
            #invalid
            return False
    elif stype == "WPA & WPA2":
        if length>=8 and length<=63:
            #ascii
            #valid
            return True
        elif length==64:
            #hex
            #valid
            if is_hex(passw):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def get_wireless_infs_from_user(_device):

    inf={"device-mode":"","remote":"","secure":""}

    #Get device mode
    device_modes=["infrastructure","adhoc"]
    index_=1
    print
    print colorize("Select device mode:","yellow")
    for mode_name in device_modes:
        print "  [%s] %s" % (index_,mode_name.upper())
        index_+=1
    mode_no = get_number("Device Mode",1,len(device_modes))-1
    print
    #print mode_no

    #Get ssid
    remote=None
    while not remote:
        print colorize("SSID","yellow")
        remotes=[]

        index_=1
        for remotePoint  in _device.access_points:
            remotes.append(remotePoint)

            print "  [%s] %s" % (index_,\
                    dbus_byte_array_to_string(remotePoint.ssid))
            index_+=1
        print "  [%s] Rescan" % index_
        print "  [%s] Enter SSID maually" % (index_+1)
        remoteNo = get_number("ESSID", 1 , len(remotes)+2)-1
        if remoteNo < len(remotes) and remoteNo > -1:
            remote = remotes[remoteNo]
        elif remoteNo == len(remotes):
            remote=None
        elif remoteNo ==len(remotes)+1:
            remote=get_input("ESSID")



    #Get secure type
    secure=None
    while not secure:
        secure_type=("Unsecured","WEP 40/128","WEP 128","WPA & WPA2")
        print colorize("Security","yellow") 
        print "  [1] Unsecured"
        print "  [2] WEP 40/128"
        print "  [3] WEP 128"
        print "  [4] WPA & WPA2"

        secure_index=get_number("Security Type ",1,4)-1
        if secure_index == 0:
            secure=secure_type[0]
        elif secure_index==1:
            secure=secure_type[1]
            passw=get_password("WEP 40/128")
            webinfs=get_wep_inf()
            inf["auth-alg"]=webinfs["auth"]
            inf["wep-key"]=webinfs["index"]
            inf["pass"]=passw
        elif secure_index==2:
            secure=secure_type[2]
            passw=get_password("WEP 128")
            webinfs=get_wep_inf()
            inf["auth-alg"]=webinfs["auth"]
            inf["wep-key"]=webinfs["index"]
            inf["pass"]=passw
        elif secure_index==3:
            passw=get_password("WPA & WPA2") 
            secure=secure_type[3]
            inf["pass"]=passw
    inf["device-mode"]=device_modes[mode_no]
    inf["remote"]=remote
    inf["secure"]=secure
    return inf

def wireless_enabled(nm_handle,interface):
    nm_handle.wireless_enabled=interface


def create_wireless_connection(nm_handle, _device):
    """Create a wireless connection."""
    import dbus

    inf=get_wireless_infs_from_user(_device)
    device_modes=["infrastructure","adhoc"]
    securities=["Unsecured","WEP 40/128","WEP 128","WPA & WPA2"]
    def wep_security_config(settings):
        settings._settings["802-11-wireless"][dbus.String("security")]="802-11-wireless-security"
        settings._settings["802-11-wireless-security"][dbus.String("auth-alg")]=inf["auth-alg"]
        wep_index="wep-key"+str(inf["wep-key"])
        settings._settings["802-11-wireless-security"][dbus.String(wep_index)]=inf["pass"]
        if not inf["wep-key"] == 1:
            settings._settings["802-11-wireless-security"][dbus.String("wep-tx-keyidx")]=inf["wep-key"]


    if inf["secure"]==securities[0]:
        settings = WirelessSettings()
    elif inf["secure"]==securities[1]:
        settings = WEP40128WirelessSettings()
        wep_security_config(settings)
    elif inf["secure"]==securities[2]:
        settings = WEP128WirelessSettings()
        wep_security_config(settings)
    elif inf["secure"]==securities[3]:
        settings=WPAWirelessSettings()
        settings._settings["802-11-wireless"][dbus.String("security")]="802-11-wireless-security"
        settings._settings["802-11-wireless-security"][dbus.String("psk")]=inf["pass"]

    settings.mac_address=_device.hwaddress
    settings.uuid = uuid.uuid4()
    settings.device = _device
    settings._settings["802-11-wireless"][dbus.String("mode")]=inf["device-mode"]
    settings._settings["802-11-wireless"][dbus.String("ssid")]=inf["remote"].ssid

    #"""Get IP and DNS assignment method"""
    settings = get_ip_assignment(settings)
    settings = get_dns_assignment(settings)


    #"""Get connection id"""
    connection_id = None
    print
    while not connection_id:
        connection_id = get_input("Profile name").strip()
        if nm_handle.get_connections_by_id(connection_id) is not None:
            print "There is already a connection named '%s'" % connection_id
            print
            connection_id = None

    settings.id = connection_id


    nm_handle.add_connection(settings)

def create_connection(nm_handle):
    """Create a connection."""

    functions = {
            DeviceType.ETHERNET : create_ethernet_connection,
            DeviceType.WIFI : create_wireless_connection,
            }

    if len(nm_handle.devices) == 0:
        # No network devices
        return

    device_types = nm_handle.devices_map.keys()

    print colorize("Select device type:", "yellow")

    for device_type in device_types:
        print "  [%s] %s" % (device_types.index(device_type) + 1,
                                    str(device_type).capitalize())

    device_no = get_number("Device type", 1, len(device_types)) - 1

    filtered_devices = nm_handle.devices_map[device_types[device_no]]

    device = get_device(nm_handle, filtered_devices)

    if device is not None:
        functions[device.type](nm_handle, device)

def get_device(nm_handle, device_list = None, type = None, mustSelect = True):
    """Get device from user"""
    types = {
                    '802-11-wireless'   : DeviceType.WIFI,
                    '802-3-ethernet'    : DeviceType.ETHERNET,
        }
    if device_list is None:
        if type is None:
            device_list = nm_handle.devices
        else:
            device_list = nm_handle.devices_map[types[type]]
    device_count=len(device_list)
    if device_count==1:
        #print device_list
        return device_list[0] 
    elif device_count>1:
        print colorize("Select device:", "yellow")
        if not mustSelect:
            print "  [0]  Device independent"
        for (index, device) in enumerate(device_list):
            print_device(device, index + 1)
        dev_no = get_number("Device", 1, len(device_list)) - 1
        print
        return device_list[dev_no]


def get_device_by_mac(nm_handle, mac_address, type = None):
    types = {
                    '802-11-wireless'   : DeviceType.WIFI,
                    '802-3-ethernet'    : DeviceType.ETHERNET,
#                    'cdma'              : [],
#                    'gsm'               : [],
#                    'unknown'           : [],
                }
    devices = None
    if not type == None:
        device_type = types[type]
        devices = nm_handle.devices_map[device_type]
    else:
        devices = nm_handle.devices

    device = None
    for dev in devices:
        if mac_address == dev.hwaddress:
            device = dev
            break
    return device

def edit_connection(nm_handle):
    """Edit a connection."""
    connection = get_connection(nm_handle, "Edit")
    changing = True
    settings = connection.settings
    while changing:
        print
        print colorize("Select an option:", "yellow")
        con_mac_address = settings.mac_address
        device_name = ""
        if con_mac_address == None:
            device_name = "Device independent"
        else:
            device = get_device_by_mac(nm_handle, con_mac_address)
            if device == None:
                device_name = "Device unplugged" #not installed
            else:
                vendor = ""
                model = ""

                if GUDEV_HANDLE is not None:
                    udev_device = \
                        GUDEV_HANDLE.query_by_subsystem_and_name("net",
                                                                 device.interface)
                    if udev_device:
                        vendor = udev_device.get_property("ID_VENDOR_FROM_DATABASE")
                        model = udev_device.get_property("ID_MODEL_FROM_DATABASE")

                device_name = " %6s %s %s [driver: %s]"\
                                    % (colorize(device.interface, "light"),
                                    vendor, model, colorize(device.driver, "yellow"))
        _index = 1

        print "  [%d] Change device: %s" % (_index, device_name)
        _index += 1

        method = "Manual"
        if settings.auto:
            method = "Automatic"
        print "  [%d] Change IP assignment method: %s" % (_index, method)
        _index += 1

        method = "Automatic"
        if not settings.dns == None:
            if "ignore-auto-dns" in settings._settings["ipv4"].keys()\
                    and settings._settings["ipv4"]["ignore-auto-dns"]:
                method = "Manual"
        print "  [%d] Change name server (DNS) assignment method: %s"\
                                                    % (_index, method)
        _index += 1

        print "  [%d] Change profile name: %s" % (_index, settings.id)
        _index += 1

        print "  [%d] Save and finish editing" % _index

        option = get_number("Option", 1, _index ) - 1
        print
        if option == 0:
            device = get_device(nm_handle, type = settings.type, mustSelect = False)
            settings.device = device
            settings.mac_address = str(device.hwaddress)
            #FIXME:should continue
            changing = False
        elif option == 1:
            dns = settings.dns[0:]
            settings = get_ip_assignment(settings)
            if dns is not None:
                settings.dns = dns
        elif option == 2:
            settings = get_dns_assignment(settings)
        elif option == 3:
            connection_id = None
            connection_ids = []

            for conn in nm_handle.connections:
                connection_ids.append(conn.settings.id)

            while not connection_id:
                connection_id = get_input("Profile name").strip()
                if connection_id in connection_ids:
                    print "There is already a connection named '%s'"\
                                                        % connection_id
                    print
                    connection_id = None

            settings.id = connection_id
        elif option == 4:
            changing = False
    nm_handle.get_connection(settings.uuid).update(settings)

def set_connection_state_down(nm_handle, connection):
    """Set the state of a given connection to Down."""
    device=get_device(nm_handle,None,connection.settings.type)
    device.disconnect()
    #print "There is no active connection or no connection named %s" % connection_id

def set_connection_state_up(nm_handle, connection_id, interface=None):
    """Set the state of a given connection to Up."""
    conn = nm_handle.get_connections_by_id(connection_id)
    if conn is not None:
        # FIXME: We're always taking the first one, check again.
        conn = conn[0]
        if interface is not None:
            # The interface is given
            for device in nm_handle.devices:
                if device.interface == interface:
                    conn_mac_addr = conn.settings.mac_address
                    if conn_mac_addr is None\
                            or conn_mac_addr == device.hwaddress:
                        nm_handle.activate_connection(conn, device)
                    else:
                        print "The connection's mac address did not match this device"
                    return

        if conn.settings.mac_address:
            device = get_device_by_mac(nm_handle, conn.settings.mac_address)
            if device is not None:
                if not device.state == DeviceState.UNAVAILABLE:
                    nm_handle.activate_connection(conn, device)
                else:
                    print "Device unavailable"
        else:
            # The connection doesn't have a fixed MAC so
            # we have to ask for the interface
            # or use a possibly given interface through CLI

            types = {
                        '802-11-wireless'   : DeviceType.WIFI,
                        '802-3-ethernet'    : DeviceType.ETHERNET,
                    #   'cdma'              : [],
                    #   'gsm'               : [],
                    #   'unknown'           : [],
            }

            device_list = nm_handle.devices_map[types[conn.settings.type]]
            device = get_device(nm_handle, device_list)

            if device is not None:
                if not device.state == DeviceState.UNAVAILABLE:
                    nm_handle.activate_connection(conn, device)
                else:
                    print "Device unavailable"
            else:
                print "No device"
    else:
        print "There is no connection named: %s" % connection_id


#####################
### Main function ###
#####################
def main():
    """Main entry point to the interactive NetworkManager utility."""

    if "--no-color" in sys.argv:
        global USE_COLOR
        USE_COLOR = False
        sys.argv.remove("--no-color")

    # Create NetworkManager handle
    nm_handle = NetworkManager()

    # If available create a gudev client for vendor/device informations
    try:
        import gudev
    except ImportError:
        pass
    else:
        global GUDEV_HANDLE
        GUDEV_HANDLE = gudev.Client("net")

    usage = """\
usage: %prog [options] <interface>

When activating a connection, you should either provide an interface like
'eth0', 'wlan0', etc. or select an interface from the list."""

    parser = OptionParser(usage)

    parser.add_option("-C", "--connections",
                      action="store_const",
                      dest="action",
                      const="connections",
                      help='List connections')

    parser.add_option("-D", "--devices",
                      action="store_const",
                      dest="action",
                      const="devices",
                      help='List devices')

    parser.add_option("-c", "--create",
                      action="store_const",
                      dest="action",
                      const="create",
                      help='Create a connection')

    parser.add_option("-e", "--edit",
                      action="store_const",
                      dest="action",
                      const="edit",
                      help='Edit a connection')

    parser.add_option("-r", "--remove",
                      action="store_const",
                      dest="action",
                      const="remove",
                      help='Remove a connection')

    parser.add_option("-a", "--activate",
                      action="store_const",
                      dest="a_connection",
                      const="activate",
                      help='Activates the given connection')

    parser.add_option("-d", "--deactivate",
                      action="store_const",
                      dest="d_connection",
                      const="deactivate",
                      help='Deactivates the given connection')

    parser.add_option("-w","--wifi",
            action="store_const",
            dest="wifi",
            const="wifi",
            help='Activates or deactivates wifi',
            )

    (options, args) = parser.parse_args()
    try:
        arg0 = args[0]
    except IndexError:
        arg0 = None
    try:
        arg1=args[1]
    except IndexError:
        arg1 = None

    if options.action == "connections":
        print_connections(nm_handle)
    elif options.action == "devices":
        print_devices(nm_handle)
    elif options.action == "create":
        create_connection(nm_handle)
    elif options.action == "remove":
        remove_connection(nm_handle)
    elif options.action == "edit":
        edit_connection(nm_handle)
    elif options.a_connection == "activate":
        if arg0 == None:
            #list connections
            con=get_connection(nm_handle,"Activate")
            #Fix No interface
            set_connection_state_up(nm_handle,con.settings.id)
        else:
            set_connection_state_up(nm_handle,arg0,arg1)
    elif options.d_connection == "deactivate":
        if arg0 == None:
            #list connections
            con=get_connection(nm_handle,"Deactivate")
            set_connection_state_down(nm_handle,con)
        else:
            set_connection_state_down(nm_handle,arg0)
    elif options.wifi == "wifi":
        trues=["1","true","True","yes","Yes"]
        if arg0 in trues:
            wireless_enabled(nm_handle,True)
        else:
            wireless_enabled(nm_handle,False)
    else:
        parser.print_help()
        return 1

    # FIXME: Do better error handling
    return 0
if __name__ == "__main__":
    sys.exit(main())

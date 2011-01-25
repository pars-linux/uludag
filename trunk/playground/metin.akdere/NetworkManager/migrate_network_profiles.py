#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import ConfigParser


default_nameservers = []
default_resolv_conf_file = "/etc/resolv.default.conf"
lan_config_file  = "/etc/network/net_tools"
wlan_config_file  = "/etc/network/wireless_tools"
NetworkManager_conf_dir = "/etc/NetworkManager/system-connections"

def get_default_nameservers():
    """Read once default name servers in resolve.default.conf, if 'name_mode' in
    given profile was set to default, supply these values in the new profile file
    """

    if len(default_nameservers) == 0:

        # TODO: We should supply a default nameserver conf unless we find any
        if os.path.exists(default_resolv_conf_file):
            try:
                file_pointer = open(default_resolv_conf_file)
                try:
                    nameservers_file = file_pointer.readlines()
                finally:
                    file_pointer.close()
            except:
                pass

        for line in nameservers_file:
            if not line.startswith("#") and line.startswith("nameserver"):
                ns = line.split()[-1]
                default_nameservers.append(ns)
    return default_nameservers


class PardusNetworkProfile:
    """Represents network profiles that we have been using in Pardus' network
    manager. We have two types of network profiles specified: wired or wireless
    """

    def __init__(self, name, connection_type, settings):

        self.profile_name = name
        self.connection_type = connection_type
        self.device = "none"
        self.net_mode = "none"
        self.name_mode = "none"
        self.state = "none"
        self.name_server = "none"
        self.net_address = "none"
        self.net_mask = "none"
        self.net_gateway = "none"
        self.remote = "none"
        self.auth = "none"
        self.auth_password = "none"

        self.set_attributes(settings)

    def set_attributes(self, settings):
        """We receive profile settings as dictionary type in 'settings'
        Map each key-value pairs for each object.
        """

        for key, value in settings.items():
            self.__dict__[key] = value

    def get_profile_name(self):
        return self.profile_name

    def get_connection_type(self):
        return self.connection_type

    def get_device(self):
        return self.device

    def get_net_mode(self):
        return self.net_mode

    def get_name_mode(self):
        return self.name_mode

    def get_state(self):
         return self.state

    def get_name_server(self):
        return self.name_server

    def get_net_address(self):
        return self.net_address

    def get_net_mask(self):
        return self.net_mask

    def get_net_gateway(self):
        return self.net_gateway

    def get_remote(self):
        return self.remote

    def get_auth(self):
        return self.auth

    def get_auth_password(self):
        return self.auth_password


class NetworkManagerProfile:
    """Represents network profiles used in NetworkManager. In NetworkManager, 
    settings are kept in a seperate file for each profile.
    """

    def __init__(self, name, pardus_profile):
        """Each section is kept in corresponding class attribute"""

        self.cfg = ConfigParser.ConfigParser()
        self.connection = Connection(pardus_profile)
        self.ipv4 = IpV4(pardus_profile)
        self.ipv6 = IpV6(pardus_profile)
        self._802_3_ethernet = self.set_802_3_ethernet(pardus_profile)
        self._802_11_wireless = self.set_802_11_wireless(pardus_profile)
        self._802_11_wireless_security = self.set_802_11_wireless_security(pardus_profile)

        self.create_config()

    def set_802_3_ethernet(self, pardus_profile):
        """If this is a wired (802-3-ethernet) profile, set _802_3_ethernet 
        attribute.
        """

        if pardus_profile.connection_type == "802-3-ethernet":
            return  _802_3_Ethernet(pardus_profile)
        else:
            return "none"

    def set_802_11_wireless(self, pardus_profile):
        """If this is a wireless (802-11-wirelesss) profile, set 
        _802_11_wireless attribute."""
        if pardus_profile.connection_type == "802-11-wireless":
            return  _802_11_Wireless(pardus_profile)
        else:
            return "none"

    def set_802_11_wireless_security(self, pardus_profile):
        """If the wireless connection has any security restrictions, create a 
        802-11-wireless-security section with corresponding values.
        """

        if pardus_profile.get_connection_type() ==  "802-11-wireless": #Check if it is a wlan profile
            if pardus_profile.get_auth() == "none":
                self._802_11_wireless.security = "none"
                return "none"
            else:
                self._802_11_wireless.security = "802-11-wireless-security"
                return _802_11_Wireless_Security(pardus_profile)
        else:
            return "none"

    def create_config(self):
        """Create sections and options in the prfoile's config file by calling
        each options corresponding method.
        """

        #FIXME: Try to do it over loops ie. self[attr].set_config()
        for attr, value in self.__dict__.items():
            if attr == "connection":
                self.connection.set_config(self.cfg)
            if attr == "ipv4":
                self.ipv4.set_config(self.cfg)
            if attr == "ipv6":
                self.ipv6.set_config(self.cfg)
            if attr == "_802_3_ethernet" and not value == "none":
                self._802_3_ethernet.set_config(self.cfg)
            if attr=="_802_11_wireless" and not value == "none":
                self._802_11_wireless.set_config(self.cfg)
            if attr=="_802_11_wireless_security" and not value == "none":
                self._802_11_wireless_security.set_config(self.cfg)

    def write_config(self):
        """Write settings to profile file"""

        #Before writing to file we must convert underscores to dashes, moreover _id must be written as id, and _type as type
        profile_path = os.path.join("%s" % NetworkManager_conf_dir, self.connection._id)
        with open(profile_path, "wb") as configfile:
            self.cfg.write(configfile)

    def set_ownership(self):
        """NetworkManager is smart enough to understand whether a configuration file is valid 
        by checking its permissions"""

        os.chmod(os.path.join("%s" %NetworkManager_conf_dir, self.connection._id), 0600)


class Connection:

    def __init__(self, pardus_profile):
        self.name = "connection"
        self._id = pardus_profile.get_profile_name()
        self.uuid = self.set_uuid(device = pardus_profile.get_device())
        self._type = pardus_profile.get_connection_type()
        self.autoconnect = "false" #FIXME False gives error on iteration in ConfigParser
        self.timestamp = "none"
        self.read_only = "false"

    def set_uuid(self, device):
        """Generate random type UUID"""
        import uuid

        return str(uuid.uuid4())

    def set_config(self, cfg):
        """One single config file will be used to write settings"""

        cfg.add_section(self.name)
        for attr, value in self.__dict__.items():
            if value not in ["false", "none"] and  attr != "name":
                #Before creating config file _id must be id, and _type must be type
                if attr == "_id" or attr == "_type" : attr = attr.split("_")[-1]
                #There isnt any underscore in config options, replace them with dashes if found any
                attr = attr.replace("_", "-")
                cfg.set(self.name, attr, value)



class IpV4:

    def __init__(self, pardus_profile):
        self.name = "ipv4"
        self.dns_search = "none"
        self.routes = "none"
        self.ignore_auto_routes = "false"
        self.ignore_auto_dns = "false"
        self.dhcp_client_id = "none"
        self.dhcp_send_hostname = "false"
        self.dhcp_hostname = "none"
        self.never_default = "false"
        self.method = pardus_profile.get_net_mode() # auto or manual, same as in NM
        self.addresses1 = self.set_addresses(pardus_profile)    # NM uses array of IPv4 address structures. We have only one for each iface
        self.dns = self.set_dns(pardus_profile)

    def set_dns(self, pardus_profile):
        """Decide whether to use default, custom or auto (DHCP assigned) nameservers"""

        if pardus_profile.get_name_mode() == "default":
            default_nameservers =";".join( get_default_nameservers())
            default_nameservers = default_nameservers + ";" # Make sure addresses end with ';'
            self.ignore_auto_dns = "true"
            return str(default_nameservers)
        elif pardus_profile.get_name_mode() == "custom":
            name_server = pardus_profile.get_name_server()
            name_server = name_server + ";"
            self.ignore_auto_dns = "true"
            return str(name_server)
        else:
            # Nothing done in auto option
            return "Auto option secildi"

    def set_addresses(self, pardus_profile):
        """Set network addresses from given settings"""

        addresses = []
        if self.method == "manual":
            net_mask = self.calculate_prefix(pardus_profile.get_net_mask())
            addresses.append(str(pardus_profile.get_net_address()))
            addresses.append(str(net_mask))
            addresses.append(str(pardus_profile.get_net_gateway()))
            addresses = ";".join(addresses)
            addresses = addresses + ";"     # Make sure addresses end with ';'
            return addresses
        else:
            return "none"

    def decimal2binary(self, n):
        """Convert decimal octet value to binary format"""

        octet = ["0","0","0","0","0","0","0","0"]
        index = 0
        if n < 0 or n > 255:
            raise ValueError, "Octet value must be between [0-255]"
        if n == 0: 
            return "".join(octet)
        while n > 0:
            octet[index] = str((n % 2))
            index += 1
            n = n >> 1
        octet.reverse()
        return "".join(octet)

    def calculate_prefix(self, net_mask):
        """Convert netmask value to CIDR prefix type which is between [1-32] as told in NM spec
            See http://mail.gnome.org/archives/networkmanager-list/2008-August/msg00076.html"""

        octets = net_mask.split(".")
        octet_in_binary = []
        netmask_value = 0
        for octet in octets:
            ret = self.decimal2binary(int(octet))
            octet_in_binary.append(ret)
        for i in "".join(octet_in_binary):
            if int(i) == 1 : netmask_value += 1
        return netmask_value

    def set_config(self, cfg):
        """One single config file will be used to write settings"""

        cfg.add_section(self.name)
        for attr, value in self.__dict__.items():
            if value not in ["false", "none"] and  attr != "name":
                attr = attr.replace("_", "-")
                cfg.set(self.name, attr, value)


class IpV6:

    def __init__(self, pardus_profile):
        self.name = "ipv6"
        self.method = "none"
        self.dns = "none"
        self.dns_search = "none"
        self.addresses = "none"
        self.routes = "none"
        self.ignore_auto_routes = "false"
        self.ignore_auto_dns = "false"
        self.dhcp_client_id = "none"
        self.dhcp_send_hostname = "none"
        self.dhcp_hostname = "none"
        self.never_default = "false"

        self.set_method()

    def set_method(self):
        """Ignoring by default for nowadays"""
        self.method = "ignore"

    def set_config(self, cfg):
        """One single config file will be used to write settings"""

        cfg.add_section(self.name)
        for attr, value in self.__dict__.items():
            if value not in ["false", "none"] and  attr != "name":
                attr = attr.replace("_", "-")
                cfg.set(self.name, attr, value)

class _802_3_Ethernet:

    def __init__(self, pardus_profile):
        self.name = "802-3-ethernet"
        self.port = "none"
        self.speed = "none" #0
        self.duplex = "full"
        self.auto_negotiate = "false"
        self.mac_address = self.set_mac_address(pardus_profile.get_device())
        self.mtu = "none" #0

    def set_mac_address(self, iface):
        """Return MAC addresses of given interface on the machine using ifconfig, inspired from python uuid module"""

        command = "ifconfig"
        hw_identifiers = ['hwaddr', 'ether']

        for dir in ['', '/sbin', '/usr/sbin']:
            executable = os.path.join(dir, command)
            if not os.path.exists(executable):
                continue

            try:
                cmd = 'LC_ALL=C %s -a 2>/dev/null ' % executable
                pipe = os.popen(cmd)
            except IOError:
                continue

            for line in pipe:
                if line.startswith(iface):
                    words = line.lower().split()
                    for i in range(len(words)):
                        if words[i] in hw_identifiers:
                            return words[i+1]

    def set_config(self, cfg):
        """One single config file will be used to write settings"""

        cfg.add_section(self.name)
        for attr, value in self.__dict__.items():
            if value not in ["false", "none"] and  attr != "name":
                attr = attr.replace("_", "-")
                cfg.set(self.name, attr, value)


class _802_11_Wireless:

    def __init__(self, pardus_profile):
        self.name = "802-11-wireless"
        self.ssid = self.set_ssid(pardus_profile)
        self.band = "none"
        self.channel = "0"
        self.bssid = "none"
        self.rate = "0"
        self.tx_power = "0"
        self.mtu = "0"
        self.seen_bssids = "none"
        self.security = "none"
        self.mode = self.set_mode(pardus_profile)
        self.mac_address = self.set_mac_address(pardus_profile.get_device())

    def set_mac_address(self, iface):
        """Return MAC addresses of given interface on the machine using ifconfig, inspired from python uuid module"""

        command = "ifconfig"
        hw_identifiers = ['hwaddr', 'ether']

        for dir in ['', '/sbin', '/usr/sbin']:
            executable = os.path.join(dir, command)
            if not os.path.exists(executable):
                continue

            try:
                cmd = 'LC_ALL=C %s -a 2>/dev/null ' % executable
                pipe = os.popen(cmd)
            except IOError:
                continue

            for line in pipe:
                if line.startswith(iface):
                    words = line.lower().split()
                    for i in range(len(words)):
                        if words[i] in hw_identifiers:
                            return words[i+1]

    def set_mode(self, pardus_profile):
        """One of 'infrastructure' or 'adhoc'. If blank, infrastructure is assumed"""

        #TODO: How to determine mode (adhoc or infrastructure) from old profile settings
        return "infrastructure"

    def set_ssid(self, pardus_profile):
        """Set ssid value"""

        if pardus_profile.connection_type == "802-11-wireless":
            return str(pardus_profile.get_remote())
        else:
            return "none"

    def set_config(self, cfg):
        """One single config file will be used to write settings"""

        cfg.add_section(self.name)
        for attr, value in self.__dict__.items():
            if value not in ["false", "none", "0"] and  attr != "name":
                attr = attr.replace("_", "-")
                cfg.set(self.name, attr, value)


class _802_11_Wireless_Security:

    def __init__(self, pardus_profile):
        self.name = "802-11-wireless-security"
        self.key_mgmt = "none"
        self.wep_tx_keyidx = "0"
        self.auth_alg = "none"
        self.proto = "none"
        self.pairwise = "none"
        self.group = "none"
        self.leap_username = "none"
        self.wep_key0 ="none"
        self.wep_key1 ="none"
        self.wep_key2 ="none"
        self.wep_key3 ="none"
        self.psk = "none"
        self.leap_password = "none"
        self.wep_key_type = "0"

        self.set_up_wireless_security(pardus_profile)

    def set_up_wireless_security(self, pardus_profile):
        """WEP, WPA or none type security based operations"""

        if pardus_profile.get_auth() in ["wep", "wepascii"]:
            self.set_wep(pardus_profile)
        elif pardus_profile.get_auth() == "wpa-psk":
            self.set_wpa(pardus_profile)
        else:
            return

    def set_wpa(self, pardus_profile):
        """Set up WPA based networks"""

        self.key_mgmt = "wpa-psk"
        self.psk = str(pardus_profile.get_auth_password())

    def set_wep(self, pardus_profile):
        """Set up WEP based networks"""

        self.auth_alg = "open" #TODO: or 'shared' ??
        self.key_mgmt = "none" # Which stands for WEP based key management
        self.wep_key0 = str(pardus_profile.get_auth_password()) # Default index
        self.wep_key_type = "1" # Interpret WEP keys as hex or ascii keys


    def set_config(self, cfg):
        """One single config file will be used to write settings"""

        cfg.add_section(self.name)
        for attr, value in self.__dict__.items():
            if value not in ["false", "none", "0"] and  attr != "name":
                attr = attr.replace("_", "-")
                cfg.set(self.name, attr, value)


class Migrator:
    """Read network profiles we have been using in Pardus' network manager and 
    transform them into NetworkManager profile type.
    """

    def __init__(self):

        self.pardus_profiles = []
        self.network_manager_profiles = []
        self.lan_config_path = lan_config_file
        self.wlan_config_path = wlan_config_file
        self.read_pardus_profiles()
        #self.transform_profiles()
        #self.write_new_profiles()

    def read_pardus_profiles(self):
        """Read wired/wireless profile settings, create PardusNetworkProfile 
        object for each one, and store them in a list.
        """

        self.lan_config = ConfigParser.ConfigParser()
        self.lan_config.read(self.lan_config_path)
        connection_type = "802-3-ethernet"
        for section in self.lan_config.sections():
            lan_settings = {}
            for option in self.lan_config.options(section):
                if option == "device":
                    #To strip device name from long device string
                    lan_settings[option] = self.lan_config.get(section, option).split("_")[-1]
                else:
                    lan_settings[option] = self.lan_config.get(section, option)
            p = PardusNetworkProfile(section, connection_type, lan_settings)
            self.pardus_profiles.append(p)

        self.wlan_config = ConfigParser.ConfigParser()
        self.wlan_config.read(self.wlan_config_path)
        connection_type = "802-11-wireless"
        for section in self.wlan_config.sections():
            wlan_settings = {}
            for option in self.wlan_config.options(section):
                if option == "device":
                    wlan_settings[option] = self.wlan_config.get(section, option).split("_")[-1]
                else:
                    wlan_settings[option] = self.wlan_config.get(section, option)
            p = PardusNetworkProfile(section, connection_type, wlan_settings)
            self.pardus_profiles.append(p)

    def transform_profiles(self):
        """Convert Pardus' network profiles to NetworkManager profiles"""

        for profile in self.pardus_profiles:
            network_manager_profile = NetworkManagerProfile(profile.get_profile_name, profile)
            self.network_manager_profiles.append(network_manager_profile)

    def write_network_manager_profiles(self):
        """Create profile file for each NetworkManager profile and change ownerships to 0600"""

        for profile in self.network_manager_profiles:
            profile.write_config()
            profile.set_ownership()


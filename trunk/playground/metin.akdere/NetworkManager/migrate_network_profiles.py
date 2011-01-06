#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to migrate network profiles from Pardus' network manager to new NetworkManager 
"""
import os
import sys
import shutil
import ConfigParser

NetworkManagerConfDir = "/etc/NetworkManager/system-connections"
NMConfDir = "/etc/network"


class PardusNMSettings:
    def __init__(self):

        self.lan_settings = {}
        self.wireless_settings = {}
        self.default_nameservers = []
        self.default_resolv_conf_file = "/etc/resolv.default.conf"

        self.lan_config_path = os.path.join(os.getcwd(), "net_tools")
        self.wireless_config_path = os.path.join(os.getcwd(), "wireless_tools")
        self.lan_config = ConfigParser.ConfigParser()
        self.lan_config.read(self.lan_config_path)
        self.wlan_config = ConfigParser.ConfigParser()
        self.wlan_config.read(self.wireless_config_path)

        self.retrieveLanProfileNames()
        self.retrieveWirelessProfileNames()

        self.readAllLanSettings()
        self.readAllWirelessSettings()

        self.readDefaultNameservers()

    def retrieveLanProfileNames(self):
        ''' A helper func to read all profile names, we will use a dict to keep 
        each setting in a corresponding profile name '''

        for section in self.lan_config.sections():
                self.lan_settings[section] = {"profile_name":section, "connection_type":"wired"}

    def retrieveWirelessProfileNames(self):
        ''' A helper func to read all profile names, we will use a dict to keep 
        each setting in a corresponding profile name '''

        for section in self.wlan_config.sections():
                self.wireless_settings[section] = {"profile_name":section,"connection_type":"wlan" }

    def readAllLanSettings(self):
        ''' Read wired profile settings of old network manager from given path '''

        for section in self.lan_config.sections():
            for option in self.lan_config.options(section):
                try:
                    if option == "device":
                        self.lan_settings[section][option] = self.lan_config.get(section, option).split("_")[-1]
                    else:
                        self.lan_settings[section][option] = self.lan_config.get(section, option)
                except:
                    self.lan_settings[section][option] = None

    def readAllWirelessSettings(self):
        ''' Read wireless profile settings of old network manager from given path '''

        for section in self.wlan_config.sections():
            for option in self.wlan_config.options(section):
                try:
                    if option == "device":
                        self.wireless_settings[section][option] = self.wlan_config.get(section, option).split("_")[-1]
                    else:
                        self.lan_settings[section][option] = self.lan_config.get(section, option)
                except:
                    self.wireless_settings[section][option] = None

    
    def readDefaultNameservers(self):
        ''' Read default DNS servers in resolve.default.conf '''

        # TODO: We should supply a default nameserver conf unless we find any
        nameservers_file = ""
        if os.path.exists(self.default_resolv_conf_file):
            try:
                file_pointer = open(self.default_resolv_conf_file)
                try:
                    nameservers_file = file_pointer.readlines()
                finally:
                    file_pointer.close()
            except:
                pass
        
        for line in nameservers_file:
            if not line.startswith("#") and line.startswith("nameserver"):
                ns = line.split()[-1]
                print ns
                self.default_nameservers.append(ns)

    def getLanProfileSettings(self, profile_name):
        ''' Return a dict that stores settings of the given LAN profile name '''

        for name, options in self.lan_settings.items():
            if name  == profile_name:
                return self.lan_settings.get(name)

    def getWirelessProfileSettings(self, profile_name):
        ''' Return a dict that stores settings of the given WLAN profile name '''

        for name, options in self.wireless_settings.items():
            if name  == profile_name:
                return self.wireless_settings.get(name)

    def getProfileNames(self, connection_type=None):
        ''' Returns the array of the profile names. Wired, wireless or both'''

        profiles = []
        if connection_type=='wired':
            for name, options in self.lan_settings.items():
                profiles.append(name)
            if len(profiles) > 0 :
                return profiles
            else:
                print "No %s connection settings found on your system!\n" % connection_type

        elif connection_type=='wireless':
            for name, options in self.wireless_settings.items():
                profiles.append(name)
            if len(profiles) > 0 :
                return profiles
            else:
                print "No %s connection settings found on your system!\n" % connection_type

        else:
            for name, options in self.lan_settings.items():
                profiles.append(name)
            for name, options in self.wireless_settings.items():
                profiles.append(name)
            if len(profiles) > 0 :
                return profiles
            else:
                print "No connection settings found on your system!\n"

    def getLanSettings(self):
        ''' Return a dict contains LAN settings'''

        return self.lan_settings

    def getWlanSettings(self):
        ''' Return a dict contains WLAN settings'''

        return self.wireless_settings

    def listProfiles(self, connection_type=None):
        ''' Temporary func to see a list of profiles '''

        print "*** LAN Profiles ***"
        for profile in self.getProfileNames('wired'):
            print profile
        print "\n*** WLAN Profiles ***"
        for profile in self.getProfileNames('wireless'):
            print profile

class NetworkManagerSettings:
    def __init__(self):

        self.pardus_nm_settings = PardusNMSettings()
        self.pardus_lan_settings = self.pardus_nm_settings.getLanSettings()
        self.pardus_wireless_settings = self.pardus_nm_settings.getWlanSettings()

        self.nm_profiles = {}
        self.config = ConfigParser.ConfigParser()

        #self.getConnectionType(self.old_settings)
        #self.getWiredSettings()
        #self.getWirelessSettings()

        #self.generateUUID()
        #self.writeSettings(self.pardus_nm_settings)

    # Helper functions
    def generateConfigFilename(self, settings):
        ''' Generate the new profile name from the given settings '''

        wired_profile_names = pardus_nm_settings.getProfileNames('wired')
        wireless_profile_names = pardus_nm_settings.getProfileNames('wireless')
        return wired_profile_names[1]


    def find_key(self, dic, key):
        ''' Return the value of dictionary dic given the key, to get the settings of the given profile name '''

        return [v for k, v in dic.iteritems() if k == key][0]

    def generateUUID(self):
        ''' Generate random type UUID '''
        import uuid

        return str(uuid.uuid4())

    def getMACAddress(self, iface):
        ''' Return MAC addresses of given interface on the machine using ifconfig, inspired from python uuid module '''

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

    def createTimeStamp(self):
        ''' NM says: " Timestamp (in seconds since the Unix Epoch) that the connection was last successfully activated. Settings services should update the connection timestamp periodically when the connection is active to ensure that an active connection has the latest timestamp"
        '''
        pass

    def decimal2binary(self, n):
        ''' Convert decimal octet value to binary format'''

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

    def calculatePrefix(self, net_mask):
        ''' Convert netmask value to CIDR prefix type which is between [1-32] as told in NM spec
            See http://mail.gnome.org/archives/networkmanager-list/2008-August/msg00076.html '''

        octets = net_mask.split(".")
        octet_in_binary = []
        netmask_value = 0
        for octet in octets:
            ret = self.decimal2binary(int(octet))
            octet_in_binary.append(ret)
        for i in "".join(octet_in_binary):
            if int(i) == 1 : netmask_value += 1
        return netmask_value

    def generateProfiles(self):
        ''' Decide what kind of profile types should be created and call regarding method '''

        for profile, options in self.pardus_lan_settings.items():
            for key, value in options.items():
                if options["net_mode"] == "auto":
                        self.createAutomaticLanSettings(options)
                if options["net_mode"] == "manual":
                        self.createManualLanSettings(options)


    def createAutomaticLanSettings(self, settings):
        ''' Create LAN settings, all addresses obtained from DHCP (IP, DNS etc.)'''

        cfg = ConfigParser.ConfigParser()
        profile_name = settings['profile_name']
        iface = settings['device']

        cfg.add_section('connection')
        cfg.add_section('ipv4')
        cfg.add_section('802-3-ethernet')
        cfg.add_section('ipv6')

        cfg.set('connection', 'id', profile_name)
        cfg.set('connection', 'uuid', self.generateUUID())
        cfg.set('connection', 'type', '802-3-ethernet')
        cfg.set('connection', 'autoconnect', 'false')

        cfg.set('ipv4', 'method', 'auto')
        self.chooseNameserverSettings(cfg, settings)

        cfg.set('802-3-ethernet', 'duplex', 'full')
        cfg.set('802-3-ethernet', 'mac-address', self.getMACAddress(iface))

        cfg.set('ipv6', 'method', 'ignore')

        self.writeSettings(cfg, profile_name)

    def createManualLanSettings(self, settings):
        ''' Create LAN settings, giving each address manually '''

        cfg = ConfigParser.ConfigParser()
        profile_name = settings['profile_name']
        iface = settings['device']

        cfg.add_section('connection')
        cfg.add_section('ipv4')
        cfg.add_section('802-3-ethernet')
        cfg.add_section('ipv6')

        cfg.set('connection', 'id', profile_name)
        cfg.set('connection', 'uuid', self.generateUUID())
        cfg.set('connection', 'type', '802-3-ethernet')
        cfg.set('connection', 'autoconnect', 'false')

        cfg.set('ipv4', 'method', 'manual')
        self.setNetworkAddresses(cfg, settings)
        self.chooseNameserverSettings(cfg, settings)

        cfg.set('802-3-ethernet', 'duplex', 'full')
        cfg.set('802-3-ethernet', 'mac-address', self.getMACAddress(iface))

        cfg.set('ipv6', 'method', 'ignore')

        self.writeSettings(cfg, profile_name)

    def chooseNameserverSettings(self, cfg, settings):
        ''' Decide whether to use default, custom or auto (DHCP assigned) nameservers '''

        default_nameservers = ";".join(self.pardus_nm_settings.default_nameservers)

        cfg.set('ipv4', 'ignoe-auto-dns', 'true')

        if settings["name_mode"] == "default":
            cfg.set('ipv4', 'dns', default_nameservers)
        elif settings["name_mode"] == "custom":
            cfg.set('ipv4', 'dns', settings['name_server'])

        # Nothing special is done in auto mode

    def setNetworkAddresses(self, cfg, settings):
        ''' Set network addresses from given settings '''

        net_mask = self.calculatePrefix(settings['net_mask'])

        # Get network address and gateway values and join them with ";"
        net_addresses = ";".join([settings['net_address'], str(net_mask), settings['net_gateway'], ""])
        cfg.set('ipv4', 'addresses1', net_addresses)

    def writeSettings(self, config, profile_name):
        ''' Create a config file and write the given settings '''

        with open(profile_name, 'wb') as configfile:
            config.write(configfile)


if __name__ == "__main__":
    ''' Magic happens '''

    old_settings = PardusNMSettings()
    old_settings.listProfiles()
    print old_settings.getLanProfileSettings('Şirket')

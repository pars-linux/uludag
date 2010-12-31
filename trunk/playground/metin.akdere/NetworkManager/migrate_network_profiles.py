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

# Map corresponding NM option to NetworkManager option
mapConfigOptions = {"id" : "profile_name",
                    "type" : "connection_type",
                    "method":"net_mode",
                    "dns" : "name_server",
                    "addresses" : ("net_address", "net_gateway"),
                    }

class PardusNMSettings:
    def __init__(self):

        self.lan_settings = {}
        self.wireless_settings = {}

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
                    self.lan_settings[section][option] = self.lan_config.get(section, option)
                except:
                    self.lan_settings[section][option] = None

    def readAllWirelessSettings(self):
        ''' Read wireless profile settings of old network manager from given path '''

        for section in self.wlan_config.sections():
            for option in self.wlan_config.options(section):
                try:
                    self.wireless_settings[section][option] = self.wlan_config.get(section, option)
                except:
                    self.wireless_settings[section][option] = None


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

        return self.wlan_settings

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
        self.nm_settings = {}

        self.pardus_lan_settings = self.pardus_nm_settings.getLansettings()
        self.pardus_wlan_settings = self.pardus_nm_settings.getWlansettings()

        self.config_filename = ''
        self.config = ConfigParser.ConfigParser()

        #self.getConnectionType(self.old_settings)
        #self.getWiredSettings()
        #self.getWirelessSettings()

        #self.generateUUID()
        self.writeSettings(self.pardus_nm_settings)

    # Helper functions
    def generateConfigFilename(self, settings):
        ''' Generate the new profile name from the given settings '''

        wired_profiles = old_settings.getProfileNames('wired')
        wireless_profiles = old_settings.getProfileNames('wireless')
        return wired_profiles[0]


    def find_key(self, dic, val):
        ''' Return the key of dictionary dic given the value '''

        return [k for k, v in dic.iteritems() if v == val][0]

    def generateUUID(self):
        pass

    def getMACAddress(self, device):
        pass

    def createTimeStamp(self):
        pass

    def createAutomaticLanSettings(self, pardus_nm_settings):
        ''' Create LAN settings, all addresses obtained from DHCP (IP, DNS etc.)'''

        lan_settings = pardus_nm_settings.getLanSettings()


    def createOnlyAutomaticLanSettings(self, lan_settings):
        ''' Create LAN settings, obtain addresses from DHCP except DNS servers '''

        pass

    def createManualLanSettings(self, lan_settings):
        ''' Create LAN settings, giving each address manually '''

        pass

    def writeSettings(self, settings):
        ''' Create a config file and write the given settings '''

        self.config_filename = self.generateConfigFilename(self.old_settings)
        #if not os.path.exists(os.path.join(os.getcwd(), self.config_filename)):
        #        cfgfile = open(os.path.join(os.getcwd(), self.config_filename), 'w')

        self.config.add_section('connection')
        self.config.add_section('ipv4')
        self.config.add_section('ipv6')
        self.config.add_section('802-3-ethernet')
        self.config.set('connection', 'id', self.generateConfigFilename(settings))
        self.config.set('connection', 'type', '802-3-ethernet')
        with open(self.config_filename, 'wb') as configfile:
            self.config.write(configfile)


if __name__ == "__main__":
    ''' Magic happens '''

    old_settings = PardusNMSettings()
    old_settings.listProfiles()
    print old_settings.getLanProfileSettings('lan')

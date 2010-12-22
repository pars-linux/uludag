#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to migrate network profiles from Pardus' network manager to new NetworkManager 
"""
import os
import shutil
import ConfigParser

class Migrator(object):
    def __init__(self):

        self.settings = {}
        self.config_path = "/etc/network/net_tools"
        self.lan_config = ConfigParser.ConfigParser()
        self.retrieveProfileNames(self.config_path)
        self.getOldSettings(self.config_path)

    def retrieveProfileNames(self, config_path):
        
        """ Read all profile names, we will use a dict to keep each setting in a corresponding profile name"""
        self.lan_config.read(config_path)
        for section in self.lan_config.sections():
            self.settings[section] = {}

    def getOldSettings(self, config_path):

        """ Read profile settings of old network manager from given path"""
        self.lan_config.read(config_path)
        for section in self.lan_config.sections():
            self.settings[section]['con_type'] = 'Ethernet' # FIXME : Do this automatically
            self.settings[section]['device'] = self.lan_config.get(section, "device")
            self.settings[section]['device_name'] = self.settings[section]['device'].split("_")[-1]
            self.settings[section]['name_mode'] = self.lan_config.get(section, "name_mode")
            self.settings[section]['net_mode'] = self.lan_config.get(section, "net_mode")

            if self.settings[section]['net_mode'] == "manual":    # We have assigned an IP address, netmask and gateway manually
                self.settings[section]['net_address'] = self.lan_config.get(section, "net_address")
                self.settings[section]['net_mask'] = self.lan_config.get(section, "net_mask")
                self.settings[section]['net_gateway'] = self.lan_config.get(section, "net_gateway")
            else:
                self.settings[section]['net_mask'] = None
                self.settings[section]['net_gateway'] = None
                self.settings[section]['net_address'] = None

if __name__ == "__main__":
    
    migrator = Migrator()

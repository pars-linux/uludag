#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to migrate network profiles from Pardus' network manager to new NetworkManager 
"""
import os
import sys
import shutil
import ConfigParser

class Migrator():
    def __init__(self):

        self.settings = {}
        self.config_path = os.path.join(os.getcwd(), "net_tools")
        self.lan_config = ConfigParser.ConfigParser()
        self.retrieveProfileNames(self.config_path)
        self.getOldLanSettings(self.config_path)

    def retrieveProfileNames(self, config_path):
        """ A helper func to read all profile names, we will use a dict to keep 
        each setting in a corresponding profile name """

        self.lan_config.read(config_path)
        for section in self.lan_config.sections():
            self.settings[section] = {}

    def getOldLanSettings(self, config_path):
        """ Read profile settings of old network manager from given path"""

        self.lan_config.read(config_path)
        for section in self.lan_config.sections():
            options = self.lan_config.options(section)
            for option in options:
                try:
                    self.settings[section][option] = self.lan_config.get(section, option)
                except:
                    self.settings[section][option] = None

    def getSettings(self, profile_name=None):
        """ Return a dict that stores settings of the given profile name """

        for name, options in self.settings.items():
            if name  == profile_name:
                return options

    def getProfileNames(self, connection_type=None):
        """ Returns the array of the profile names """
        profiles = []
        if connection_type:
            for name, options in self.settings.items():
                profiles.append(name)
            if len(profiles) > 0 :
                return profiles
            else:
                print "No %s connection settings found on your system!\n" % connection_type

        else:
            print "Usage getProfileNames(['wired', 'wireless'])"

if __name__ == "__main__":
    """Magic happens"""

    migrator = Migrator()
    print migrator.getSettings(migrator.getProfileNames('wired')[2])

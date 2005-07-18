# -*- conding: utf-8 -*-

# PISI Configuration File module, obviously, is used to read from the
# configuration file. Module also defines default values for
# configuration parameters.

# Configuration file is located in /etc/pisi/pisi.conf by default,
# having an INI like format like below.
#
#[general]
#destinationdirectory = /tmp
#
#[build]
#host = i686-pc-linux-gnu
#CFLAGS= -mcpu=i686 -O2 -pipe -fomit-frame-pointer
#CXXFLAGS= -mcpu=i686 -O2 -pipe -fomit-frame-pointer
#
#[dirs]
#lib_dir = /var/lib/pisi
#db_dir = /var/db/pisi
#archives_dir = /var/cache/pisi/archives
#packages_dir = /var/cache/pisi/packages
#tmp_dir = /var/tmp/pisi

import os
from ConfigParser import ConfigParser, NoSectionError


class ConfigException(Exception):
    pass

class GeneralDefaults:
    """Default values for [general] section"""
    destinationdirectory = os.getcwd() + "/tmp" # FOR ALPHA
    distribution = "Pardus"
    distribution_release = "0.1"

class BuildDefaults:
    """Default values for [build] section"""
    host = "i686-pc-linux-gnu"
    CFLAGS = "-mcpu=i686 -O2 -pipe -fomit-frame-pointer"
    CXXFLAGS= "-mcpu=i686 -O2 -pipe -fomit-frame-pointer"

class DirsDefaults:
    "Default values for [directories] section"
    lib_dir = "/var/lib/pisi"
    db_dir = "/var/db/pisi"
    archives_dir = "/var/cache/pisi/archives"
    packages_dir = "/var/cache/pisi/packages"
    tmp_dir =  "/var/tmp/pisi"

# bu bilgiyi burada tutmak mantıklı değil. bunun yerine kullanıcının
# kendi ev dizininde ayrı bir dosyada tutmak gerekiyor. Şimdilik bunu
# desteklemeyelim. Sonra hallederiz...
# class SvnDefaults:
#     """Default values for [svn] section """
#     username =  password = None

class ConfigurationSection(object):
    """ConfigurationSection class defines a section in the configuration
    file, using defaults (above) as a fallback."""
    def __init__(self, section, items=[]):
        self.items = items
        
        if section == "general":
            self.defaults = GeneralDefaults
        elif section == "build":
            self.defaults = BuildDefaults
        elif section == "directories":
            self.defaults = DirsDefaults
        else:
            e = "No section by name '%s'" % section
            raise ConfigException, e

        self.section = section

    def __getattr__(self, attr):
        if not self.items:
            if hasattr(self.defaults, attr):
                return getattr(self.defaults, attr)
            return ""
        for item in self.items:
            if item[0] == attr:
                return item[1]
        return ""


class ConfigurationFile(object):
    """Parse and get configuration values from the configuration file"""
    def __init__(self, filePath):
        parser = ConfigParser()
        self.filePath = filePath

        parser.read(self.filePath)

        try:
            generalitems = parser.items("general")
        except NoSectionError:
            generalitems = []
        self.general = ConfigurationSection("general", generalitems)

        try:
            builditems = parser.items("build")
        except NoSectionError:
            builditems = []
        self.build = ConfigurationSection("build", builditems)

        try:
            dirsitems = parser.items("directories")
        except NoSectionError:
            dirsitems = []
        self.dirs = ConfigurationSection("directories", dirsitems)

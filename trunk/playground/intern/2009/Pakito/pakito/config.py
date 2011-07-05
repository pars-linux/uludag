# -*- coding: utf-8 -*-

#TODO: KConfigSkeleton is more suitable, but it crashes? 

from kdecore import KSimpleConfig

class Config(KSimpleConfig):
    def __init__(self):
        KSimpleConfig.__init__(self, "pakitorc")
        self.packagerName = ""
        self.packagerEmail = ""
	self.rootPassword = ""
    
    def read(self):
        self.setGroup("Packager Information")
        self.packagerName = self.readEntry("Packager Name", "")
        self.packagerEmail = self.readEntry("Packager Email", "")
	self.rootPassword = self.readEntry("Root Password", "")
        
    def write(self):
        self.setGroup("Packager Information")
        self.writeEntry("Packager Name", self.packagerName)
        self.writeEntry("Packager Email", self.packagerEmail)
	self.writeEntry("Root Password", self.rootPassword)
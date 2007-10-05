# -*- coding: utf-8 -*-

#TODO: KConfigSkeleton is more suitable, but it crashes? 

from kdecore import KSimpleConfig

class Config(KSimpleConfig):
    def __init__(self):
        KSimpleConfig.__init__(self, "pakitorc")
        self.packagerName = ""
        self.packagerEmail = ""
    
    def read(self):
        self.setGroup("PackagerInformation")
        self.packagerName = self.readEntry("Packager Name", "")
        self.packagerEmail = self.readEntry("Packager Email", "")
        
    def write(self):
        self.setGroup("PackagerInformation")
        self.writeEntry("Packager Name", self.packagerName)
        self.writeEntry("Packager Email", self.packagerEmail)
#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar

class PardusTools:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()
        self.package = self.getMainPackage()

    def getPackages(self):
        return list(self.link.User.Manager)

    def getMainPackage(self):
        #FIX ME: This function is hardcoded.
        packages = self.getPackages()
        if not len(packages):
            return None
        return "mudur"

    def mount(self, device, path):
        self.link.Disk.Manager[self.package].mount(device, path)

    def umount(self, device):
        self.link.Disk.Manager[self.package].umount(device)

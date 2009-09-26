#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar

class PardusTools:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()

    def mount(self, device, path):
        self.link.Disk.Manager["mudur"].mount(device, path)

    def umount(self, device):
        self.link.Disk.Manager["mudur"].umount(device)

    def createSyslinux(self, device):
        self.link.Disk.Manager["puding"].createSyslinux(device)

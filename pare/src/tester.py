# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from pare import Pare

class Test(object):


    def __init__(self):
        self.pare = Pare()

    def testDevices(self):
        self.pare.storageInitialize()
        print "birinci"
        devices = None
        devices=self.pare.devices
        print devices
        if devices == None:
            print "Upss"
        for dev in devices:
            print dev.name


if __name__ == "__main__":
    test = Test()
    test.testDevices()
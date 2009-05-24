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

from pare.storage import Pare

class Test(object):


    def __init__(self):
        self.pare = Pare()

    def listDisks(self):
        disks = self.pare.disks
        for disk in disks:
            print "disk.path:%s" % disk.path
        
        return disks
    
    def listPartitions(self, disk):
        print "####"
        
        for part in self.pare.diskPartitions(disk):
                print "listPartitions--->   %s  partition minor %s" % (disk, part.minor)

if __name__ == "__main__":
    test = Test()
    disks = test.listDisks()
    print "len(disks):%d" % len(disks)
    for disk in disks:
        test.listPartitions(disk.path)
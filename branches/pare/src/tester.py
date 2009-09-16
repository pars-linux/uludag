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

from pare.storage import Storage
import parted

class Test(object):


    def __init__(self):
        self.pare = Storage()

    def listDisks(self):
        return self.pare.disks
        #for disk in disks:
         #   print "disk.path:%s" % disk.path

        return disks

    def listPartitions(self, disk):
        for part in self.pare.diskPartitions(disk):
                print "listPartitions--->   %s  partition path %s" % (disk.name, part.path)

    def physicalVolumes(self, disk):
        return self.pare.physicalVolumes(disk)

    def volumeGroups(self):
        vgs = self.pare.volumeGroups
        for vg in vgs:
            print "volumeGroups--> %s" % vg.name 

    def logicalVolumes(self):
        lvs = self.pare.logicalVolumes
        for lv in lvs:
            print "list logicalVolumes--> %s" % lv.name
        return lvs

    def addPartition(self, disk, partition,type, size, filesystem, flags):
        self.pare.addPartition(disk, partition, type, filesystem, size, flags)

    def getDiskPartition(self, disk, minor):
        return self.pare.getPartition(disk, minor)

    def commit2Disk(self, disk):
        self.pare.commitToDisk(disk)

    def deleteDiskPartition(self, disk, partition):
        self.pare.deletePartition(disk, partition)

    def removeLV(self, lv):
        print "lv.path : %s" % lv.path 
        self.pare.removeLV(lv)

if __name__ == "__main__":
    test = Test()
    #disks = test.listDisks()
    volumeGroups = test.volumeGroups()

    #for disk in disks:
    #    test.listPartitions(disk)

    #for disk in disks:
    #    physicalVolumes = test.physicalVolumes(disk)

    lvs = test.logicalVolumes()
    test.removeLV(lvs[0])
    #for disk in disks:
     #   if disk.path == "/dev/sdd":
     #       partition = test.getDiskPartition(disk.path, -1)
     #       #print "partition:%s" % partition.partition
     #       test.addPartition(disk, partition, parted.PARTITION_NORMAL, 300, "ext3", flags=[parted.PARTITION_BOOT,parted.PARTITION_LVM])
     #       #test.commit2Disk(disk.path)

    #for disk in disks:
     #   test.listPartitions(disk)

    #for disk in disks:
     #   if disk.path == "/dev/sdd":
     #       partition = test.getDiskPartition(disk.path, 3)
     #       print "partition:%s" % partition
     #       test.deleteDiskPartition(disk, partition)
     #       test.commit2Disk(disk.path)

    #for disk in disks:
     #   test.listPartitions(disk.path)


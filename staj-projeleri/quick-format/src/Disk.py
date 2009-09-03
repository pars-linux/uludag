#! /usr/bin/env python
import parted
import re

class disk:
    """Class to manipulate disks"""
    disks = []
    dev = None
    disk = None

    def __init__(self):
        """Find all the disks on on this system. So we know which to open."""
        self.find_disks()

    def __del__(self):
        """Destroy objects if we have them"""
        if self.disk:
            del self.disk
        if self.dev:
            del self.dev

    def open(self, name):
        """Open a disk. But only if we know it exists"""
        if name in self.disks:
            self.dev = parted.PedDevice.get('/dev/' + name)
            self.disk = parted.PedDisk.new(self.dev)
        else:
            print "Disk does not exsist"

    def list_partitions(self):
        """List all the partitions on a disk."""

        if (self.disk.get_last_partition_num() > 0):
            partition = self.disk.next_partition()
            partition = self.disk.next_partition(partition)

            while(partition.num > 0):
                print self.disk.dev.path, partition.num, partition.geom.length
                partition = self.disk.next_partition(partition)

    def clear_disk(self):
        """Delete all the partitions from a disk"""
        self.disk.delete_all()
        self.disk.commit()

    def find_disks(self):
        """Find all the Disk on the system"""
        f = open("/proc/partitions")
        txt = f.read()
        f.close()

        regex = re.compile("(\s+[0-9]+){3}\s")
        match = regex.search(txt)

        disks = dict()
        while (match != None):
            disk = txt[match.end():match.end()+3]

            if disk not in disks:
                disks[disk] = len(disks)

            txt = txt[match.end():]
            match = regex.search(txt)

        #Now turn into a list
        tmpdisks = []
        for (k,v) in disks.iteritems():
            tmpdisks.append([v,k])
        tmpdisks.sort()
        for i in range(len(tmpdisks)):
            self.disks.append(tmpdisks[i][1])

    def new_partition(self, size, fs, type):
        """Try to create a new partition"""
        fstype = parted.file_system_type_get_next()
        while (fstype != None and fstype.name != fs):
            fstype = parted.file_system_type_get_next(fstype)

        status = 0
        part = self.disk.next_partition()
        while part:
            #Check if we can use this
            if (part.type == parted.PARTITION_FREESPACE
                and part.geom.length >= size):
                newp = self.disk.partition_new(parted.PARTITION_PRIMARY, 
                                               fstype,
                                               part.geom.start, 
                                               part.geom.start + size)

                constraint = self.disk.dev.constraint_any ()
                try:
                    self.disk.add_partition (newp, constraint)
                    status = 1
                    break
                except parted.error:
                    print "Could not add disk"
            part = self.disk.next_partition(part)

        if not status:
            print "not enough free space"
        else:
            self.disk.commit()

    def mb2sectors(self, size):
        """Convert a size in mega bytes to sectors"""
        return size * 1024 * 1024 / self.dev.sector_size

    def sectors2mb(self, size):
        """Conver a size in sectors to megabytes"""
        return size * self.dev.sector / 1024 / 1024

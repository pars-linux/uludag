#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os
import sys
import copy
import glob
import parted

class DeviceError(Exception):
    pass

def getPartitionsOfDevice(device_path):
    """Returns all partitions of a given device but swap partition"""
    def getPartitionInfo(part):
        partition = {}
        if part.num >= 1:
            fs_name = ""
            if part.fs_type and part.fs_type.name != 'linux-swap':
                if part.fs_type.name == 'fat16' or part.fs_type.name == 'fat32':
                    part_type = 'vfat'
                elif part.fs_type.name == 'ntfs':
                    part_type = 'ntfs-3g'
                else:
                    part_type = part.fs_type.name
                return (device_path + str(part.num), {"mount_point": '',
                                                          "file_system": part_type,
                                                          "options": '',
                                                          "dump_freq": '0',
                                                          "fs_pass_no": '0'})
                return partition

    dev = parted.PedDevice.get(device_path)

    try:
        disk = parted.PedDisk.new(dev)
    except:
        label = archinfo['x86']["disklabel"]
        disk_type = parted.disk_type_get(label)
        disk = dev.disk_new_fresh(disk_type)

    part = disk.next_partition()
    while part:
        info = getPartitionInfo(part)
        if info:
            yield info
        part = disk.next_partition(part)

def getBlockDevices():
    """Returns a list of *non-removable* block devices attached to the system"""

    if not os.path.exists("/sys/block"):
        raise DeviceError, "sysfs not found!"

    devices = []

    for dev_type in ["hd*", "sd*"]:
        sysfs_devs = glob.glob("/sys/block/" + dev_type)
        for sysfs_dev in sysfs_devs:
            if not int(open(sysfs_dev + "/removable").read().strip()):
                devlink = os.readlink(sysfs_dev + "/device")
                if not "/usb" in devlink:
                    devices.append("/dev/" + os.path.basename(sysfs_dev))
    return devices

class FstabError(Exception):
    pass

class Fstab:
    def __init__(self, File = "/etc/fstab", debug = False):
        self.File = File
        self.Debug = debug
        if os.path.isfile(File):
            self.content = self.__emergeContent()
        else:
            self.content = []

        # basic syntax check of the content
        try:
            assert([x for x in self.content if len(x.split()) != 6] == [])
        except:
            raise FstabError, "Syntax of the fstab file doesn't seem to be correct"

        self.defaultMountDir = "/mnt"
        self.excludedFilesystems = ["proc", "tmpfs", "swap"]
        self.allDevices = getBlockDevices()

        self.defaultFileSystemOptions = {}
        self.defaultFileSystemOptions["vfat"] = "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6"
        self.defaultFileSystemOptions["ext3"] = "noatime"
        self.defaultFileSystemOptions["ext2"] = "noatime"
        self.defaultFileSystemOptions["ntfs-3g"] = "dmask=007,fmask=117,locale=tr_TR.UTF-8,gid=6"
        self.defaultFileSystemOptions["reiserfs"] = "noatime"
        self.defaultFileSystemOptions["xfs"] = "noatime"
        self.defaultFileSystemOptions["defaults"] = "defaults"

        self.update()

    def update(self):
        self.__allPartitions, self.__fstabPartitions = {}, {}

        self.__emergeAllPartitions()
        self.__emergeFstabPartitions()

        for p in self.__fstabPartitions.keys():
            if self.__allPartitions.get(p):
                self.__allPartitions[p].update(self.__fstabPartitions[p])

    def writeContent(self, File = None):
        if not self.Debug:
            if not File:
                File = self.File
            try:
                f = open(File, "w")
            except IOError:
                # raise FstabError, "Unable to write: %s"
                print "ERROR: Unable to write : %s" % self.File

            for line in self.content:
                f.write(line)
            f.close()
            return True
        else:
            for line in self.content:
                print line.rstrip("\n")

    def __emergeContent(self):
        return [line for line in open(self.File).readlines() if not line.startswith('#') if not line.startswith("\n")]

    def __emergeAllPartitions(self):
        for dev in self.allDevices:
            for info in [info for info in getPartitionsOfDevice(dev)]:
                self.__allPartitions[info[0]] = info[1]

    def __emergeFstabPartitions(self):
        for line in self.content:
            if line.split()[2] not in self.excludedFilesystems:
                self.__fstabPartitions[line.split()[0]] = {"mount_point": line.split()[1],
                                                        "file_system": line.split()[2],
                                                        "options": line.split()[3],
                                                        "dump_freq": line. split()[4],
                                                        "fs_pass_no": line.split()[5]}

    def getFstabPartitions(self):
        return self.__fstabPartitions

    def getAvailablePartitions(self):
        ap = {}
        for p in set(self.__allPartitions) - set(self.__fstabPartitions):
            ap[p] = copy.deepcopy(self.__allPartitions[p])
        return ap

    def addAvailablePartitions(self):
        """Adds all partitions that have no entries in fstab, 
           into fstab with default parameters"""
        for p in self.getAvailablePartitions():
            self.addFstabEntry(p, self.__allPartitions[p])

    def getDepartedPartitions(self):
        """Returns a list of partitions that have entries in fstab but also
        they do not exist anymore"""
        dp = {}
        for p in set(self.__fstabPartitions) - set(self.__allPartitions):
            dp[p] = copy.deepcopy(self.__fstabPartitions[p])
        return dp

    def delDepartedPartitions(self):
        """Removes partitions from fstab. These partitions have entries in fstab but also
        they do not exist anymore"""
        for p in self.getDepartedPartitions():
            self.delFstabEntry(p)

    def getAllPartitions(self):
        return self.__allPartitions

    def addFstabEntry(self, partition, attr_dict = {}):
        """Adds an fstab entry for 'partition', with attributes given in 'attr_dict'"""

        if not partition:
            ## print "DEBUG: 'partition' can not be null."
            return -1

        if attr_dict.get('mount_point') == '':
            attr_dict['mount_point'] = self.defaultMountDir + '/' + os.path.basename(partition)


        err = []
        if not self.__allPartitions.get(partition):
            err.append("ERROR: '%s' is not an available partition." % (partition))
        if self.__fstabPartitions.get(partition):
            self.delFstabEntry(partition)
        if err:
            print err
            return -1

        if attr_dict.get('file_system') == '':
            attr_dict['file_system'] = self.__allPartitions[partition]['file_system']

        if attr_dict.get('dump_freq') == '':
            attr_dict['dump_freq'] = '0'

        if attr_dict.get('fs_pass_no') == '':
            attr_dict['fs_pass_no'] = '0'

        if attr_dict.get('options') == '':
            attr_dict['options'] = self.defaultFileSystemOptions.get(attr_dict['file_system']) or self.defaultFileSystemOptions['defaults']

        if not self.Debug:
            if not os.path.exists(attr_dict['mount_point']):
                try:
                    os.mkdir(attr_dict['mount_point'])
                except OSError:
                    print ("ERROR: Unable to create mount point: '%s' for '%s'" % (attr_dict['mount_point'], partition))

        self.content.append("%-11s %-20s %-9s %-20s %s %s\n" % (partition, 
                                                         attr_dict['mount_point'], 
                                                         attr_dict['file_system'], 
                                                         attr_dict['options'], 
                                                         attr_dict['dump_freq'], 
                                                         attr_dict['fs_pass_no']))
        self.update()

    def delFstabEntry(self, partition):
        if not self.__fstabPartitions.get(partition):
            print("ERROR: There is not any fstab record for '%s'.\n" % (partition))
            return -1
        else:
            for c in range(0, len(self.content)):
                if self.content[c].split()[0] == partition:
                    self.content.remove(self.content[c])
                    self.update()
                    return 0

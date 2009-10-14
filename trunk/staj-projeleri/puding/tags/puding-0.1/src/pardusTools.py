#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3 (Read COPYING file.)
#

import comar
import glob
import os
import shutil

class Main:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

        self.file_list = self.getFileList()

    def getFileList(self):
        file_list = ["%s/pardus.img" % self.src]
        for i in glob.glob("%s/boot/*" % self.src):
            if os.path.isfile(i):
                file_list.append(i)
        file_list.extend(glob.glob("%s/repo/*" % self.src))

        return file_list

    def getNumberOfFiles(self):
        return len(self.file_list)

    def getTotalSize(self):
        total_size = 0
        for i in self.file_list:
            file_size = os.stat(i).st_size
            total_size += file_size

        return total_size / 1024 ** 2

    def copyFile(self, path):
        shutil.copyfile(path, "%s/%s" % (self.dst, path.split(self.src)[-1]))

class Authorization:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()

    def mount(self, device, path):
        self.link.Disk.Manager["mudur"].mount(device, path)

    def umount(self, device):
        self.link.Disk.Manager["mudur"].umount(device)

    def createSyslinux(self, device):
        self.link.Disk.Manager["puding"].createSyslinux(device)


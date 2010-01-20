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

        self.file_list = self.get_file_list()

    def get_file_list(self):
        file_list = ["%s/pardus.img" % self.src]
        for i in glob.glob("%s/boot/*" % self.src):
            if os.path.isfile(i):
                file_list.append(i)
        file_list.extend(glob.glob("%s/repo/*" % self.src))

        return file_list

    def get_number_of_files(self):
        return len(self.file_list)

    def get_total_size(self):
        total_size = 0
        for i in self.file_list:
            file_size = os.stat(i).st_size
            total_size += file_size

        return total_size / 1024 ** 2

    def copy_file(self, path):
        shutil.copyfile(path, "%s/%s" % (self.dst, path.split(self.src)[-1]))

class Authorization:
    def __init__(self):
        self.link = comar.Link()
        self.link.setLocale()

    def mount(self, device, path):
        self.link.Disk.Manager["mudur"].mount(device, path)

    def umount(self, device):
        self.link.Disk.Manager["mudur"].umount(device)

    def create_syslinux(self, device):
        self.link.Disk.Manager["puding"].create_syslinux(device)


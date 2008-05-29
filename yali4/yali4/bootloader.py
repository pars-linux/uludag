# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import glob

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from yali4.exception import *
from yali4.constants import consts
import yali4.sysutils
import yali4.partitiontype as parttype
import yali4.partitionrequest as request
from yali4.partitionrequest import partrequests
import yali4.gui.context as ctx

grub_conf_tmp = """\
default 0
timeout 10
gfxmenu /boot/grub/message
background 10333C

title %(pardus_version)s
root (%(grub_root)s)
kernel (%(grub_root)s)/boot/%(boot_kernel)s %(boot_parameters)s
initrd (%(grub_root)s)/boot/%(initramfs)s 

"""

win_part_tmp = """
title %(title)s (%(fs)s) - %(root)s
rootnoverify (%(grub_root)s)
makeactive
chainloader +1

"""

win_part_tmp_multiple_disks = """
title %(title)s (%(fs)s) - %(root)s
map (hd0) (hd1)
map (hd1) (hd0)
rootnoverify (%(grub_root)s)
makeactive
chainloader +1

"""


class BootLoader:
    """ Bootloader Operations 
        Default bootlader is GRUB """
    def __init__(self):
        self.device_map = os.path.join(consts.target_dir, "boot/grub/device.map")
        self.grub_conf = os.path.join(consts.target_dir, "boot/grub/grub.conf")

    def _find_grub_dev(self, dev_path):
        """ Returns the GRUB device from given dev_path
            It uses YALI's deviceMap created from EDD"""
        if dev_path.find("cciss") > 0:
            # HP Smart array controller (something like /dev/cciss/c0d0p1)
            dev_name = os.path.basename(dev_path)[:-2]
        else:
            dev_name = str(filter(lambda u: u.isalpha(),
                                  os.path.basename(dev_path)))

        for l in open(self.device_map).readlines():
            if l.find(dev_name) >= 0:
                l = l.split()
                d = l[0]
                # remove paranthesis
                return d[1:-1]

    def _find_hd0(self):
        """ Returns first disk from deviceMap """
        for l in open(self.device_map).readlines():
            if l.find("hd0") >= 0:
                l = l.split()
                # (hd0)   /dev/hda
                d = l[1]
                return d

    def write_grub_conf(self, install_root_path, install_dev, install_root_path_label):
        """ Check configurations and write grub.conf to the installed system.
            Default path is /mnt/target/boot/grub.conf """
        if not install_dev.startswith("/dev/"):
            install_dev = "/dev/%s" % install_dev

        # some paths has own directories like (/dev/cciss/c0d0p1)
        # it removes /dev/ and gets the device.
        install_root = install_root_path[5:]

        grub_dir = os.path.join(consts.target_dir, "boot/grub")
        if not os.path.exists(grub_dir):
            os.makedirs(grub_dir)

        # write an empty grub.conf, for grub to create a device map.
        open(self.grub_conf, "w").close()
        deviceMap = open(self.device_map, "w")
        i = 0

        # create device map
        for disk in ctx.installData.orderedDiskList:
            deviceMap.write("(hd%d)\t%s\n" % (i,disk))
            i+=1
        deviceMap.close()

        # cmd = "/sbin/grub --batch --no-floppy --device-map=%s < %s" % (self.device_map, self.grub_conf)
        # os.system(cmd)

        _grb = self._find_grub_dev(install_root_path)

        # grub_root is the device on which we install.
        minor = str(int(filter(lambda u: u.isdigit(), install_root)) -1)
        grub_root = ",".join([_grb, minor])

        def find_boot_kernel():
            """ Returns the installed kernel version """
            d = os.path.join(consts.target_dir, "boot")
            k = glob.glob(d + "/kernel-*")
            return os.path.basename(k[0])

        def find_initramfs_name(bk):
            """ Returns the installed initramfs name """
            ver = bk[len("kernel-"):]
            return "initramfs-%s" % ver

        def boot_parameters(root_label):
            """ Returns kernel parameters from cmd_line.
                It also cleans unnecessary options """

            def is_required(param):
                params = ["initrd","init","xorg","yali4","BOOT_IMAGE","lang","mudur",consts.kahyaParam]
                for p in params:
                    if param.startswith("%s=" % p):
                        return False
                return True

            s = []
            # Get parameters from cmdline.
            for i in [x for x in open("/proc/cmdline", "r").read().split()]:
                if i.startswith("root="):
                    s.append("root=LABEL=%s" % (root_label))
                elif is_required(i):
                    s.append(i)

            # a hack for http://bugs.pardus.org.tr/3345
            rt = request.mountRequestType
            pt = parttype.swap
            swap_part_req = partrequests.searchPartTypeAndReqType(pt, rt)
            if swap_part_req:
                s.append("resume=%s" %(swap_part_req.partition().getPath()))

            return " ".join(s).strip()

        boot_kernel = find_boot_kernel()
        initramfs_name = find_initramfs_name(boot_kernel)
        boot_parameters =  boot_parameters(install_root_path_label)
        s = grub_conf_tmp % {"root": install_root,
                             "grub_root": grub_root,
                             "pardus_version": consts.pardus_version,
                             "boot_kernel": boot_kernel,
                             "boot_parameters": boot_parameters,
                             "initramfs": initramfs_name}
        open(self.grub_conf, "w").write(s)

    def grub_conf_append_win(self, install_dev, win_dev, win_root, win_fs):
        """ Appends Windows Partitions to the GRUB Conf """
        grub_dev = self._find_grub_dev(win_dev)
        minor = str(int(filter(lambda u: u.isdigit(), win_root)) -1)
        grub_root = ",".join([grub_dev, minor])

        ctx.debugger.log("GCAW : win_dev : %s , win_root : %s " % (win_dev, win_root))
        ctx.debugger.log("GCAW : grub_dev: %s , grub_root: %s " % (grub_dev, grub_root))
        ctx.debugger.log("GCAW : install_dev: %s " % install_dev)

        if not install_dev:
            install_dev = self._find_hd0()

        ctx.debugger.log("GCAW :2install_dev: %s " % install_dev)

        dev_str = str(os.path.basename(install_dev))
        ctx.debugger.log("GCAW : dev_str: %s " % dev_str)

        if win_dev == dev_str:
            s = win_part_tmp % {"title": _("Windows"),
                                "grub_root": grub_root,
                                "root": win_root,
                                "fs": win_fs}
        else:
            s = win_part_tmp_multiple_disks % {"title": _("Windows"),
                                               "grub_root": grub_root,
                                               "root": win_root,
                                               "fs": win_fs}

        open(self.grub_conf, "a").write(s)

    def install_grub(self, grub_install_root=None):
        """ Install GRUB to the given device or partition """

        if not grub_install_root.startswith("/dev/"):
            grub_install_root = "/dev/%s" % grub_install_root

        cmd = "%s --root-directory=%s %s --no-floppy" % (yali4.sysutils.find_executable("grub-install"),
                                             consts.target_dir,
                                             grub_install_root)

        ctx.debugger.log("IG : cmd: %s " % cmd)

        if os.system(cmd) != 0:
            raise YaliException, "Command failed: %s" % cmd
        else:
            return True
        return False


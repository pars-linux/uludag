#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3 (Read COPYING file.)
#

import dbus
import glob
import os
import shutil
import subprocess
import tempfile

from puding.constants import LOCALE
from puding.constants import SYSLINUX
from puding.releases import releases
from puding.resources import ResourceManager

def get_disk_info(dst):
    disk_info = os.statvfs(dst)
    capacity = int(disk_info.f_bsize * disk_info.f_blocks / 1024**2)
    available = int(disk_info.f_bsize * disk_info.f_bavail / 1024**2)
    used = int(disk_info.f_bsize * (disk_info.f_blocks - disk_info.f_bavail) / 1024**2)

    return [capacity, available, used]

def get_iso_size(src):
    return os.stat(src).st_size

def get_file_size(file):
    file_size = os.stat(file).st_size / 1024.0**2

    return file_size

def get_mounted(disk_path):
    parts = {}
    for line in open("/proc/mounts"):
        if line.startswith("/dev/"):
            device, path, other = line.split(" ", 2)
            parts[path] = device

    return parts[disk_path.replace(" ", "\\040")]

def run_command(cmd):
    process = subprocess.call(cmd, shell = True)

    return process

def create_config_file(iso_dir, dst):
    res = ResourceManager()
    conf_dir = os.path.join(dst, "boot", "syslinux")
    isolinux_dir = os.path.join(iso_dir, "boot", "isolinux")
    conf_files = [os.path.join(isolinux_dir, "gfxboot.com"),
        os.path.join(isolinux_dir, "hdt.c32")]
    conf_files.extend(glob.glob(os.path.join(res.DEV_HOME, "datas", "gfxtheme", "*")))

    for i in conf_files:
        file_name = os.path.split(i)[-1]
        if not os.path.exists(os.path.join(conf_dir, file_name)):
            shutil.copyfile(i, os.path.join(conf_dir, file_name))

    syslinux_conf_file = os.path.join(conf_dir, "syslinux.cfg")
    if not os.path.exists(syslinux_conf_file):
        shutil.copyfile(res.get_data_file(os.path.join("datas", "syslinux.cfg.pardus")), syslinux_conf_file)

def create_syslinux(iso_dir, dst):
    create_config_file(iso_dir, dst)

    sys_file = os.path.join(dst, "ldlinux.sys")
    if os.path.exists(sys_file):
        os.remove(sys_file)

    # FIX ME: Should use PartitionUtils
    device = os.path.split(get_mounted(dst))[1][:3]
    cmd = "cat /usr/lib/syslinux/mbr.bin > /dev/%s" % device
    if run_command(cmd):
        return False

    cmd = "LC_ALL=C syslinux %s" % get_mounted(dst)
    return run_command(cmd)

def create_USB_dirs(dst):
    dirs = ("repo", "boot/syslinux")

    for d in dirs:
        path = "%s/%s" % (dst, d)
        if not os.path.exists(path):
            os.makedirs(path)

def unmount_dirs():
    # BAD CODE:
    for line in open("/proc/mounts"):
        path = line.split(" ", 2)[1]
        if path.endswith("Puding"):
            run_command("umount %s" % path)

    tempdir = tempfile.gettempdir()
    for puding_dir in glob.glob("%s/*Puding" % tempdir):
        os.rmdir(puding_dir)

class PartitionUtils:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.drives = {}
        self.devices = []
        self.label = "PARDUS_USB"

    def return_drives(self):
        return self.drives

    def format_device(self, dst):
        cmd = "mkfs.vfat -F 32 %s" % dst

        return run_command(cmd)

    def get_device(self, device):
        dev_obj = self.bus.get_object("org.freedesktop.Hal", device)

        return dbus.Interface(dev_obj, "org.freedesktop.Hal.Device")

    def add_device(self, dev, parent = None):
        mount = str(dev.GetProperty("volume.mount_point"))
        device = str(dev.GetProperty("block.device"))

        self.drives[device] = {
            "label" : str(dev.GetProperty("volume.label")).replace(" ", "_"),
            "fstype"   : str(dev.GetProperty("volume.fstype")),
            "fsversion": str(dev.GetProperty("volume.fsversion")),
            "uuid"     : str(dev.GetProperty("volume.uuid")),
            "mount"    : mount,
            "device"   : dev,
            "unmount"  : False,
            "device"   : device,
            "parent"   : parent.GetProperty("block.device")
            }

    def detect_removable_drives(self):
        hal_obj = self.bus.get_object("org.freedesktop.Hal",
                                 "/org/freedesktop/Hal/Manager")
        hal = dbus.Interface(hal_obj, "org.freedesktop.Hal.Manager")

        devices = hal.FindDeviceByCapability("storage")

        for device in devices:
            dev = self.get_device(device)

            if dev.GetProperty("storage.bus") == "usb":
                if dev.GetProperty("block.is_volume"):
                    self.add_device(dev)

                    continue

                else:
                    children = hal.FindDeviceStringMatch("info.parent", device)

                    for child in children:
                        child = self.get_device(child)

                        if child.GetProperty("block.is_volume"):
                            self.add_device(child, parent = dev)

        if not len(self.drives):
            return False

        else:
            return True

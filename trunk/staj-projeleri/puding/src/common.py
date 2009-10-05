#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import dbus
import gettext
import glob
import os
import shutil
import subprocess

from constants import HOME
from constants import MOUNT_ISO
from constants import MOUNT_USB
from constants import NAME
from constants import LOCALE
from constants import SHARE
from constants import SYSLINUX

from releases import releases

t = gettext.translation(NAME, LOCALE, fallback = True)
_ = t.ugettext

def getDiskInfo(dst):
    disk_info = os.statvfs(dst)
    capacity = int(disk_info.f_bsize * disk_info.f_blocks / 1024**2)
    available = int(disk_info.f_bsize * disk_info.f_bavail / 1024**2)
    used = int(disk_info.f_bsize * (disk_info.f_blocks - disk_info.f_bavail) / 1024**2)

    return [capacity, available, used]

def getIsoSize(src):
    return os.stat(src).st_size

def getFileSize(file):
    file_size = os.stat(file).st_size / 1024.0**2

    return file_size

def getNumberOfFiles(src):
    all_files = []
    all_files.extend(glob.glob("%s/repo/*" % src))
    boot_files = glob.glob("%s/boot/*" % src)
    for file in boot_files:
        if os.path.isfile(file):
            all_files.append(file)
    all_files.append("%s/pardus.img" % src)

    return len(all_files)

def runCommand(cmd):
    process = subprocess.call(cmd, shell = True)

    return process

def run(cmd):
    process = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               stdin = subprocess.PIPE)

    result = process.communicate()

    return process, result

def copyPisiPackage(file, dst, pisi):
    shutil.copy(file, "%s/repo/%s" % (dst, pisi))

    return pisi

def createConfigFile(dst):
    conf_dir = "%s/boot/syslinux" % dst
    conf_files = ["%s/gfxboot.com" % SYSLINUX, "%s/hdt.c32" % SYSLINUX]
    conf_files.extend(glob.glob("%s/gfxtheme/*" % SHARE))

    for file in conf_files:
        file_name = os.path.split(file)[1]
        if not os.path.exists("%s/%s" % (conf_dir, file_name)):
            shutil.copyfile(file, "%s/%s" % (conf_dir, file_name))

    syslinux_conf_file = "%s/syslinux.cfg" % conf_dir
    if not os.path.exists(syslinux_conf_file):
        shutil.copyfile("%s/syslinux.cfg.pardus" % SHARE, syslinux_conf_file)

def createSyslinux(dst):
    createConfigFile(dst)

    sys_file = "%s/ldlinux.sys" % dst
    if os.path.exists(sys_file):
        os.remove(sys_file)

    # FIX ME: Should use PartitionUtils
    device = os.path.split(getMounted(dst))[1][:3]
    cmd = "cat /usr/lib/syslinux/mbr.bin > /dev/%s" % device
    if runCommand(cmd):
        return False

    cmd = "LC_ALL=C syslinux %s" % getMounted(dst)
    return runCommand(cmd)

def createSyslinux_old(dst):
    sys_file = "%s/ldlinux.sys" % dst
    if os.path.exists(sys_file):
        os.remove(sys_file)

    cmd = "LC_ALL=C syslinux %s" % getMounted(dst)

    return runCommand(cmd)

def getMounted(disk_path):
    parts = {}
    for line in open("/proc/mounts"):
        if line.startswith("/dev/"):
            device, path, other = line.split(" ", 2)
            parts[path] = device

    return parts[disk_path]

def createDirs():
    if not os.path.exists(HOME):
        os.makedirs(MOUNT_ISO)
        os.mkdir(MOUNT_USB)

def createUSBDirs(dst):
    dirs = ("repo", "boot/syslinux")

    for d in dirs:
        path = "%s/%s" % (dst, d)
        if not os.path.exists(path):
            os.makedirs(path)

class PartitionUtils:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.drives = {}
        self.devices = []
        self.label = "PARDUS_USB"

    def returnDrives(self):
        return self.drives

    def formatDevice(self, dst):
        cmd = "mkfs.vfat -F 32 %s" % dst

        return runCommand(cmd)

    def getDevice(self, device):
        dev_obj = self.bus.get_object("org.freedesktop.Hal", device)

        return dbus.Interface(dev_obj, "org.freedesktop.Hal.Device")

    def addDevice(self, dev, parent = None):
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

    def detectRemovableDrives(self):
        hal_obj = self.bus.get_object("org.freedesktop.Hal",
                                 "/org/freedesktop/Hal/Manager")
        hal = dbus.Interface(hal_obj, "org.freedesktop.Hal.Manager")

        devices = hal.FindDeviceByCapability("storage")

        for device in devices:
            dev = self.getDevice(device)

            if dev.GetProperty("storage.bus") == "usb":
                if dev.GetProperty("block.is_volume"):
                    self.addDevice(dev)

                    continue

                else:
                    children = hal.FindDeviceStringMatch("info.parent", device)

                    for child in children:
                        child = self.getDevice(child)

                        if child.GetProperty("block.is_volume"):
                            self.addDevice(child, parent = dev)


        if not len(self.drives):
            return False

        else:
            return True

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import gzip
import pisi
import shutil


sysdir = "/sys/bus/pci/devices/"
driversDB = "/usr/share/X11/DriversDB"

grub_file = "/boot/grub/grub.conf"
grub_new = "/boot/grub/grub.conf.new"
grub_back = "/boot/grub/grub.conf.back"
kernel_file = "/etc/kernel/kernel"
kernel_file_pae = "/etc/kernel/kernel-pae"

fglrx = {"fglrx": ["module-fglrx-userspace",
                   "xorg-video-fglrx",
                   "ati-control-center"]}

nvidia_current = {"nvidia-current": ["module-nvidia-current-userspace",
                                     "xorg-video-nvidia-current",
                                     "nvidia-settings"]}

nvidia96 = {"nvidia96": ["module-nvidia96-userspace",
                         "xorg-video-nvidia96",
                         "nvidia-settings"]}

nvidia173 = {"nvidia173": ["module-nvidia173-userspace",
                           "xorg-video-nvidia173",
                           "nvidia-settings"]}

def edit_grub(driver_name):
    if driver_name == "nvidia-current":
        os_driver = "nouveau"
    elif driver_name == "fglrx":
        os_driver = "radeon"
    else:
        os_driver = False

    kernel_version = get_kernel_flavor()

    # Get the current used kernel versio    # Create a new grub file
    # Do not change the file if blacklist= .. is already available
    grub_tmp = open(grub_new, "w")
    with open(grub_file) as grub:
        for line in grub:
            if "kernel" in line and kernel_version in line:
                if "blacklist" in line or not os_driver:
                    print "Grub.conf is already configured"
                    configured = False
                    grub_tmp.write(line)
                elif os_driver:
                    kernel_parameters = line.split()
                    kernel_parameters.append("blacklist=%s \n" % os_driver)
                    new_kernel_line = " ".join(kernel_parameters)
                    grub_tmp.write(new_kernel_line)
                    configured = True
                    print "The parameter \"blacklist=%s\" is added to Grub.conf" % os_driver
            else:
                grub_tmp.write(line)
    grub_tmp.close()

    #Replace the new grub file with the old one, create also a backup file
    if configured:
        shutil.copy2(grub_file, grub_back)
        print "Backup of grub file is created: /boot/grub/grub.conf.back"

        shutil.copy2(grub_new, grub_file)
        print "New grub file is created: /boot/grub/grub.conf"

def resolve_intersections():
    obsolote = []
    needed = []

    driver_name = get_primary_driver()
    module_name = get_kernel_module_package(driver_name)

    packages_dicts = [nvidia_current, nvidia96, nvidia173, fglrx]
    for package in packages_dicts:
        for driver, module in package.items():
            module.append(module_name)
            package[driver] = module
            if driver_name != driver:
                obsolote.append(package)
            else:
                needed.append(package)

    return (needed, obsolote)

def get_kernel_module_package(name):
    '''Get the appropirate module for the specified kernel'''
    kernel_flavor = get_kernel_flavor()

    if "pae" in kernel_flavor:
        config = gzip.open("/proc/config.gz").read()
        for option in config:
            if "X86_PAE=y" in option:
                return "module-pae-%s" % name
            else:
                return "module-%s" % name
    else:
        return "module-%s" % name

def get_kernel_flavor():
    ''' Get kernel version '''
    if os.path.exists(kernel_file_pae):
        with open(kernel_file_pae) as kernel:
            for line in kernel:
                return line
    else:
        with open(kernel_file) as kernel:
            for line in kernel:
                return line

def get_primary_driver():
    '''Get driver name for the working primary device'''
    for boot_vga in glob.glob("%s/*/boot_vga" % sysdir):
        if open(boot_vga).read().startswith("1"):
            dev_path = os.path.dirname(boot_vga)
            vendor = open(os.path.join(dev_path, "vendor")).read().strip()
            device = open(os.path.join(dev_path, "device")).read().strip()
            device_id = vendor[2:] + device[2:]

            for line in open(driversDB):
                if line.startswith(device_id):
                    driver_name = line.split()[1]
    return driver_name

if __name__ == '__main__':
    needed, obsolote = resolve_intersections()

    print
    print "The package name of the driver is     : %s" % driver_name
    print
    print "Packages that should be installed : %s" % needed
    print "Packages that should be removed   : %s" % obsolote
    print

    edit_grub(driver_name)


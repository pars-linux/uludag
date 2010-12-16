#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import gzip
import pisi
import shutil

# This scripts automatically detects the brand of a graphic card
# After detecting, it simply returns a list which contains modules
# that should be added/installed. These modules are mostly based on
# proprietary graphic card drivers.
# This script also has a extra function that modify grub.conf to
# reflect the changes of the installed modules. It does append a
# "blacklist=..." string to the end of kernel line in grub.conf. Due
# to one will able to use the proprietary drivers like nvidia-current
# or fglrx


# System files and directories
sysdir = "/sys/bus/pci/devices/"
driversDB = "/usr/share/X11/DriversDB"

grub_file = "/boot/grub/grub.conf"
grub_new = "/boot/grub/grub.conf.new"
grub_back = "/boot/grub/grub.conf.back"
kernel_file = "/etc/kernel/kernel"
kernel_file_pae = "/etc/kernel/kernel-pae"

# This dict contains all module sthat should be removed first
# After that we add only modules that we need
driver_packages = {"fglrx": ["module-fglrx",
                             "module-pae-fglrx",
                             "module-fglrx-userspace",
                             "xorg-video-fglrx",
                             "ati-control-center"] ,
                   "nvidia-current": ["module-nvidia-current",
                                      "module-pae-nvidia-current",
                                      "module-nvidia-current-userspace",
                                      "xorg-video-nvidia-current",
                                      "nvidia-settings"] ,
                   "nvidia96": ["module-nvidia96",
                                "module-pae-nvidia96",
                                "module-nvidia96-userspace",
                                "xorg-video-nvidia96",
                                "nvidia-settings"],
                   "nvidia173": ["module-nvidia173",
                                 "module-pae-nvidia173",
                                 "module-nvidia173-userspace",
                                 "xorg-video-nvidia173",
                                 "nvidia-settings"]}

def edit_grub(driver_name):
    '''Edit grub file to enable the use of propretiary graphic card drivers'''
    if driver_name == "nvidia-current":
        os_driver = "nouveau"
    elif driver_name == "fglrx":
        os_driver = "radeon"
    else:
        os_driver = False

    kernel_list = get_kernel_flavors()
    kernel_version = kernel_list["kernel"] # This one should change

    # Get the current used kernel version
    # Create a new grub file
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

def needed_module():
    '''Filter modules that should be addded'''
    module_to_install ={}
    driver_name = get_primary_driver()
    kernel_list = get_kernel_module_package(driver_name)

    # List only kernel_flavors, we assume that a kernel flavor begins with "module-" and ends with "-userspace"
    kernel_flavors = filter(lambda x: x.startswith("module-") and not x.endswith("-userspace"), \
                            driver_packages[driver_name])

    # Kernel_list contains currently used kernel modules
    # Kernel_flavors contains predefined kernel modules
    # driver_package[driver_name] contains all modules 
    # All modules should be stay nontouched, but remove kernels in kernel_flavors that are not in kernel_list
    # (hence we are not using them)
    need_to_install = list(set(driver_packages[driver_name]) - (set(kernel_flavors)- set(kernel_list)))
    module_to_install[driver_name]  = need_to_install

    return module_to_install

def get_kernel_module_package(driver_name):
    '''Get the appropirate module for the specified kernel'''
    kernel_flavor = get_kernel_flavors()

    kernel_list=[]
    for kernel_name, kernel_version in kernel_flavor.items():
        tmp, sep, suffix = kernel_name.partition("-")
        if suffix:
            kernel_list.append("module-%s-%s" % (suffix, driver_name))
        else:
            kernel_list.append("module-%s" % driver_name)

    return kernel_list

def get_kernel_flavors(param=False):
    ''' Get kernel version '''
    kernel_dict = {}

    if not param:
        for kernel_file in glob.glob("/etc/kernel/*"):
            kernel_name = os.path.basename(kernel_file)
            kernel_dict[kernel_name] = open(kernel_file).read()
    else:
        # We might want to give custom parameters
        # The below on is just an example
        kernel_dict[param] = "2.6.36.1-147"

    return kernel_dict

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
    driver_name = get_primary_driver()
    needed = needed_module()

    print
    print "Packages that should be added to list        : %s" % needed
    print
    print "Packages that should be removed from list    : %s" % driver_packages
    print
    edit_grub(driver_name)


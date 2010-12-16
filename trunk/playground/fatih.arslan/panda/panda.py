#!/usr/bin/python
# -*- coding: utf-8 -*-
# This scripts automatically detects the brand of a graphic card
# After detecting, it simply returns a list which contains modules
# that should be added/installed. These modules are mostly based on
# proprietary graphic card drivers.
# This script also has a extra function that modify grub.conf to
# reflect the changes of the installed modules. It does append a
# "blacklist=..." string to the end of kernel line in grub.conf. Due
# to one will able to use the proprietary drivers like nvidia-current
# or fglrx


import os
import sys
import glob
import gzip
import pisi
import shutil

# System files and directories
sysdir = "/sys/bus/pci/devices/"
driversDB = "/usr/share/X11/DriversDB"

grub_file = "/boot/grub/grub.conf"
grub_new = "/boot/grub/grub.conf.new"
grub_back = "/boot/grub/grub.conf.back"
kernel_file = "/etc/kernel/kernel"
kernel_file_pae = "/etc/kernel/kernel-pae"

def get_blacklisted_packages():
    driver_name = get_primary_driver()

    for driver in ["nvidia-current", "nvidia96", "nvidia173"]:
        if driver_name == driver:
            return "blacklist=nouveau"

    if driver_name == "fglrx":
        return "blacklist=radeon"
    else:
        return None

def update_grub_entries():
    '''Edit grub file to enable the use of propretiary graphic card drivers'''
    os_driver = get_blacklisted_packages()
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

def get_all_driver_packages():
    '''This dict contains all module sthat should be removed first'''
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

    return driver_packages

def get_needed_driver_packages(kernel_param=None):
    '''Filter modules that should be addded'''
    driver_name = get_primary_driver()
    driver_packages = get_all_driver_packages()
    kernel_list = get_kernel_module_package(kernel_param)

    # List only kernel_flavors, we assume that a kernel flavor begins with "module-" and ends with "-userspace"
    kernel_flavors = filter(lambda x: x.startswith("module-") and not x.endswith("-userspace"), \
                            driver_packages[driver_name])

    # Kernel_list contains currently used kernel modules
    # Kernel_flavors contains predefined kernel modules
    # driver_package[driver_name] contains all modules 
    # All modules should be stay nontouched, but remove kernels in kernel_flavors that are not in kernel_list
    # (hence we are not using them)
    need_to_install = list(set(driver_packages[driver_name]) - (set(kernel_flavors)- set(kernel_list)))

    return need_to_install

def get_kernel_module_package(kernel_param=None):
    '''Get the appropirate module for the specified kernel'''
    driver_name = get_primary_driver()
    kernel_flavor = get_kernel_flavors(kernel_param=None)

    kernel_list=[]
    if isinstance(kernel_flavor, dict):
        kernel_iter = kernel_flavor.keys()
    else:
        kernel_iter = kernel_flavor

    for kernel_name in kernel_iter:
        tmp, sep, suffix = kernel_name.partition("-")
        if suffix:
            kernel_list.append("module-%s-%s" % (suffix, driver_name))
        else:
            kernel_list.append("module-%s" % driver_name)

    return kernel_list

def get_kernel_flavors(kernel_param=None):
    ''' Get kernel version '''
    kernel_dict = {}

    if kernel_param is None:
        for kernel_file in glob.glob("/etc/kernel/*"):
            kernel_name = os.path.basename(kernel_file)
            kernel_dict[kernel_name] = open(kernel_file).read()
        return kernel_dict
    else:
        # We might want to give custom parameters
        return kernel_param

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

    print "You have to import this module"



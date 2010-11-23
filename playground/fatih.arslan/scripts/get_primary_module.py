#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import gzip

sysdir = "/sys/bus/pci/devices/"
driversDB = "/usr/share/X11/DriversDB"

packages = {"nvidia-current": ("xorg-video-nvidia-current",
                               "nvidia-settings")}

def get_kernel_module_package(kernel_flavor, name):
    '''Get the appropirate module for the specified kernel'''
    if kernel_flavor == "pae":
        config = gzip.open("/proc/config.gz").read()
        for option in config:
            if "X86_PAE=y" in option:
                return "module-pae-%s" % name
            else:
                return "module-%s" % name
    else:
        return "module-%s" % name

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
    module_name = get_kernel_module_package(None, driver_name)
    
    print driver_name, module_name
    #sys.exit(returnDevName())


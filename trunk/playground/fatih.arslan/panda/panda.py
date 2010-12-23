#!/usr/bin/python
# -*- coding: utf-8 -*-


# PANDA - Pardus Alternative Driver Administration
#
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

sysdir = "/sys/bus/pci/devices/"
driversDB = "/usr/share/X11/DriversDB"

grub_file = "/boot/grub/grub.conf"
grub_new = "/boot/grub/grub.conf.new"
grub_back = "/boot/grub/grub.conf.back"
kernel_file = "/etc/kernel/kernel"
kernel_file_pae = "/etc/kernel/kernel-pae"

class Panda():
    '''Pardus Alternative Driver Administration'''
    def __init__ (self):
        self.driver_name = None
        self.driver_packages = None
        self.kernel_flavors = None
        self.os_driver = None

    def __get_primary_driver(self):
        '''Get driver name for the working primary device'''
        for boot_vga in glob.glob("%s/*/boot_vga" % sysdir):
            if open(boot_vga).read().startswith("1"):
                dev_path = os.path.dirname(boot_vga)
                vendor = open(os.path.join(dev_path, "vendor")).read().strip()
                device = open(os.path.join(dev_path, "device")).read().strip()
                device_id = vendor[2:] + device[2:]

                for line in open(driversDB):
                    if line.startswith(device_id):
                        self.driver_name = line.split()[1]

                if not self.driver_name:
                    self.driver_name = "Not defined"

        return self.driver_name

    def __get_kernel_module_packages(self, kernel_list=None):
        '''Get the appropirate module for the specified kernel'''
        if not kernel_list:
            if self.kernel_flavors is None:
                self.__get_kernel_flavors()
                kernel_list = self.kernel_flavors.keys()

        if self.driver_name is None:
            self.__get_primary_driver()

        module_packages = []
        for kernel_name in kernel_list:
            tmp, sep, suffix = kernel_name.partition("-")
            if suffix:
                module_packages.append("module-%s-%s" % (suffix, self.driver_name))
            else:
                module_packages.append("module-%s" % self.driver_name)

        return module_packages

    def __get_kernel_flavors(self):
        ''' Get kernel version '''
        kernel_dict = {}

        for kernel_file in glob.glob("/etc/kernel/*"):
            kernel_name = os.path.basename(kernel_file)
            kernel_dict[kernel_name] = open(kernel_file).read()

        self.kernel_flavors = kernel_dict

    def __get_blacklisted_packages(self):
        if self.driver_name is None:
            self.__get_primary_driver()

        if self.driver_name == "fglrx":
            self.os_driver = "radeon"
        elif self.driver_name in ["nvidia-current", "nvidia96", "nvidia173"]:
            self.os_driver = "nouveau"


    def get_needed_driver_packages(self, kernel_flavors=None):
        '''Filter modules that should be addded'''
        if self.driver_packages is None:
            self.get_all_driver_packages()

        needed_module_packages = self.__get_kernel_module_packages(kernel_flavors)

        if not self.driver_name == "Not defined":
            # List only kernel_flavors, we assume that a kernel flavor begins with
            # "module-" and does not end with "-userspace"
            module_packages = filter(lambda x: x.startswith("module-") and not x.endswith("-userspace"), \
                                    self.driver_packages[self.driver_name])

            # Kernel_list contains currently used kernel modules
            # Kernel_flavors contains predefined kernel modules
            # driver_package[driver_name] contains all modules 
            # All modules should be stay nontouched, but remove kernels in kernel_flavors
            # that are not in kernel_list (hence we are not using them)

            need_to_install = list(set(self.driver_packages[self.driver_name]) - \
                                   (set(module_packages) - set(needed_module_packages)))

            return need_to_install
        else:
            return []

    def get_all_driver_packages(self):
        '''This dict contains all module sthat should be removed first'''
        self.driver_packages = {"fglrx": ["module-fglrx",
                                     "module-pae-fglrx",
                                     "module-fglrx-userspace",
                                     "xorg-video-fglrx"],
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
        return self.driver_packages

    def update_grub_entries(self, arg="auto"):
        '''Edit grub file to enable the use of propretiary graphic card drivers'''
        if self.os_driver is None:
            self.__get_blacklisted_packages()

        if self.kernel_flavors is None:
            self.__get_kernel_flavors()

        kernel_version = self.kernel_flavors["kernel"] # This one should change

        if arg == "vendor" and self.os_driver is None:
            print "I'm not able to install vendor drivers"
            return
        elif arg:
            pass
        else:
            return "Wrong parameter!\" You can use: vendor or os"


         ## Grub Parsing
        configured = False
        grub_tmp = open(grub_new, "w")
        with open(grub_file) as grub:
            for line in grub:
                if "kernel" in line and kernel_version in line:
                    if "blacklist" in line:
                        kernel_parameters = line.split()
                        blacklist = filter(lambda x: x.startswith("blacklist="), kernel_parameters)
                        blacklist_args = []
                        for blck in blacklist:
                            blck_args = blck.split("=")[1]
                            if ',' in blck_args:
                                blck_args = blck_args.split(",")
                                for bl_args in blck_args:
                                    blacklist_args.append(bl_args)
                            else:
                                blacklist_args.append(blck_args)

                        # The current os driver is blacklisted, multiple choices
                        if self.os_driver in blacklist_args:
                            status = "using-%s" % self.driver_name

                            # Already configured, but user want to use nouveau,fglrx
                            if arg == "os":
                                new_kernel_param = filter(lambda x: not x.startswith("blacklist="), \
                                                          kernel_parameters)
                                for bl_args in blacklist_args:
                                    if bl_args != self.os_driver:
                                        new_kernel_param.append("blacklist=%s" % bl_args)

                                new_kernel_param.append("\n")
                                new_kernel_line = " ".join(new_kernel_param)
                                grub_tmp.write(new_kernel_line)
                                configured = True
                                status = "using-%s" % self.os_driver.strip("blacklist=")

                            # Already configured, user want to use vendor drivers,no need to change
                            elif arg =="vendor":
                                configured = False
                                status = "using-%s" % self.driver_name

                        # No os driver is blacklisted, the user want to use vendor driver
                        elif arg == "vendor" and self.os_driver:
                            kernel_parameters.append("blacklist=%s \n" % self.os_driver)
                            new_kernel_line = " ".join(kernel_parameters)
                            grub_tmp.write(new_kernel_line)
                            configured = True
                            status = "using-%s" % self.driver_name

                        # The user wants to use os driver, no need to change
                        else:
                            if self.os_driver:
                                status = "using-%s" % self.os_driver.strip("blacklist=")
                            else:
                                # Neither Ati nor Nvidia drivers are used. (ex: intel)
                                status = "using-non-vendor"

                    elif (arg == "vendor" or arg == "auto") and self.os_driver:
                        kernel_parameters = line.split()
                        kernel_parameters.append("blacklist=%s \n" % self.os_driver)
                        new_kernel_line = " ".join(kernel_parameters)
                        grub_tmp.write(new_kernel_line)
                        configured = True
                        status = "using-%s" % self.driver_name

                    else:
                        status = "using-%s" % self.os_driver
                        if self.os_driver:
                            status = "using-%s" % self.os_driver.strip("blacklist=")
                        else:
                            status = "using-non-vendor"
                            # Neither Ati nor Nvidia drivers are used. (ex: intel)
                else:
                    grub_tmp.write(line)
        grub_tmp.close()

        #Replace the new grub file with the old one, create also a backup file
        if configured:
            # Backup of grub file is created: /boot/grub/grub.conf.back
            shutil.copy2(grub_file, grub_back)

            # New grub file is created: /boot/grub/grub.conf
            shutil.copy2(grub_new, grub_file)

        return status

if __name__ == '__main__':
    p = Panda()
    #print
    #print "Packages needed to enable vendor driver:"
    #print p.get_needed_driver_packages()
    #print
    #print "Packages that could be removed. These are not needed:"
    #print p.get_all_driver_packages()
    #print

    status = p.update_grub_entries("os")
    print
    print status

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
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
    def __init__ (self, default_args=None):
        self.driver_name = None
        self.kernel_flavors = None
        self.os_driver = None
        self.driver_packages = {"fglrx": ["module-fglrx",
                                     "module-pae-fglrx",
                                     "module-fglrx-userspace",
                                     "xorg-video-fglrx"],
                           "nvidia-current": ["module-nvidia-current",
                                              "module-pae-nvidia-current",
                                              "module-nvidia-current-userspace",
                                              "xorg-video-nvidia-current",
                                              "nvidia-xconfig",
                                              "nvidia-settings"] ,
                           "nvidia96": ["module-nvidia96",
                                        "module-pae-nvidia96",
                                        "module-nvidia96-userspace",
                                        "xorg-video-nvidia96",
                                        "nvidia-xconfig",
                                        "nvidia-settings"],
                           "nvidia173": ["module-nvidia173",
                                         "module-pae-nvidia173",
                                         "module-nvidia173-userspace",
                                         "xorg-video-nvidia173",
                                         "nvidia-xconfig",
                                         "nvidia-settings"]}

    def __get_primary_driver(self):
        '''Get driver name for the working primary device'''

        self.driver_name = "Not defined"

        for boot_vga in glob.glob("%s/*/boot_vga" % sysdir):
            if open(boot_vga).read().startswith("1"):
                dev_path = os.path.dirname(boot_vga)
                vendor = open(os.path.join(dev_path, "vendor")).read().strip()
                device = open(os.path.join(dev_path, "device")).read().strip()
                device_id = vendor[2:] + device[2:]

                try:
                    db_file = open(driversDB)
                except IOError:
                    break

                # We've found a Nvidia card, thus set it to nvidia-current
                # That's a workaround for new Nvidia cards that are not written in driversDB
                if vendor[2:] == "10de":
                    self.driver_name = "nvidia-current"

                for line in db_file:
                    if line.startswith(device_id):
                        self.driver_name = line.split()[1]
                        break

                # We've set a card, no need to search for another one
                break 

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

    def get_blacklisted_module(self):
        if self.driver_name is None:
            self.__get_primary_driver()

        if self.driver_name == "fglrx":
            self.os_driver = "radeon"
            return self.os_driver
        elif self.driver_name in ["nvidia-current", "nvidia96", "nvidia173"]:
            self.os_driver = "nouveau"
            return self.os_driver
        else:
            return


    def get_needed_driver_packages(self, kernel_flavors=None, installable=False):
        '''Filter modules that should be addded'''
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

            if installable:
                import pisi
                idb = pisi.db.installdb.InstallDB()
                need_to_install = [x for x in need_to_install if not idb.has_package(x)]

            return need_to_install
        else:
            return []

    def get_all_driver_packages(self):
        '''Extract lists from the driver dict and return one unique single list'''
        drivers = sum([x for x in self.driver_packages.values()], [])

        return list(set(drivers))

    def update_grub_entries(self, arg="status"):
        '''Edit grub file to enable the use of propretiary graphic card drivers'''
        if self.os_driver is None:
            self.get_blacklisted_module()

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

        def keyword_in_line(line, keyword="blacklist"):
            params = line.split()
            blacklist = []

            for param in params:
                if param.startswith("%s=" % keyword):
                    modules = param.split("=", 1)[1].split(",")
                    blacklist.extend(modules)

            return blacklist

        def update_keyword_in_line(line, keyword_param=None, keyword="blacklist"):
            params = [x for x in line.strip().split() if not x.startswith("%s" % keyword)]

            if keyword_param is "ADDNOMODESET":
                params.append(keyword)
            elif keyword_param:
                params.append("%s=%s" % (keyword, ",".join(keyword_param)))

            return " ".join(params) + "\n"

        if arg == "status":
            import StringIO
            grub_tmp = StringIO.StringIO()
        else:
            grub_tmp = open(grub_new, "w")

        with open(grub_file) as grub:
            for line in grub:
                if "kernel" in line and kernel_version in line:
                    blacklist = keyword_in_line(line)
                    xorg_param = keyword_in_line(line, "xorg")

                    if arg == "status":
                        if self.os_driver in blacklist:
                            return "vendor"
                            #return self.driver_name
                        elif self.os_driver:
                            return "os"
                            #return self.os_driver
                        else:
                            return "nonvendor"

                    elif arg == "os":
                        blacklist = [x for x in blacklist if x != self.os_driver]
                        if xorg_param:
                            xorg_param = []
                        nomodeset_param = []
                        status = "os"

                    elif arg == "vendor":
                        if self.os_driver not in blacklist:
                            blacklist.append(self.os_driver)
                        if xorg_param:
                            xorg_param = []
                        nomodeset_param = []
                        status = "vendor"

                    elif arg == "generic":
                        if not xorg_param:
                            xorg_param.append("safe")
                        nomodeset_param = "ADDNOMODESET"
                        status = "generic"

                    line = update_keyword_in_line(line, xorg_param, "xorg")
                    line = update_keyword_in_line(line, nomodeset_param, "nomodeset")
                    new_line = update_keyword_in_line(line, blacklist)
                    print new_line
                    grub_tmp.write(new_line)
                    configured = True

                else:
                    grub_tmp.write(line)

        grub_tmp.close()

        # Replace the new grub file with the old one, create also a backup file
        if configured:
            # Backup of grub file is created: /boot/grub/grub.conf.back
            shutil.copy2(grub_file, grub_back)

            # New grub file is created: /boot/grub/grub.conf
            shutil.copy2(grub_new, grub_file)

        return status

if __name__ == '__main__':
    p = Panda()
    print p.get_all_driver_packages()
    print p.get_blacklisted_modules()
    print p.update_grub_entries("status")
    print p.get_needed_driver_packages(installable=False)


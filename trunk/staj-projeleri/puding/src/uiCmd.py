#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3 (Read COPYING file.)
#

import os
import glob
import sys
import shutil
import subprocess

from common import _
from common import runCommand
from common import createConfigFile
from common import createSyslinux
from common import createUSBDirs
from common import getIsoSize
from common import getMounted
from common import PartitionUtils

from constants import HOME
from constants import MOUNT_ISO
from constants import MOUNT_USB
from constants import NAME
from constants import SHARE

from releases import releases

class ProgressBar:
    def __init__(self, src):
        self.wheel = ("\\", "|", "/", "-")
        self.tour = 52 - 2
        iso_size = getIsoSize(src)
        self.bytes = iso_size / 50

    def fWheel(self, wheel, digit):
        return wheel[digit%4]

    def fSpaces(self, tour, digit):
        return "[" + digit * "=" + (tour - digit) * " " + "]"

    def fProgressbar(self, wheel, tour, digit):
        sys.stdout.write("\r%s\t%s " % (self.fSpaces(tour, digit),
                         self.fWheel(wheel, digit)))
        sys.stdout.flush()

    # FIX ME: This function should be src/common.py
    def verifyIsoChecksum(self, src):
        import hashlib

        checksum = hashlib.md5()
        isofile = file(src, "rb")
        bytes = self.bytes
        total = 0

        while bytes:
            data = isofile.read(bytes)
            checksum.update(data)
            bytes = len(data)
            total += bytes
            digit  = total / self.bytes
            self.fProgressbar(self.wheel, self.tour, digit)

        print("\b\b%s." % _("Finished"))

        src_md5 = checksum.hexdigest()

        for release in releases:
            if src_md5 in release['md5']:
                return release['name'], release['md5'], release['url']

        return False

class Utils:
    def colorize(self, output, color):
        colors = {"red"                : "\033[31m",
                  "green"              : "\033[32m",
                  "yellow"             : "\033[33m",
                  "blue"               : "\033[34m",
                  "purple"             : "\033[35m",
                  "cyan"               : "\033[36m",
                  "white"              : "\033[37m",
                  "brightred"          : "\033[01;31m",
                  "brightgreen"        : "\033[01;32m",
                  "brightyellow"       : "\033[01;33m",
                  "brightblue"         : "\033[01;34m",
                  "brightcyan"         : "\033[01;36m",
                  "brightwhite"        : "\033[01;37m",
                  "default"            : "\033[0m"  }

        return colors[color] + output + colors["default"]

    def cprint(self, output, color = None, no_wrap = False):
        if no_wrap and color == None:
            print(output),

        elif no_wrap and not color == None:
            print(self.colorize(output, color)),

        elif not no_wrap and color == None:
            print(output)

        else:
            print(self.colorize(output, color))

class Create:
    def __init__(self, src, dst):
        self.utils = Utils()
        self.progressbar = ProgressBar(src)

        if dst == None:
            self.partutils = PartitionUtils()

            if not self.partutils.detectRemovableDrives():
                self.utils.cprint(_("USB device not found."), "red")
                sys.exit()

            else:
                device, dst = self.__askDestination()

                # FIX ME: You should not use it.
                if not dst:
                    cmd = "mount -t vfat %s %s" % (device, MOUNT_USB)
                    runCommand(cmd)
                    dst = MOUNT_USB

        if self.__checkSource(src) and self.__checkDestination(dst):
            createUSBDirs(dst)
            self.__createImage(src, dst)

        else:
            sys.exit(1)

    def __checkSource(self, src):
        if not os.path.isfile(src):
            self.utils.cprint(_("The path is invalid, please specify an image path."), "red")

            return False

        self.utils.cprint(_("Calculating checksum..."))

        try:
            (name, md5, url) = self.progressbar.verifyIsoChecksum(src)

            self.utils.cprint(_("\n   Image path: %s" % src))
            self.utils.cprint(_("         Name: %s" % name))
            self.utils.cprint(_("       Md5sum: %s" % md5))
            self.utils.cprint(_(" Download URL: %s\n" % url))

            return True

        # FIX ME: Bad Code..
        except TypeError:
            self.utils.cprint(_("The checksum of the source cannot be validated. Please specify a correct source or be sure that you have downloaded the source correctly."), "red")

            return False

    def __askDestination(self):
        self.drives = self.partutils.returnDrives()
        if len(self.drives) == 1:
            # FIX ME: If disk is unmounted, you should mount it before return process!
            # It returns mount point directory.
            device = self.drives.keys()[0]

        else:
            drive_no = 0

            self.utils.cprint(_("Devices:"), "brightcyan")

            for drive in self.drives:
                drive_no += 1

                # FIX ME: Bad coding..
                self.utils.cprint("\n%d) %s:" % (drive_no, drive), "brightcyan")
                self.utils.cprint(_("    Label\t\t:"), "green", True)
                self.utils.cprint(self.drives[drive]["label"], "yellow")

                self.utils.cprint(_("    Parent\t\t:"), "green", True)
                self.utils.cprint(str(self.drives[drive]["parent"]), "yellow")

                self.utils.cprint(_("    Mount Point\t\t:"), "green", True)
                mount_dir = self.drives[drive]["mount"]
                if not mount_dir:
                    self.utils.cprint("%s (%s)" % (MOUNT_ISO,  _("not mounted")), "yellow")
                else:
                    self.utils.cprint(mount_dir, "yellow")

                self.utils.cprint(_("    Unmount\t\t:"), "green", True)
                self.utils.cprint(str(self.drives[drive]["unmount"]), "yellow")

                self.utils.cprint(_("    UUID\t\t:"), "green", True)
                self.utils.cprint(self.drives[drive]["uuid"], "yellow")

                self.utils.cprint(_("    File System Version\t:"), "green", True)
                self.utils.cprint(self.drives[drive]["fsversion"], "yellow")

                self.utils.cprint(_("    File System Type\t:"), "green", True)
                self.utils.cprint(self.drives[drive]["fstype"], "yellow")

            try:
                id = int(raw_input("%s " % _("USB devices or partitions have found more than one. Please choose one:")))

                device = self.drives.keys()[id - 1]

            except ValueError:
               self.cprint(_("You must enter a number between 0 - %d." % drive_no + 1), "red")

               return False

        destination = self.drives[device]["mount"]

        return device, destination

    def __checkDestination(self, dst):
        if os.path.isdir(dst) and os.path.ismount(dst):
            self.__printDiskInfo(dst)
            self.utils.cprint(_("Please double check your path information. If you don't type the path to the USB stick correctly, you may damage your computer. Would you like to continue?"))

            answer = raw_input("%s " % _("Please type CONFIRM to continue:"))

            if answer in (_('CONFIRM'), _('confirm')):
                self.utils.cprint(_("Writing image data to USB stick!"), "green")

                return True

            else:
                self.utils.cprint(_("You did not type CONFIRM. Exiting.."), "red")

                return False

        else:
            self.utils.cprint(_("The path you have typed is invalid. If you think the path is valid, make sure you have mounted USB stick to the path you gave. To check the path, you can use: mount | grep %s" % dst), "red")

            return False

    def __printDiskInfo(self, dst):
        from common import getDiskInfo

        (capacity, available, used) = getDiskInfo(str(dst))

        print(_("USB disk informations:"))
        print("%s: %dMB" % (_("\tCapacity\t"), capacity))
        print("%s: %dMB" % (_("\tAvailable\t"), available))
        print("%s: %dMB" % (_("\tUsed\t\t"), used))

    def __createImage(self, src, dst):
        self.utils.cprint(_("Mounting image..."), "green")
        cmd = "fuseiso %s %s" % (src, MOUNT_ISO)
        if runCommand(cmd):
            self.utils.cprint(_("Could not mounted image."), "red")

            return False

        self.utils.cprint(_("Creating boot manager..."), "yellow")
        if createSyslinux(dst):
            self.utils.cprint(_("Could not create boot manager."), "red")

            return False

        self.__copyImage(MOUNT_ISO, dst)

        self.utils.cprint(_("Unmounting image..."), "green")
        cmd = "fusermount -u %s" % MOUNT_ISO

        if runCommand(cmd):
            self.utils.cprint(_("Could not unmounted image."), "red")

            return False

        if dst == MOUNT_USB:
            self.utils.cprint(_("Unmounting USB disk..."), "green")
            cmd = "umount %s" % MOUNT_USB

            if runCommand(cmd):
                self.utils.cprint(_("Could not unmounted USB disk."), "red")

                return False

        self.utils.cprint(_("USB disk is ready. Now you can install or run Pardus from your USB disk."), "brightgreen")

        return True

    def __copyImage(self, src, dst):
        # FIX ME: Now, Puding supports only Pardus..
        from puding.pardusTools import Main

        tools = Main(src, dst)
        file_list = tools.file_list

        for path in file_list:
            file_name = os.path.split(path)[-1]
            self.utils.cprint("%s:" % _("Copying"), "green", True)
            self.utils.cprint(file_name, "brightyellow")
            tools.copyFile(path)

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3 (Read COPYING file.)
#

import os
import sys
import tempfile

from puding import _
from puding.common import run_command
from puding.common import create_syslinux
from puding.common import create_USB_dirs
from puding.common import get_disk_info
from puding.common import get_iso_size
from puding.common import unmount_dirs
from puding.common import PartitionUtils
from puding.releases import releases


class ProgressBar:
    def __init__(self, src):
        self.wheel = ("\\", "|", "/", "-")
        self.tour = 52 - 2
        iso_size = get_iso_size(src)
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
    def verify_iso_checksum(self, src):
        import hashlib

        checksum = hashlib.md5()
        isofile = file(src, "rb")
        size = self.bytes
        total = 0

        while size:
            data = isofile.read(size)
            checksum.update(data)
            size = len(data)
            total += size
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
        self.iso_dir = tempfile.mkdtemp(suffix="_isoPuding")

        if not dst:
            self.partutils = PartitionUtils()

            if not self.partutils.detect_removable_drives():
                self.utils.cprint(_("USB device not found."), "red")
                sys.exit()

            else:
                device, dst = self.__ask_destination()

                # FIX ME: You should not use it.
                if not dst:
                    dst = tempfile.mkdtemp(suffix="_usbPuding")
                    cmd = "mount -t vfat %s %s" % (device, dst)
                    self.utils.cprint(_("Mounting USB device..."), "green")
                    run_command(cmd)

        self.utils.cprint(_("Mounting image..."), "green")
        cmd = "fuseiso %s %s" % (src, self.iso_dir)
        if run_command(cmd):
            self.utils.cprint(_("Could not mounted image."), "red")

            sys.exit(1)

        if self.__check_source(src) and self.__check_destination(dst):
            from pardusTools import Main

            tools = Main(self.iso_dir, dst)
            if self.__check_disk_info(dst, tools.get_total_size()):
                self.__create_image(src, dst)

        else:
            self.utils.cprint(_("The path you have typed as second argument is invalid. Please check the USB directory."), "red")
            unmount_dirs()

            sys.exit(1)

    def __ask_destination(self):
        self.drives = self.partutils.return_drives()
        if len(self.drives) == 1:
            # FIX ME: If disk is unmounted, you should mount it before return process!
            # It returns mount point directory.
            device = self.drives.keys()[0]

        else:
            drive_no = 0

            self.utils.cprint(_("Devices:"), "brightwhite")

            for drive in self.drives:
                drive_no += 1

                # FIX ME: Bad coding..
                self.utils.cprint("%d) %s:" % (drive_no, drive), "brightgreen")
                self.utils.cprint("    %s:" % _("Label"), "green", True)
                print(self.drives[drive]["label"])

                self.utils.cprint("    %s:" % _("Parent"), "green", True)
                print(str(self.drives[drive]["parent"]))

                self.utils.cprint("    %s:" % _("Mount Point"), "green", True)
                mount_dir = self.drives[drive]["mount"]
                if not mount_dir:
                    print("%s (%s)" % (self.iso_dir,  _("not mounted")))
                else:
                    print(mount_dir)

                self.utils.cprint("    %s:" % _("Unmount"), "green", True)
                print(str(self.drives[drive]["unmount"]))

                self.utils.cprint("    UUID:", "green", True)
                print(self.drives[drive]["uuid"])

                self.utils.cprint("    %s:" % _("File System Version"), "green", True)
                print(self.drives[drive]["fsversion"])

                self.utils.cprint("    %s:" % _("File System Type"), "green", True)
                print("%s\n" % self.drives[drive]["fstype"])

            try:
                part_number = int(raw_input(_("USB devices or partitions have found more than one. Please choose one:") + " "))

            except ValueError:
                self.utils.cprint(_("Please enter a number between 0 - %d." % (drive_no + 1)), "red")

                sys.exit(1)

            try:
                device = self.drives.keys()[part_number - 1]

            except IndexError:
                self.utils.cprint(_("You must enter a number between 0 - %d." % (drive_no + 1)), "red")

                sys.exit(1)

        destination = self.drives[device]["mount"]

        return device, destination

    def __check_destination(self, dst):
        if os.path.isdir(dst) and os.path.ismount(dst):
            return True

        return False

    def __check_disk_info(self, dst, total_size):
        (capacity, available, used) = get_disk_info(str(dst))
        if available < total_size:
            self.utils.cprint(_("There is not enough space left on your USB stick for the image."), "red")

            self.utils.cprint(_("Unmounting directories..."), "red")
            unmount_dirs()

            return False

        self.utils.cprint(_("USB disk informations:"), "brightgreen")
        self.utils.cprint("    %s:" % _("Capacity"), "green", True)
        print("%dMB" % capacity)

        self.utils.cprint("    %s:" % _("Available"), "green", True)
        print("%dMB" % available)

        self.utils.cprint("    %s:" % _("Used"), "green", True)
        print("%dMB" % used)

        print(_("\nPlease double check your path information. If you don't type the path to the USB stick correctly, you may damage your computer. Would you like to continue?"))

        answer = raw_input("%s " % _("Please type CONFIRM to continue:"))
        if answer in (_('CONFIRM'), _('confirm')):
            self.utils.cprint(_("Writing image data to USB stick!"), "green")

            return True

        self.utils.cprint(_("You did not type CONFIRM. Exiting.."), "red")
        unmount_dirs()

        return False

    def __check_source(self, src):
        if not os.path.isfile(src):
            self.utils.cprint(_("The path is invalid, please specify an image path."), "red")

            return False

        self.utils.cprint(_("Calculating checksum..."), "green")

        try:
            (name, md5, url) = self.progressbar.verify_iso_checksum(src)

            self.utils.cprint(_("Source Informations:"), "brightgreen")
            self.utils.cprint("    %s:" % _("Image Path"), "green", True)
            print(src)
            self.utils.cprint("    %s:" % _("Name"), "green", True)
            print(name)
            self.utils.cprint("    Md5sum:", "green", True)
            print(md5)
            self.utils.cprint("    %s:" % _("Download URL"), "green", True)
            print(url)

            return True

        # FIX ME: Bad Code..
        except TypeError:
            self.utils.cprint(_("The checksum of the source cannot be validated. Please specify a correct source or be sure that you have downloaded the source correctly."), "red")

            return False

    def __create_image(self, src, dst):
        create_USB_dirs(dst)

        self.utils.cprint(_("Creating boot manager..."), "yellow")
        if create_syslinux(self.iso_dir, dst):
            self.utils.cprint(_("Could not create boot manager."), "red")

            return False

        self.__copy_image(self.iso_dir, dst)

        self.utils.cprint(_("Unmounting image and USB disk..."), "green")
        unmount_dirs()

        self.utils.cprint(_("USB disk is ready. Now you can install or run Pardus from your USB disk."), "brightgreen")

        return True

    def __copy_image(self, src, dst):
        # FIX ME: Now, Puding supports only Pardus..
        from pardusTools import Main

        tools = Main(src, dst)
        file_list = tools.file_list

        for path in file_list:
            file_name = os.path.split(path)[-1]
            self.utils.cprint("%s:" % _("Copying"), "green", True)
            self.utils.cprint(file_name, "brightyellow")
            tools.copy_file(path)

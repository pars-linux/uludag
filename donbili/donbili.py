#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
import os
import sys
import time
import hashlib
import tempfile

###
# Main Hardware class
###

class Hardware(object):
    def __init__(self):

        # Sections
        self.sections = ["Basic Informations", \
                         "CPU Informations", \
                         "PCI Devices", \
                         "USB Devices", \
                         "Driver Informations", \
                         "Sound Devices", \
                         "Video Devices", \
                         "Printer Configuration", \
                         "Printer Queues", \
                         "X11 Server Informations", \
                         "Video Devices", \
                         "Scanner Devices", \
                         "Disk Usage", \
                         "Memory Usage", \
                         "COMAR Log", \
                         "Kernel Log", \
                         "KDE4 Informations", \
                         "YALI Installation Log"]

        # Mapping for final report generation
        self.layout = dict(zip(self.sections, map(lambda x: "_get_%s" % x.lower().replace(" ", "_"), self.sections)))

        # Set today's date
        self.today = time.strftime("%F")


    # Private methods

    def __output_file(self, tmpfile):
        """Generate a unique output file name."""
        return "%s-%s-%s" % ("donbili", time.strftime("%Y%m%d"), \
                             hashlib.sha1(open(tmpfile, "r").read()).hexdigest()[:10])

    def __gather_output(self, cmd, params=[], excludes=[], includes=[], date=False, indent=False):
        """Capture the output of cmd and return it as a string."""

        def matches(text, date, i_patterns, e_patterns):
            result = True
            if date and not text.startswith(self.today):
                return False

            for p in i_patterns:
                if p in text:
                    break
                result = False

            for p in e_patterns:
                if p in text:
                    result = False
                    break

            return result

        output = ind = ""

        if os.path.exists(cmd) and not os.access(cmd, os.X_OK):
            # Assume that we're trying to read the contents of cmd, not to execute it
            output = open(cmd, "r").read().strip().split("\n")
        else:
            # Run it and get the output
            output = os.popen("%s %s" % (cmd, " ".join(params))).read().rstrip().split("\n")

        if indent:
            ind = "  "

        return "\n".join(["%s%s" % (ind,l) for l in output if matches(l, date, includes, excludes)])


    def __format_msg(self, msg, sep, up=False):
        """Return the msg + len(msg)*'-' for pretty printing."""
        m = "%s\n%s\n" % (msg, (sep*len(msg)))
        if up:
            m = "%s\n%s\n" % (sep*len(msg), m)

        return m

    def __format_section(self, d):
        section = ""
        if d:
            if isinstance(d, str) or isinstance(d, unicode):
                # Directly dump it
                section += "%s\n" % d
            elif isinstance(d, dict):
                max_section_name = max([len(k) for k in d.keys()])
                for k in [_k[0] for _k in sorted(d.items(), key=lambda x: x[1], cmp=lambda x,y: len(str(x))-len(str(y)))]:
                    if not d[k]:
                        section += "%s\n" % k
                    elif isinstance(d[k], str):
                        section += "%s%s : %s\n" % (k, ((max_section_name-len(k))*' '), d[k])
                    elif isinstance(d[k], list):
                        section += "%s%s\n  %s" % (k, ((max_section_name-len(k))*' '), "\n  ".join(d[k]))
                        section += "\n"
        return section

    # Information collectors for each section

    def _get_basic_informations(self):
        d = {}
        d['Kernel version'] = self.__gather_output("uname", ["-o", "-r", "-s"])

        for dmi_data in ("bios_date",    "bios_vendor",  "bios_version", \
                         "board_vendor", "product_name", "sys_vendor", \
                         "modalias"):
            d[dmi_data.replace("_", " ").capitalize()] = open("/sys/class/dmi/id/%s" % dmi_data, "r").read().strip()

        return d

    def _get_cpu_informations(self):
        d = {}
        cpuinfo = open("/proc/cpuinfo", "r").read()

        # Number of cores
        d['Processor count'] = cpuinfo.count("processor\t:")

        # Reduce to one core
        for line in cpuinfo[:cpuinfo[1:].index('processor\t:')].replace("\t", "").split("\n"):
            prop = line.split(": ")
            if prop[0] in ("processor", "vendor_id", "cpu family", "model", "model name", \
                           "stepping", "cpu MHz", "cache size", "flags", "bogomips", "power management"):
                d[prop[0].capitalize().replace("_", " ")] = prop[1]

        return d

    def _get_driver_informations(self):
        d = {}
        probed_modules = [m.split()[0] for m in self.__gather_output("lsmod", excludes=["snd_", "sound"]).split("\n")[1:]]
        for m in probed_modules:
            # Collect parameter informations about modules
            d[m] = []
            try:
                for param in os.listdir("/sys/module/%s/parameters" % m):
                    try:
                        d[m].append("%s: %s" % (param, open("/sys/module/%s/parameters/%s" % (m, param)).read().strip()))
                    except IOError:
                        # Can't read it, pass
                        pass
            except OSError:
                # No parameters
                pass

        return d

    def _get_sound_devices(self):
        return self.__gather_output("alsa-info", ["--stdout"],
                                    excludes=["upload="],
                                    indent=True)

    def _get_video_devices(self):
        return self.__gather_output("scanimage", ["-L", "-v"])

    def _get_pci_devices(self):
        return self.__gather_output("lspci", ["-nn"])

    def _get_usb_devices(self):
        return self.__gather_output("lsusb")

    def _get_disk_usage(self):
        return self.__gather_output("df", ["-ahPT"])

    def _get_memory_usage(self):
        return self.__gather_output("free", ["-mt"])

    def _get_printer_queues(self):
        import cups
        c = cups.Connection()

        result = ""
        for p, pattr in c.getPrinters().items():
            result += "[%s]\n  " % p

            result += "\n  ".join(["%s: %s" % (k, v) for k,v in pattr.items()])
            result += "\n\n"

        return result

    def _get_printer_configuration(self):
        return self.__gather_output("/var/log/syslog",
                                    includes=["hal_lpadmin", "udev-configure-printer"])

    def _get_kernel_log(self):
        # Filter out ALSA too big adjustment messages
        return self.__gather_output("dmesg", excludes=["Too big adjustment"])

    def _get_comar_log(self):
        return self.__gather_output("/var/log/comar3/trace.log",
                                    excludes=["Missing - Method"],
                                    date=True)


    # Public methods

    def dump(self):
        """Generate the final hardware report."""

        report = ""

        # Header
        report += self.__format_msg("Hardware report generated on %s by donbili" % time.asctime(), '*', True)

        # Sections
        for section in self.sections:
            try:
                info = getattr(globals()['hwdata'], self.layout[section])
            except Exception, e:
                continue
            else:
                report += "%s\n%s\n" % (self.__format_msg(section, '-'), self.__format_section(info()))

        return report


###
# donbili starts here
###

if __name__ == "__main__":

    # Set locale to C for a better world
    os.environ["LC_ALL"] = "C"

    # Create an instance of Hardware
    hwdata = Hardware()

    # Dump the informations
    print hwdata.dump()

    sys.exit(0)

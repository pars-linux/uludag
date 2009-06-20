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
                         "Sound Devices", \
                         "Printing Informations", \
                         "X11 Server Informations", \
                         "Video Devices", \
                         "Scanner Devices", \
                         "Disk Usage", \
                         "Memory Usage", \
                         "KDE4 Informations", \
                         "YALI Installation Log"]

        # Mapping for final report generation
        self.layout = dict(zip(self.sections, map(lambda x: "_get_%s" % x.lower().replace(" ", "_"), self.sections)))


    # Private methods

    def __output_file(self, tmpfile):
        """Generate a unique output file name."""
        return "%s-%s-%s" % ("donbili", time.strftime("%Y%m%d"), \
                             hashlib.sha1(open(tmpfile, "r").read()).hexdigest()[:10])

    def __gather_output(self, cmd, params=[]):
        """Capture the output of cmd and return it as a string."""
        return os.popen("%s %s" % (cmd, " ".join(params))).read().strip()


    def __format_msg(self, msg, sep, up=False):
        """Return the msg + len(msg)*'-' for pretty printing."""
        m = "%s\n%s\n\n" % (msg, (sep*len(msg)))
        if up:
            m = "%s\n%s" % (sep*len(msg), m)

        return m

    def __format_section(self, d):
        section = ""
        if d:
            max_section_name = max([len(k) for k in d.keys()])
            for k in d.keys():#sorted(d.keys(), cmp=lambda x,y: len(y)-len(x)):
                section += "%s%s : %s\n" % (k, ((max_section_name-len(k))*' '), d[k])
        return section

    # Information collectors for each section

    def _get_basic_informations(self):
        d = {}
        d['Kernel version'] = self.__gather_output("uname", ["-o", "-r", "-s"])

        for dmi_data in ("bios_date",    "bios_vendor",  "bios_version", \
                         "board_vendor", "product_name", "sys_vendor"):
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


    # Public methods

    def dump(self):
        """Generate the final hardware report."""

        report = ""

        # Header
        report += self.__format_msg("Hardware report generated on %s by donbili" % time.asctime(), '*', True)

        # Sections
        for section in sorted(self.sections):
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

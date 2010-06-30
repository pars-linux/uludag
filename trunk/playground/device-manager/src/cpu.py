#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Ozan Çağlayan <ozan@pardus.org.tr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import os
import glob

class CPU(object):
    """Class implementing system CPU."""
    def __init__(self):
        self.__parse_cpuinfo()

    def __parse_cpuinfo(self):
        """Parse /proc/cpuinfo and provide the necessary informations."""
        f = open("/proc/cpuinfo", "r")
        cpuinfo = f.read().strip()
        f.close()

        # processor occurences give the number of cores
        self.nr_cores = cpuinfo.count("processor\t:")

        # Trim the list to ignore the cores other than the first one
        cpuinfo = cpuinfo.replace("\t", "").split("\n")
        cpuinfo = cpuinfo[:cpuinfo.index("")]

        # Update instance members with cpuinfo
        self.__dict__.update(dict([(line.split(":")[0].replace(" ", "_"), line.split(":")[-1].strip()) \
                for line in cpuinfo]))

        # Split the flags for convenience
        # Definition for each flag can be found in "arch/x86/include/asm/cpufeature.h"
        self.flags = self.flags.split()

    def has_flag(self, flag):
        """Returns true if the given flag is supported by the CPU."""
        return flag in self.flags

    def supports_pae(self):
        """Returns true if the processor supports PAE (Physical Address Extension)."""
        return "pae" in self.flags

    def supports_vt(self):
        """Returns true if the processor supports Hardware Virtualization."""
        return "vmx" in self.flags or "svm" in self.flags

    def supports_x86_64(self):
        """Returns true if the processor supports long-mode (x86_64)."""
        return "lm" in self.flags

    def supports_microcode(self):
        """Returns true if processor supports microcode driver."""
        #FIXME: Look at mandriva's initscript
        return os.path.exists("/dev/cpu/microcode")

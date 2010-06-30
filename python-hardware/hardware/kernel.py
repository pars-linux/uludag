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
#
# kernel.py: Kernel and Module classes to represent the running kernel
#            and the loaded modules and their parameters


import os
import glob

class Module(object):
    """Class which implements a kernel module."""
    def __init__(self, name):
        self.name = name
        self.parameters = {}

        self.__parse_parameters()

    def __parse_parameters(self):
        """Store the module parameters in a dictionary."""
        for param in glob.glob(os.path.join("/sys/module",
                                            self.name, "parameters/*")):
            self.parameters[os.path.basename(param)] = \
                    open(param, "r").read().strip()


class Kernel(object):
    """Class which implements a kernel."""
    def __init__(self):
        self.kver = os.uname()[2]
        self.karch = os.uname()[-1]

        # Parse kernel cmdline
        self.cmdline = open("/proc/cmdline", "r").read().strip()

        self.modules = {}

        self.detect_modules()

    def __str__(self):
        return "Kernel architecture: %s\nKernel version: %s" % (self.kver,
                                                                self.karch)

    def detect_modules(self):
        """Parses /proc/modules to detect loaded modules."""
        with open("/proc/modules", "r") as _file:
            for module in [m.split()[0] for m in _file.readlines()]:
                self.modules[module] = Module(module)

    def is_module_loaded(self, name):
        """Returns true if the given module is loaded."""
        return os.path.exists(os.path.join("/sys/module", name))

    def get_total_memory(self):
        """Returns the amount of RAM installed in the maching in MB."""
        mem = 0.0
        with open("/proc/meminfo", "r") as _file:
            for line in _file.readlines():
                if line.startswith("MemTotal:"):
                    mem = int((int(line.split()[1])/1024.0))
                    break
        return mem

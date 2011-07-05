#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# puding
# Copyright (C) Gökmen Görgen 2009 <gkmngrgn@gmail.com>
#
# puding is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# puding is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import getopt
import os
import sys
from optparse import OptionParser
from optparse import OptionGroup

try:
    from puding import _
except ImportError: 
    module_dir = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    sys.path.append(module_dir)

    from puding import _

from puding.common import run_command
from puding.common import unmount_dirs
from puding.constants import LICENSE
from puding.constants import VERSION


class Options:
    def parse_args(self, parser):
        parser.add_option("-l", "--license", dest = "license", action = "store_true", help = _("show program's license info and exit"))
        parser.add_option("-c", "--create", dest = "create", action = "store_true", help = _("create Pardus USB image from console"))

        return parser.parse_args()

    def main(self):
        description = _("Puding is an USB image creator for Pardus Linux.")
        parser = OptionParser(description = description, version = VERSION)
        (opts, args) = self.parse_args(parser)

        if opts.create:
            if not os.getuid() == 0:
                print(_("You need superuser permissions to run this application."))

                sys.exit(0)

            try:
                from puding.ui.cmd import puding_cmd

                source = os.path.realpath(args[0])

                try:
                    destination = os.path.realpath(args[1])

                except:
                    destination = None

                puding_cmd.Create(source, destination)

            except IndexError:
                print(_("Invalid usage. Example:"))
                print("\tpuding --create /mnt/archive/Pardus-2009.iso\n")
                print(_("(If you know directory path that is your USB device mount point)"))
                print("\tpuding --create /mnt/archive/Pardus-2009.iso /media/disk")

        elif opts.license:
            print(LICENSE)

        else:
            from puding.ui.qt.puding_qt import RunApplicationInterface

            RunApplicationInterface()


if __name__ == "__main__":
    try:
        Options().main()

    except KeyboardInterrupt:
        print(_("\nQuitting, please wait."))
        unmount_dirs()

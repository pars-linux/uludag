#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# puding.py
# Copyright (C) Gökmen Görgen 2009 <gkmngrgn@gmail.com>
# 
# puding.py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# puding.py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import getopt
import os
import sys

from optparse import (OptionParser, OptionGroup)
from puding.common import (_, createDirs)
from puding.constants import (HOME, LICENSE, NAME, USAGE, VERSION)

class Options:
    def parseArgs(self, parser):
        parser.add_option('-l', '--license', dest = 'license', action = 'store_true',
                          help = _("show program's license info and exit"))
        parser.add_option("-c", "--create", dest = "create", action = "store_true",
                          help = _("create Pardus USB image from console"))

        group = OptionGroup(parser, _("Graphical Interface Options"))
        group.add_option("--with-qt", dest = "with_qt", action = "store_true",
                          help = _("run Puding with Qt4 graphical interface"))

        parser.add_option_group(group)

        return parser.parse_args()

    def main(self):
        parser = OptionParser(usage = USAGE, version = VERSION)
        (opts, args) = self.parseArgs(parser)

        if opts.create:
            if not os.getuid() == 0:
                print(_("You need superuser permissions to run this application."))
 
                sys.exit(0)

            try:
                from puding import ui_cmd

                source = os.path.realpath(args[0])

                try:
                    destination = os.path.realpath(args[1])

                except:
                    destination = None

                ui_cmd.Create(source, destination)

            except IndexError:
                print(_("Invalid usage. Example:"))
                print("\t%s --create /mnt/archive/Pardus-2009.iso\n" % NAME)
                print("(If you know directory path that is your USB device mount point)\n\
\t%s --create /mnt/archive/Pardus-2009.iso /media/disk" % NAME)

        elif opts.license:
            print(LICENSE)

        elif opts.with_qt:
            from puding import ui_qt
            from PyQt4 import QtGui

            app = QtGui.QApplication(sys.argv)
            form = ui_qt.Create()
            form.show()
            sys.exit(app.exec_())

        else:
            parser.print_help()

if __name__ == "__main__":
    createDirs()

    try:
        Options().main()

    except KeyboardInterrupt:
        print(_("\nQuit."))
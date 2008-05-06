# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# YALI options module defines a class for command line options.

from optparse import OptionParser

class Options(object):

    def __init__(self):
        parser = OptionParser()
        parser.add_option("-d", "--debug", dest="debug",
                          action="store_true", default="False",
                          help="enable debug")
        parser.add_option("-r", "--dryRun", dest="dryRun",
                          action="store_true", default="False",
                          help="only show the result")
        parser.add_option("-f", "--firstBoot", dest="firstBoot",
                          action="store_true", default="False",
                          help="only show the result")
        parser.add_option("-k", "--kahyaFile", dest="kahyaFile",
                          help="Run with Kahya file", metavar="FILE")
        parser.add_option("-s", "--startFrom", dest="startupScreen",
                          help="Start from the given screen (num)", type="int", default=0)
        self.options, self.args = parser.parse_args()

    def __getattr__(self, name):
        if hasattr(self.options, name):
            return getattr(self.options, name)
        else:
            return None

# Command line options singleton.
options = Options()

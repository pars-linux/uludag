#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys

def main(args):
    prj = None
    for item in args[1:]:
        if not item.startswith("-"):
            prj = item
            args.remove(item)
    import gui
    gui.gui_main(args, prj)

if __name__ == "__main__":
    main(sys.argv)

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

def do_operation(project_file, op):
    import project
    import maker
    
    prj = project.Project()
    err = prj.open(project_file)
    if err:
        raise RuntimeError("%s" % err)
    
    if op == "make":
        maker.make(prj)
    # make-repo
    # make-image
    # install-image
    # configure-image
    elif op == "squash-image":
        maker.squash_image(prj)
    elif op == "make-iso":
        maker.make_iso(prj)
    else:
        raise RuntimeError("Unknown operation '%s'" % op)

def main(args):
    if len(args) == 3:
        do_operation(args[2], args[1])
        return
    prj = None
    for item in args[1:]:
        if not item.startswith("-"):
            prj = item
            args.remove(item)
    import gui
    gui.gui_main(args, prj)

if __name__ == "__main__":
    main(sys.argv)

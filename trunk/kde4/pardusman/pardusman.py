#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# System
import sys
import time


def maker(op, project_file):
    from repotools import maker, project

    prj = project.Project()
    err = prj.open(project_file)
    if err:
        raise RuntimeError("%s" % err)

    start = time.time()

    if op == "make" or op == "make-repo":
        prj.get_repo(update_repo=True)
        maker.make_repos(prj)
    if op == "check-repo":
        maker.check_repo_files(prj)
    if op == "make" or op == "make-live":
        maker.make_image(prj)
    # install-live
    # configure-live
    if op == "make" or op == "make-live" or op == "pack-live":
        maker.squash_image(prj)
    if op == "make" or op == "make-iso":
        maker.make_iso(prj)

    end = time.time()
    print "Total time is", end - start, "seconds."


def usage(app):
    print "Usage: %s [command] path/to/project.xml" % app
    print
    print "Commands:"
    print "  make-repo  : Make local repos"
    print "  check-repo : Check repo files"
    print "  make-live  : Install image & make squashfs"
    print "  pack-live  : Make squashfs"
    print "  make-iso   : Make ISO"
    print "  make       : Make all!"


def main(args):
    if len(args) == 2 and args[1] in ["help", "-h", "--help"]:
        usage(args[0])
    elif len(args) == 3:
        maker(args[1], args[2])
    else:
        import gui
        gui.gui(args)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

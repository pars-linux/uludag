#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import sys
from optparse import OptionParser

import comar
from zorg import versionString

zorg_info = " Xorg AutoConfiguration tool"

class OUT:
    def __init__(self, colorout):
        if colorout:
            self.NORMAL = '\x1b[37;0m'
            self.BOLD = '\x1b[37;01m'
            self.MARK = '\x1b[36;01m'
            self.WARN = '\x1b[35m'
            self.WARNMSG = '\x1b[35;01m'
            self.ERROR = '\x1b[31m'
            self.ERRORMSG = '\x1b[31;01m'
        else:
            self.NORMAL = ''
            self.BOLD = ''
            self.MARK = ''
            self.WARN = ''
            self.WARNMSG = ''
            self.ERROR = ''
            self.ERRORMSG = ''

        self.type_sect = "%s-> " % self.MARK
        self.type_info = "%s   " % self.NORMAL
        self.type_warn = "%sWW " % self.WARN
        self.type_error  = "%sEE " % self.ERROR

    def _write(self, type, msg):
        print "%s %s%s" % (type, msg, self.NORMAL)

    def sect(self, msg):
        if debug:
            self._write(self.type_sect, "%s%s" % (self.BOLD, msg))

    def info(self, msg):
        if debug:
            self._write(self.type_info, msg)

    def warn(self, msg):
        self._write(self.type_warn, "%s%s" % (self.WARNMSG, msg))

    def error(self, msg):
        self._write(self.type_error, "%s%s" % (self.ERRORMSG, msg))
        sys.exit(1)

class ZorgApp:
    def __init__(self, opts):
        self.debug = opts.debug
        self.out = OUT(opts.colorout)
        self.com = comar.Link()

    def safe(self):
        self.com.Xorg.Display.safeConfigure()

    def probe(self):
        self.com.Xorg.Display.autoConfigure()

    def info(self):
        com = self.com
        com.Xorg.Display.listCards()
        reply = com.read()
        if not reply:
            self.out.error("Could not retrieve card list.")
            return

        cards = reply.data
        self.out.sect("Following video cards have been configured:")
        for card in cards.splitlines():
            cardId, name = card.split(" ", 1)
            self.out.info(name)

def main():
    # running from command line
    parser = OptionParser(description = "%s version %s" % (zorg_info, versionString()))
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      default=False, help="print extra debug info")
    parser.add_option("-n", "--no-color", action="store_false", dest="colorout",
                      default=True, help="do not print colorized output")
    parser.add_option("-s", "--safe", action="store_true", dest="safe",
                      default=False, help="setup VESA 800x600 config without probing hardware")
    parser.add_option("-p", "--probe", action="store_true", dest="probe",
                      default=False, help="force probing all devices, even if xorg.conf exists")
    parser.add_option("-i", "--info", action="store_true", dest="info",
                      default=False, help="print video, monitor and input info, no advanced probing is done")
    parser.add_option("--intelfix", action="store_true", dest="intelfix",
                      default=False, help="run Intel BIOS bug workaround")
    parser.add_option("--intellist", action="store_true", dest="intellist",
                      default=False, help="list available BIOS modes for Intel cards")

    opts, args = parser.parse_args()

    app = ZorgApp(opts)

    if opts.safe:
        app.safe()
    elif opts.probe:
        app.probe()
    elif opts.info:
        app.info()
    else:
        app.out.error("Not implemented yet.")

if __name__ == "__main__":
    main()

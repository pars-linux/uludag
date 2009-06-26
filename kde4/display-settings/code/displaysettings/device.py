#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

class Output:
    # Connection status
    Connected = 0
    Disconnected = 1
    Unknown = 2

    # Output type
    UnknownOutput = -1
    LaptopPanel = 0
    AnalogOutput = 1
    DigitalOutput = 2
    TVOutput = 3

    def __init__(self, name):
        self.name = name
        self.connection = self.Disconnected

        outputTypes = (
            (self.LaptopPanel,     ("lvds")),
            (self.AnalogOutput,    ("crt", "vga")),
            (self.DigitalOutput,   ("dfp", "dvi", "hdmi", "tmds")),
            (self.TVOutput,        ("s-video", "composite", "component", "tv")))

        outputLower = name.lower()
        for otype, names in outputTypes:
            if outputLower.startswith(names):
                self.outputType = otype
                break
        else:
            self.outputType = self.UnknownOutput

    def __repr__(self):
        return "<Output %s>" % self.name

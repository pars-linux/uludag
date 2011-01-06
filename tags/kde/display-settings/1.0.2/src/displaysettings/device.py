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

from PyKDE4 import kdecore
from PyKDE4 import kdeui

from pardus.strutils import ascii_lower

class Output(object):
    # Connection status
    Connected, \
    Disconnected, \
    Unknown, \
    = range(3)

    # Output type
    UnknownOutput, \
    DefaultOutput, \
    LaptopPanel, \
    AnalogOutput, \
    DigitalOutput, \
    TVOutput, \
    = range(6)

    def __init__(self, name):
        self.name = name
        self.connection = self.Disconnected

        outputTypes = (
            (self.DefaultOutput,   ("default")),
            (self.LaptopPanel,     ("lvds")),
            (self.AnalogOutput,    ("crt", "vga")),
            (self.DigitalOutput,   ("dfp", "dvi", "hdmi", "tmds")),
            (self.TVOutput,        ("s-video", "composite", "component", "tv")))

        outputLower = ascii_lower(name)
        for otype, names in outputTypes:
            if outputLower.startswith(names):
                self.outputType = otype
                break
        else:
            self.outputType = self.UnknownOutput

    def __repr__(self):
        return "<Output %s>" % self.name

    def getTypeString(self):
        names = {
                Output.UnknownOutput:   "",
                Output.DefaultOutput:   kdecore.i18n("Default Output"),
                Output.LaptopPanel:     kdecore.i18n("Laptop Panel"),
                Output.AnalogOutput:    kdecore.i18n("Analog Output"),
                Output.DigitalOutput:   kdecore.i18n("Digital Output"),
                Output.TVOutput:        kdecore.i18n("TV Output"),
                }
        return names[self.outputType]

    def getIcon(self):
        icons = {
                Output.LaptopPanel:     "computer-laptop",
                Output.TVOutput:        "video-television"
                }
        return kdeui.KIcon(icons.get(self.outputType, "video-display"))

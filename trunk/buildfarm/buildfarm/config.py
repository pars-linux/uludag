#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

import ConfigParser

class Config(object):
    """Configuration class for /etc/buildfarm/buildfarm.conf."""
    def __init__(self, conf_file="/etc/buildfarm/buildfarm.conf"):
        self.__items = dict()

        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read(conf_file)
        self.read()

    def read(self):
        for s in self.configuration.sections():
            self.__items.update(dict(self.configuration.items(s)))

    def __getattr__(self, attr):
        value = self.__items.get(attr, None)
        if value and value in ("True", "False"):
            value = bool(value)
        elif "," in value:
            value = value.split(",")

        return value

# Initialize configuration object
configuration = Config()


if __name__ == "__main__":
    # Test code
    c = Config()
    print c.deltablacklist

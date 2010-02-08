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

from buildfarm.config import configuration as conf
import ConfigParser

class Auth(object):
    def __init__(self):
        self.data = {}
        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read(conf.credentialsfile)
        self.read()

    def read(self):
        for s in self.configuration.sections():
            self.data[s] = [k[1] for k in self.configuration.items(s)]

    def get_credentials(self, section):
        return self.data.get(section, ['', ''])


# Test code
if __name__ == "__main__":
    def test(user, password):
        print "username:%s\npassword:%s" % (user, password)

    a = Auth()
    test(*a.get_credentials('Twitter'))

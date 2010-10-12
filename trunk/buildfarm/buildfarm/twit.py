#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

from buildfarm.auth import Auth
from buildfarm.config import configuration as conf

class Twitter(object):
    def __init__(self):
        self.api = None
        self.prefix = "[%s/%s/%s]" % (conf.release.capitalize(),
                                      conf.subrepository,
                                      conf.architecture)
        self.auth = Auth()
        try:
            import twitter
        except ImportError:
            pass
        else:
            # Read the credentials from a safe place
            self.api = twitter.Api(*self.auth.get_credentials('Twitter'))

    def update(self, msg):
        if self.api:
            return self.api.PostUpdate("%s %s" % (self.prefix, msg))


if __name__ == "__main__":
    t = Twitter()
    t.update("Test")

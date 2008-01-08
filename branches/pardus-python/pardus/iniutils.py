# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

"""initutils module provides ini style configuration file utils."""

import os
import ConfigParser

class iniDB:
    def __init__(self, db_file):
        try:
            print os.path.basename(db_file)
            os.makedirs(os.path.dirname(db_file))
        except OSError:
            pass
        if not os.path.exists(db_file):
            fp = file(db_file, "w")
            fp.write()
            fp.close()
        self.db_file = db_file
        self.cp = ConfigParser.ConfigParser()
        self.cp.read(db_file)

    def listDB(self):
        profiles = self.cp.sections()
        if "general" in profiles:
            profiles.remove("general")
        return profiles

    def getDB(self, name):
        dct = {}
        if name in self.cp.sections():
            dct = dict(self.cp.items(name))
        return dct

    def setDB(self, name, dct):
        for key, value in dct.iteritems():
            if value:
                if name not in self.cp.sections():
                    self.cp.add_section(name)
                self.cp.set(name, key, value)
            elif name in self.cp.sections():
                self.cp.remove_option(name, key)
        fp = open(self.db_file, "w")
        self.cp.write(fp)
        fp.close()

    def remDB(self, name):
        self.cp.remove_section(name)

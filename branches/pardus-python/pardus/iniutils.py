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
    def __init__(self, db_dir):
        self.db_dir = db_dir

    def listDB(self):
        return os.listdir(self.db_dir)

    def getDB(self, name):
        dct = {}
        try:
            os.makedirs(self.db_dir)
        except OSError:
            pass
        db_file = os.path.join(self.db_dir, name)
        if os.path.exists(db_file):
            cp = ConfigParser.ConfigParser()
            cp.read(db_file)
            if "general" in cp.sections():
                dct = dict(cp.items("general"))
        return dct

    def setDB(self, name, dct):
        try:
            os.makedirs(self.db_dir)
        except OSError:
            pass
        db_file = os.path.join(self.db_dir, name)
        cp = ConfigParser.ConfigParser()
        for key, value in dct.iteritems():
            if value:
                if "general" not in cp.sections():
                    cp.add_section("general")
                cp.set("general", key, value)
            elif "general" in cp.sections():
                cp.remove_option("general", key)
        fp = open(db_file, "w")
        cp.write(fp)
        fp.close()

    def remDB(self, name):
        try:
            os.makedirs(self.db_dir)
        except OSError:
            pass
        db_file = os.path.join(self.db_dir, name)
        os.unlink(db_file)

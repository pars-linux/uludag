# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PISI Configuration module is used for gathering and providing
# regular PISI configurations.

# Authors: Baris Metin <baris@uludag.org.tr
#          Eray Ozkural <eray@uludag.org.tr>

from constants import const
from configfile import ConfigurationFile

class Config(object):
    """Config Singleton"""
    
    def __init__(self, options = None):
        self.options = options
        self.values = ConfigurationFile("/etc/pisi/pisi.conf")
        self.destdir = self.values.general.destinationdirectory

    def __call__(self):
        return self

    # directory accessor functions
    # here is how it goes
    # x_dir: system wide directory for storing info type x
    # pkg_x_dir: per package directory for storing info type x

    def lib_dir(self):
        return self.destdir + self.values.dirs.lib_dir

    def db_dir(self):
        return self.destdir + self.values.dirs.db_dir

    def archives_dir(self):
        return self.destdir + self.values.dirs.archives_dir

    def packages_dir(self):
        return self.destdir + self.values.dirs.packages_dir

    def index_dir(self):
        return self.destdir + self.values.dirs.index_dir

    def tmp_dir(self):
        return self.destdir + self.values.dirs.tmp_dir

    # bu dizini neden kullanıyoruz? Yalnızca index.py içerisinde
    # kullanılıyor ama /var/tmp/pisi/install gibi bir dizine niye
    # ihtiyacımız var? (baris)
    def install_dir(self):
        return self.tmp_dir() + const.install_dir_suffix

config = Config()

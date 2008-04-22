# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# YALI constants module defines a class with constant members. An
# object from this class can only bind values one to it's members.

import locale
from os.path import join

class _constant:
    """ Constant members implementation """
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind constant: %s" % name
        # Binding an attribute once to a const is available
        self.__dict__[name] = value

    def __delattr__(self, name):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't unbind constant: %s" % name
        # we don't have an attribute by this name
        raise NameError, name

class Constants:
    """ YALI's Constants """
    __c = _constant()

    def __getattr__(self, attr):
        return getattr(self.__c, attr)

    def __setattr__(self, attr, value):
        setattr(self.__c, attr, value)

    def __delattr__(self, attr):
        delattr(self.__c, attr)

consts = Constants()

consts.pardus_version = file("/etc/pardus-release").readlines()[0].strip()

consts.data_dir = "/usr/share/yali4"

# log file for storing after installation
consts.log_file = "/var/log/yaliFirstBoot.log"

# dbus socket path
consts.dbus_socket_file = "/var/run/dbus/system_bus_socket"

# user faces (for KDM)
consts.user_faces_dir = join(consts.data_dir, "user_faces")

# pardus repository
consts.pardus_repo_name = ""
consts.pardus_repo_uri = ""

#consts.pardus_repo_name = "pardus-2007.3"
#consts.pardus_repo_uri = "http://paketler.pardus.org.tr/pardus-2007.3/pisi-index.xml.bz2"

# min root partition size
consts.min_root_size = 3500

# kahya options
consts.kahyaParam = "kahya"

# firstBoot options
consts.firstBootParam = "oeminstall"
consts.firstBootFile = join(consts.data_dir,"data/firstBoot.xml")

try:
    consts.lang = locale.getdefaultlocale()[0][:2]
except:
    # default lang to en_US
    consts.lang = "en"

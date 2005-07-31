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

# Context module.

# Authors: Baris Metin <baris@uludag.org.tr
#          Eray Ozkural <eray@uludag.org.tr>

from constants import const
from config import Config
from specfile import SpecFile

class BuildContext(object):
    """Build Context Singleton"""

    class ctximpl(Config.configimpl):        # singleton implementation

        def __init(self):
            super(ctximpl, self).__init__()

        def setSpecFile(self, pspecfile):
            self.pspecfile = pspecfile
            spec = SpecFile()
            spec.read(pspecfile)
            spec.verify()    # check pspec integrity
            self.spec = spec

        # directory accessor functions
        
        # pkg_x_dir: per package directory for storing info type x

        def pkg_dir(self):
            "package build directory"
            packageDir = self.spec.source.name + '-' \
                + self.spec.source.version + '-' + self.spec.source.release

            return self.destdir + self.values.dirs.tmp_dir \
                + '/' + packageDir
   
        def pkg_work_dir(self):
            return self.pkg_dir() + const.work_dir_suffix

        def pkg_install_dir(self):
            return self.pkg_dir() + const.install_dir_suffix

    __instance = ctximpl()               # singleton implementation

    def __init__(self, pspecfile):
        self.__instance.setSpecFile(pspecfile)

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

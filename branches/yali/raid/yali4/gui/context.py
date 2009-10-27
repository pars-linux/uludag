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

from os.path import join
from yali4.gui import installdata

# singletons from yali.*
from yali4.constants import consts
from yali4.options import options
from yali4.partitionrequest import partrequests

# lock for format request
requestsCompleted = False

# bind some constant values
# There are more values defined in yali/constants.py!
consts.pics_dir = join(consts.data_dir, "pics")
consts.slidepics_dir = join(consts.data_dir, "slideshow")
consts.helps_dir = join(consts.data_dir, "helps")

debugger = None
debugEnabled = False

# install data
installData = installdata.InstallData()

# icon factory
# iconfactory = yali.gui.iconfactory.IconFactory(consts.pics_dir)

# auto partitioning
use_autopart = False

# auto installation
autoInstall = False

# keydata
keydata = None

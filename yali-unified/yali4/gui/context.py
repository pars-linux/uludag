# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
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
import yali4.sysutils

# Distribution specific artwork/images/styles
# FIXME: This can't be moved to constants.py because it causes
# circular import
consts.stylesheet = join(consts.data_dir, "data", consts.pardus_release, "style.qss")

# FIXME: Handling /proc/cmdline OR yali4-bin --theme is disabled for now
#consts.stylesheet = join(consts.data_dir, "data/%s.qss" % (yali4.sysutils.checkYaliOptions("theme") or options.theme))

# Alternative stylesheet
consts.alternatestylesheet = join(consts.data_dir, "data/oxygen.qss")

# lock for format request
requestsCompleted = False

# debugger variables
debugger = None
debugEnabled = False

# install data
installData = installdata.InstallData()

# edd check
isEddFailed = False

# auto partitioning
use_autopart = False

# auto installation
autoInstall = False

# keydata
keydata = None

# Bus
bus = None

# Selected disk for manual partitioning screen
selectedDisk = None

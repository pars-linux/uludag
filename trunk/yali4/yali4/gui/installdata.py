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

# Auto Partition Methods
methodUseAvail, methodEraseAll, methodManual = range(3)

# Boot Loader Options
B_DONT_INSTALL = 0
B_INSTALL_PART = 1
B_INSTALL_MBR  = 2
B_INSTALL_SMART= 3

class InstallData:
    keyData = None
    rootPassword = None
    hostName = None
    users = []
    autoLoginUser = None
    autoPartDev = None
    autoPartPartition = None
    autoPartMethod = methodUseAvail
    bootLoaderDev = None
    bootLoaderOption = B_DONT_INSTALL
    orderedDiskList = []
    repoAddr = None
    useYaliFirstBoot = False
    timezone = "Europe/Istanbul"


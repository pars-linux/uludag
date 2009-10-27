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
methodUseAvail, methodEraseAll = range(2)

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
    orderedDiskList = []
    repoAddr = None
    useYaliFirstBoot = False
    timezone = "Europe/Istanbul"


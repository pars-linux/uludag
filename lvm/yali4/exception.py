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

class YaliError(Exception):
    pass

class YaliException(Exception):
    pass

class YaliExceptionInfo(Exception):
    pass

class FSError(YaliError):
    pass

class FSCheckError(YaliError):
    pass

class LVMError(YaliError):
    pass

class PhysicalVolume(LVMError):
    pass

class VolumeGroupError(LVMError):
    pass

class LogicalVolume(LVMError):
    pass

class RaidError(YaliError):
    pass
class MDRaidError(RaidError):
    pass
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

class   StorageError(Exception):
    pass

#Device
class DeviceError(StorageError):
    pass

#Device Format
class DeviceFormatError(StorageError):
    pass
class FormatCreateError(DeviceFormatError):
    pass

#Device Libs
class DMError(StorageError):
    pass
class RaidError(StorageError):
    pass
class MDRaidError(StorageError):
    pass
class LVMError(StorageError):
    pass
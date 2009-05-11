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

class   PareError(Exception):
    pass

#Device
class StorageError(PareError):
    pass

class StorageListError(StorageError):
    pass


#Storage Format
class StorageFormatError(StorageError):
    pass
class FormatCreateError(StorageFormatError):
    pass

#Storage Format
class StorageFormatError(StorageError):
    pass

class FileSystemError(StorageFormatError):
    pass

class FileSystemMigrateError(StorageError):
    pass
class FileSystemResizeError(StorageError):
    pass

#Storage Libs
class DMError(StorageError):
    pass
class RaidError(StorageError):
    pass
class MDRaidError(StorageError):
    pass
class LVMError(StorageError):
    pass
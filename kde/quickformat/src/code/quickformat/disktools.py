#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import errno
from time import sleep
from fcntl import ioctl
import os, sys

# Path to sync executable
PATH_SYNC = '/bin/sync'

# Emulate required asm-generic/ioctl.h macros
_IOC_NRBITS    = 8
_IOC_TYPEBITS  = 8
_IOC_SIZEBITS  = 14
_IOC_DIRBITS   = 2

_IOC_NRMASK    = ((1 << _IOC_NRBITS)   - 1)
_IOC_TYPEMASK  = ((1 << _IOC_TYPEBITS) - 1)
_IOC_SIZEMASK  = ((1 << _IOC_SIZEBITS) - 1)
_IOC_DIRMASK   = ((1 << _IOC_DIRBITS)  - 1)

_IOC_NRSHIFT   = 0
_IOC_TYPESHIFT = (_IOC_NRSHIFT   + _IOC_NRBITS)
_IOC_SIZESHIFT = (_IOC_TYPESHIFT + _IOC_TYPEBITS)
_IOC_DIRSHIFT  = (_IOC_SIZESHIFT + _IOC_SIZEBITS)

# Direction bits.
_IOC_NONE      = 0
_IOC_WRITE     = 1
_IOC_READ      = 2

def _IOC(dir,type,nr,size):
    return (((dir)  << _IOC_DIRSHIFT)  | \
            (type   << _IOC_TYPESHIFT) | \
            ((nr)   << _IOC_NRSHIFT)   | \
            ((size) << _IOC_SIZESHIFT))

def _IO(type, nr):
    """Note: type is specified in hex and nr in decimal."""
    return _IOC(_IOC_NONE,(type),(nr),0)

def BLKRRPART():
    """Returns ioctl number for re-reading partition table."""
    # Kernels >2.6.17 have BLKRRPART defined in include/linux/fs.h.
    return _IO(0x12, 95)
# -------------------------------------------

def refreshPartitionTable(device):
    """Re-Read partition table on device."""

    try:
        fd = os.open(device, os.O_RDONLY)
    except EnvironmentError, (error, strerror):
        print 'Could not open device %s. Reason: %s.'%(device, strerror)
        sys.exit(-1)

    # Sync and wait for Sync to complete
    os.system(PATH_SYNC)
    sleep(2)

    # Call required ioctl to re-read partition table
    try:
        ioctl(fd, BLKRRPART())
    except EnvironmentError, (error, message):
        # Attempt ioctl call twice in case an older kernel (1.2.x) is being used
        os.system(PATH_SYNC)
        sleep(2)

        try:
            ioctl(fd, BLKRRPART())
        except EnvironmentError, (error, strerror):
            print 'IOCTL Error: %s for device %s.'%(strerror, device)
            sys.exit(-1)

    print 'Successfully re-read partition table on device %s.'%(device)
    # Sync file buffers
    os.fsync(fd)
    os.close(fd)

    # Final sync
    print "Syncing %s ...  " % (device),
    os.system(PATH_SYNC)
    sleep(4) # for sync()
    print "Done."


def getMounted():
    parts = []
    for line in open('/proc/mounts'):
        if line.startswith('/dev/'):
            device, path, other = line.split(" ", 2)
            parts.append((device, path, ))
    return parts


def umount(device):
    for dev, path in getMounted():
        if dev == device and path == "/":
            fail(_(FAIL_ROOT) % device)
    runCommand(['/bin/umount', device])



#!/bin/env python

"""
    Author: Sumanth J.V (sumanth@cse.unl.edu, sumanthjv@gmail.com)
    Date:   Jan 30 - 2007
    Version: 1.0
    Description: The script accepts as arguments a list of devices and
                 re-reads the partition table on all the specified
                 devices. The code is relatively safe since it opens the
                 specified devices in read-only mode and calls the same
                 ioctl that fdisk would call when re-reading the partition
                 table. It uses the same macros as defined in the linux
                 kernel to determine the correct ioctl number.
    Warning: Ensure that you use this script on devices that are currently
             not mounted. Please use this program only if you understand
             what it is doing. I do not assume any responsibility for any
             data loss that might occur when using this program.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""



import os, sys
import errno
from time import sleep
from fcntl import ioctl

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

def reReadPartitionTable(device):
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


def main():
    if len(sys.argv)==1 or sys.argv[1] in ['--help', '-h']:
        print('Usage: %s device1 [device2] [device3] ...'%(sys.argv[0]))
    else:
        for dev in sys.argv[1:]:
            reReadPartitionTable(dev)


if __name__ == "__main__":
    main()

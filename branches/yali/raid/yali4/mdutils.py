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

from yali4.sysutils import execWithCapture
import sys
import os
import string
import yali4.partedutils

mdadmOutput = "/tmp/mdadmout"
raidCount = {}

class MdadmError(Exception):

    ## The constructor.
    # @param args The arguments passed to the mdadm command.
    # @param name The the name of the RAID device used in the mdadm command.
    def __init__(self, args, name=None):
        self.args = args
        self.name = name
        self.log = self.getCmdOutput()

    ## Get the output of the last mdadm command run.
    # @return The formatted output of the mdadm command which caused an error.
    def getCmdOutput(self):
        f = open(mdadmOutput, "r")
        lines = reduce(lambda x,y: x + [string.strip(y),], f.readlines(), [])
        lines = string.join(reduce(lambda x,y: x + ["   %s" % (y,)], \
                                    lines, []), "\n")
        return lines

    def __str__(self):
        s = ""
        if not self.name is None:
            s = " for device %s" % (self.name,)
        command = "mdadm " + string.join(self.args, " ")
        return "'%s' failed%s\nLog:\n%s" % (command, s, self.log)


def _mdadm(*args):
    try:
        lines = execWithCapture("mdadm", args, stderr = mdadmOutput)
        lines = string.split(lines, '\n')
        lines = reduce(lambda x,y: x + [y.strip(),], lines, [])
        return lines
    except:
        raise MdadmError, args

## Get the superblock from a RAID device.
# @param The full path to a RAID device name to check.
# This device node must already exist.
# @return A tuple of contents of the RAID superblock, or ValueError.
def raidsbFromDevice(device, raidDevice=False):
    try:
        info = yali4.partedutils._getRaidInfo(device, raidDevice)
        return (info['major'], info['minor'], info['uuid'], info['level'],
                info['nrDisks'], info['totalDisks'], info['mdMinor'])
    except:
        raise ValueError


def _startRaid(mdDevice, mdMinor, uuid):
    print "mdadm -A --uuid=%s --super-minor=%s %s" % (uuid, mdMinor, mdDevice)
    try:
       _mdadm("-A", "--uuid=%s"%(uuid,), "--super-minor=%s"%(mdMinor,), mdDevice)
    except MdadmError:
        ei = sys.exc_info()
        ei[1].name = mdDevice
        raise ei[0], ei[1], ei[2]

# @param aMember is a member of raid 'mdDevice', ex: hdc5
# @param mdDevice is the raid device, ex: md0
def raidstart(mdDevice, aMember):
    """ start raid device mdDevice ( like md0, md1 etc. ) """
    print "starting raid device %s" % (mdDevice,)
    if raidCount.has_key(mdDevice) and raidCount[mdDevice]:
        raidCount[mdDevice] = raidCount[mdDevice] + 1
        return

    raidCount[mdDevice] = 1

    mdInode = "/dev/%s" % mdDevice
    mbrInode = "/dev/%s" % aMember

    if os.path.exists(mdInode):
        minor = os.minor( os.stat(mdInode).st_rdev )
    else:
        minor = int(mdDevice[2:])
    try:
        info = yali4.partedutils._getRaidInfo(mbrInode)
        if info.has_key('mdMinor'):
            minor = info['mdMinor']
        _startRaid( mdInode, minor, info['uuid'])
    except:
        pass

def _stopRaid(mdDevice):
    print "mdadm --stop %s" % (mdDevice,)
    try:
        _mdadm("--stop", mdDevice)
    except MdadmError:
        ei = sys.exc_info()
        ei[1].name = mdDevice
        raise ei[0], ei[1], ei[2]

# @param mdDevice is the raid device to stop. ex: md0
def raidstop(mdDevice):
    print "stopping raid device %s" %(mdDevice,)
    if raidCount.has_key(mdDevice):
        if raidCount[mdDevice] > 1:
            raidCount[mdDevice] = raidCount[mdDevice] -1
            return
        del raidCount[mdDevice]

    devInode = "/dev/%s" % mdDevice
    try:
        _stopRaid(devInode)
    except:
        pass




























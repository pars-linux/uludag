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

from pare.errors import LVMError
from pare.utils import sysutils
import re
import gettext


_ = lambda x: gettext.ldgettext("pare", x)

MAX_LV_SLOTS = 256

def _lvmclear(args):
    try:
        return sysutils.run("lvm",args)
    except Exception:
        #FIXME:log.error
        raise LVMError, args[0]

def _lvmcapture(args):
    try:
        return sysutils.run("lvm", args, capture=True)
    except RuntimeError, (errno, msg):
        #FIXME:log.error
        raise LVMError, msg

def checkLVM():
    check = False
    for path in os.environ["PATH"].split(":"):
        if os.access("%s/lvm" % path, os.X_OK):
            check = True
            break

    if check:
        check = False
        for line in open("/proc/devices").readlines():
            if "device-mapper" in line.split():
                check = True
                break

    return check

config_args = []
config_args_data = { "filterRejects": [],
                     "filterAccepts": [] }


def composeConfig():
    """lvm commands accept lvm.conf type arguments preceded by --config"""

    global config_args, config_args_data
    config_args = []

    filter = ""
    rejects = config_args_data["filterRejects"]

    if len(rejects) > 0:
        for i in range(len(rejects)):
            filter_string = filter_string + ("\"r|%s|\"," % rejects[i])

    # As we add config strings we should check them all.
    if filter == "":
        # Nothing was really done.
        return

    # devices_string can have (inside the brackets) "dir", "scan",
    # "preferred_names", "filter", "cache_dir", "write_cache_state",
    # "types", "sysfs_scan", "md_component_detection".  see man lvm.conf.
    devices = " devices {%s} " % (filter_string) # strings can be added
    config = devices_string # more strings can be added.
    config_args = ["--config", config]

def composeConfig_addFilterRejectRegexp(regexp):
    """ Add a regular expression to the --config string."""
    global config_args_data
    config_args_data["filterRejects"].append(regexp)

    # compoes config once more.
    composeConfig()

def composeConfig_resetFilter():
    global config_args_data
    config_args_data["filterRejects"] = []
    config_args_data["filterAccepts"] = []
# End config_args handling code.

# Names that should not be used int the creation of VGs
vg_blacklist = []

def getPossiblePhysicalExtents(floor=0):
    """Returns a list of integers representing the possible values for
       the physical extent of a volume group.  Value is in KB.

       floor = size (in KB) of smallest PE we care about.
    """

    possiblePE = []
    curpe = 8
    while curpe <= 16384*1024:
        if curpe >= floor:
            possiblePE.append(curpe)
        curpe = curpe * 2

    return possiblePE

def blacklistVG(name):
    global vg_blacklist
    vg_blacklist.append(name)


def getMaxLVSize():
    """ Return the maximum size (in MB) of a logical volume. """
    return (16*1024*1024) #Max is 16TiB

def safeLvmName(name):
    tmp = name.strip()
    tmp = tmp.replace("/", "_")
    tmp = re.sub("[^0-9a-zA-Z._]", "", tmp)
    tmp = tmp.lstrip("_")

    return tmp

def pvcreate(device):
    args = ["pvcreate"] + config_args + [device]

    return  _lvmclear(args)

def pvresize(device, size):
    args = ["pvresize"] + \
            ["--setphysicalvolumesize", ("%dm" % size)] + \
            config_args + \
            [device]

    return _lvmclear(args)

def pvremove(device):
    args = ["pvremove"] + config_args + [device]

    return _lvmclear(args)

def pvinfo(device):
    """
        If the PV was created with '--metadacopies 0', lvm will do some
        scanning of devices to determine from their metadata which VG
        this PV belongs to.

        pvs -o pv_name,pv_mda_count,vg_name,vg_uuid --config \
            'devices { scan = "/dev" filter = ["a/loop0/", "r/.*/"] }'
    """

    #cfg = "'devices { scan = \"/dev\" filter = [\"a/%s/\", \"r/.*/\"] }'"·
    args = ["pvs", "--noheadings"] + \
            ["--units", "m"] + \
            ["-o", "pv_name,pv_mda_count,vg_name,vg_uuid"] + \
            config_args + \
            [device]

    buffer = _lvmcapture(args)

    values = buffer.split()
    if not values:
        raise LVMError(_("pvinfo failed for %s" % device))

    # don't raise an exception if pv is not a part of any vg
    pv_name = values[0]
    try:
        vg_name, vg_uuid = values[2], values[3]
    except IndexError:
        vg_name, vg_uuid = "", ""

    info = {'pv_name': pv_name,
            'vg_name': vg_name,
            'vg_uuid': vg_uuid}

    return info

def vgcreate(vg_name, pv_list, pe_size):
    argv = ["vgcreate"]
    if pe_size:
        argv.extend(["-s", "%dm" % pe_size])
    argv.extend(config_args)
    argv.append(vg_name)
    argv.extend(pv_list)

    return _lvmclear(args)

def vgremove(vg_name):
    args = ["vgremove"] + config_args + [vg_name]

    return _lvmclear(args)

def vgactivate(vg_name):
    args = ["vgchange", "-a", "y"] + config_args + [vg_name]

    return _lvmclear(args)

def vgdeactivate(vg_name):
    args = ["vgchange", "-a", "n"] + config_args + [vg_name]

    return _lvmclear(args)

def vgreduce(vg_name, pv_list, rm=False):
    """ Reduce a VG.

    rm -> with RemoveMissing option.
    Use pv_list when rm=False, otherwise ignore pv_list and call vgreduce with
    the --removemissing option.
    """
    args = ["vgreduce"]
    if rm:
        args.extend(["--removemissing", vg_name])
    else:
        args.extend([vg_name] + pv_list)

    return _lvmclear(args)

def vginfo(vg_name):
    args = ["vgs", "--noheadings", "--nosuffix"] + \
            ["--units", "m"] + \
            ["-o", "name,size,uuid,max_pv,pv_count,vg_extent_size,vg_extent_count,vg_free_count,vg_free,max_lv"] + \
            config_args + \
            [vg_name]

    buffer = _lvmcapture(args)

    #print "buffer:%s" % buffer
    buffer_dict = buffer.split()
    #print "len(buffer_dict) :%d" % len(buffer_dict) 
    if len(buffer_dict) != 10:
        raise LVMError(_("vginfo failed for %s" % vg_name))

    info = {}

    (info['name'],
     info['size'],
     info['uuid'],
     info['max_pv'],
     info['pv_count'],
     info['vg_extent_size'],
     info['vg_extent_count'],
     info['vg_free_count'],
     info['vg_free'],
     info['max_lv'],
    ) = buffer_dict

    return info

def lvs(vg_name):
    args = ["lvs", "--noheadings", "--nosuffix"] + \
            ["--units", "m"] + \
            ["-o", "lv_name,lv_uuid,lv_size"] + \
            config_args + \
            [vg_name]

    buffer = _lvmcapture(args)

    lvs = {}
    for line in buffer.splitlines():
        line = line.strip()
        if not line:
            continue
        (name, uuid, size) = line.split()
        lvs[name] = {"size": size,
                     "uuid": uuid}

    if not lvs:
        raise LVMError(_("lvs failed for %s" % vg_name))

    return lvs

def lvcreate(vg_name, lv_name, size):
    args = ["lvcreate"] + \
            ["-L", "%dm" % size] + \
            ["-n", lv_name] + \
            config_args + \
            [vg_name]


    return _lvmclear(args)

def lvremove(vg_name, lv_name):
    args = ["lvremove"] + \
            config_args + \
            ["%s/%s" % (vg_name, lv_name)]

    return _lvmclear(args)

def lvresize(vg_name, lv_name, size):
    args = ["lvresize"] + \
            ["-L", "%dm" % size] + \
            config_args + \
            ["%s/%s" % (vg_name, lv_name)]

    return _lvmclear(args)

def lvactivate(vg_name, lv_name):
    # see if lvchange accepts paths of the form 'mapper/$vg-$lv'
    args = ["lvchange", "-a", "y"] + \
            config_args + \
            ["%s/%s" % (vg_name, lv_name)]

    return _lvmclear(args)

def lvdeactivate(vg_name, lv_name):
    args = ["lvchange", "-a", "n"] + \
            config_args + \
            ["%s/%s" % (vg_name, lv_name)]

    return _lvmclear(args)

def lvinfo(lv_path):
    args = ["lvs", "--noheadings", "--nosuffix"] + \
            ["--units", "m"] + \
            ["-o", "lv_name,lv_uuid,lv_size,vg_name"] + \
            config_args + \
            [lv_path]

    print "args:%s" % args
    buffer = _lvmcapture(args)

    buffer_dict = buffer.split()
    if len(buffer_dict) != 4:
        raise LVMError(_("lvinfo failed for %s" % lv_path))

    info = {}

    (info['lv_name'],
     info['lv_uuid'],
     info['lv_size'],
     info['vg_name']) = buffer_dict

    return info

def lvlist(vg_name):
    lvs = []
    args = ["lvs", "--noheadings",
            "--nosuffix", "--options", "vg_name,lv_name"]
    
    info = {}
    lines = None
    lines = _lvmcapture(args).strip().split("\n")
    print lines
    for line in lines:
        buffer = line.split()
        
        print "len(buffer) %d" % len(buffer)
        (info['vg_name'], info['lv_name']) = buffer 
        #print "vg:%s lv:%s" % (info['vg_name'],info['lv_name'])
        if vg_name == info['vg_name']:
            lvs.append(info['lv_name'])
    
    return lvs

def pvlist():
    pvs = []
    
    args = ["pvdisplay", "-C", "--noheadings", "--units", "m", "--nosuffix", "--options", "pv_name,vg_name,dev_size"]
        
    lines = _lvmcapture(args).strip().split("\n")
    for line in lines:
        buffer = line.split()
        
        (dev, vg, size) = buffer
         
        pvs.append((dev, vg, size))
        
    return pvs

def vglist():
    vgs = []
    args = ["vgdisplay", "--noheadings", "--units", "m",
            "--nosuffix", "--options",
            "vg_name,vg_size,vg_extent_size,vg_free"]
    
    lines = _lvmcapture(args).strip().split("\n")
    for line in lines:
        buffer = line.split()
        
        (vg, size, pesize, free) = line
        vgs.append((vg, size, pesize, free))
    
    return vgs
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

from errors import LVMError
import sysutils
import gettext

_ = lambda x: gettext.ldgettext("pare", x)

MAX_LV_SLOTS = 256

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
    global lvm_vg_blacklist
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
    args = ["pvcreate"] + \
            config_args + \
            [device]

    return_code = sysutils.execClear("lvm",
                                     args,
                                     stdout = "/dev/tty5",
                                     stderr = "/dev/tty5")

    if return_code == 0:
        raise LVMError(_("pvcreate failed for %s" % device))


def pvresize(device, size):
    args = ["pvresize"] + \
            ["--setphysicalvolumesize", ("%dm" % size)] + \
            config_args + \
            [device]

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")
    if return_code:
        raise LVMError(_("pvresize failed for %s" % device))

def pvremove(device):
    args = ["pvremove"] + \
            config_args + \
            [device]

    return_code = sysutils.execClear("lvm",
                                    args,
                                    stdout = "/dev/tty5",
                                    stderr = "/dev/tty5")
    if return_code == 0:
        raise LVMError(_("pvremove failed for %s" % device))

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

    buffer = sysutils.execWithCapture("lvm",
                                            args,
                                            stderr = "/dev/tty5")
    values = buffer.split()
    if not values:
        raise LVMError(_("vgcreate failed for %s" % vg_name))

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

    return_code = sysutils.execClear("lvm", argv,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")

    if return_code == 0:
        raise LVMError(_("vgcreate failed for %s" % vg_name))

def vgremove(vg_name):
    args = ["vgremove"] + \
            config_args +\
            [vg_name]

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")

    if return_code == 0:
        raise LVMError(_("vgremove failed for %s" % vg_name))

def vgactivate(vg_name):
    args = ["vgchange", "-a", "y"] + \
            config_args + \
            [vg_name]

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")
    if return_code == 0:
        raise LVMError(_("vgactivate failed for %s" % vg_name))

def vgdeactivate(vg_name):
    args = ["vgchange", "-a", "n"] + \
            config_args + \
            [vg_name]

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")

    if return_code == 0:
        raise LVMError(_("vgdeactivate failed for %s" % vg_name))

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

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")

    if return_code == 0 :
        raise LVMError(_("vgreduce failed for %s" % vg_name))

def vginfo(vg_name):
    args = ["vgs", "--noheadings", "--nosuffix"] + \
            ["--units", "m"] + \
            ["-o", "uuid,size,free,extent_size,extent_count,free_count,pv_count"] + \
            config_args + \
            [vg_name]

    buffer = sysutils.execWithCapture("lvm",
                                    args,
                                    stderr="/dev/tty5")
    buffer_dict = buffer.split()
    if len(info) != 7:
        raise LVMError(_("vginfo failed for %s" % vg_name))

    info = {}

    (info['uuid'],
    info['size'],
    info['free'],
    info['pe_size'],
    info['pe_count'],
    info['pe_free'],
    info['pv_count']) = buffer_dict

    return info

def lvs(vg_name):
    args = ["lvs", "--noheadings", "--nosuffix"] + \
            ["--units", "m"] + \
            ["-o", "lv_name,lv_uuid,lv_size"] + \
            config_args + \
            [vg_name]

    buffer = sysutils.execWithCapture("lvm",
                                args,
                                stderr="/dev/tty5")

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

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")

    if return_code == 0:
        raise LVMError(_("lvcreate failed for %s/%s" % (vg_name, lv_name)))

def lvremove(vg_name, lv_name):
    args = ["lvremove"] + \
            config_args + \
            ["%s/%s" % (vg_name, lv_name)]

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")

    if return_code:
        raise LVMError(_("lvremove failed for %s" % lv_name))

def lvresize(vg_name, lv_name, size):
    args = ["lvresize"] + \
            ["-L", "%dm" % size] + \
            config_args + \
            ["%s/%s" % (vg_name, lv_name)]

    rc = iutil.execWithRedirect("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5",
                                searchPath=1)

    if rc:
        raise LVMError("lvresize failed for %s" % lv_name)

def lvactivate(vg_name, lv_name):
    # see if lvchange accepts paths of the form 'mapper/$vg-$lv'
    args = ["lvchange", "-a", "y"] + \
            config_args + \
            ["%s/%s" % (vg_name, lv_name)]

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")
    if return_code == 0:
        raise LVMError(_("lvactivate failed for %s" % lv_name))

def lvdeactivate(vg_name, lv_name):
    args = ["lvchange", "-a", "n"] + \
            config_args + \
            ["%s/%s" % (vg_name, lv_name)]

    return_code = sysutils.execClear("lvm", args,
                                stdout = "/dev/tty5",
                                stderr = "/dev/tty5")

    if return_code == 0:
        raise LVMError(_("lvdeactivate failed for %s" % lv_name))
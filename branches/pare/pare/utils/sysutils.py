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

import subprocess
from pardus.sysutils import find_executable
import logging
import os
import sys
log = logging.getLogger("pare")

def checkNumeric(num):
    if num is None:
        num =  0
    elif not (isinstance(num, int) or isinstance(num, long) or isinstance(num, float)):
        raise ValueError("Value must be a number!")
    return num

def run(cmd, params, capture=False):
    #print "BURAAAA"
    #print "params:%s" % params
    # Merge parameters with command
    if params:
        cmd = "%s %s"% (cmd, ' '.join(params))
    #print "%s" % cmd
    
    #print "split::: %s" % cmd
    # to use Popen we need a tuple
    _cmd = tuple(cmd.split())
    #print "_cmd%s" % _cmd
    #log.info("RUN : %s" % cmd)

    #stdout must return LC_ALL=C
    env = os.environ.copy()
    env.update({"LC_ALL": "C"})

    # Create an instance for Popen
    try:
        proc = subprocess.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError, (errno, msg):
        raise RuntimeError, "Error running " + _cmd + ": " + msg
        
    

    # Capture the output
    stdout, stderr = proc.communicate()
    result = proc.poll()

    log.error(stderr)
    log.debug(stdout)

    # if return code larger then zero, means there is a problem with this command
    if result > 0:
        log.error("FAILED : %s" % cmd)
        return False
    log.info("SUCCESS : %s" % cmd)
    if capture:
        return stdout
    return True


def mount(source, target, fs, needs_mtab=False):
    params = ["-t", fs, source, target]
    if not needs_mtab:
        params.insert(0,"-n")

    mount_res = run("mount",params)

    return mount_res


def umount(mountpoint=''):

    umount_res = execClear("umount", mountpoint)

def notify_kernel(path, action="change"):
    """ Signal the kernel that the specified device has changed. """
    log.debug("notifying kernel of '%s' event on device %s" % (action, path))
    path = os.path.join(path, "uevent")
    if not path.startswith("/sys/") or not os.access(path, os.W_OK):
        log.debug("sysfs path '%s' invalid" % path)
        raise ValueError("invalid sysfs path")

    f = open(path, "a")
    f.write("%s\n" % action)
    f.close()

def get_sysfs_path_by_name(dev_name, class_name="block"):
    dev_name = os.path.basename(dev_name)
    sysfs_class_dir = "/sys/class/%s" % class_name
    dev_path = os.path.join(sysfs_class_dir, dev_name)
    if os.path.exists(dev_path):
        return dev_path

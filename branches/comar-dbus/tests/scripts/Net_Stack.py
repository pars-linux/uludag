#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import re
import string
import subprocess

rc_path = "/etc/resolv.conf"
name_path = "/etc/env.d/01hostname"
hosts_path = "/etc/hosts"
env_cmd = "/sbin/update-environment"
host_cmd = "/usr/bin/hostname %s"
valid_name_chars = string.ascii_letters + string.digits + '.' + '_' + '-'

def getDefs():
    defs = []
    for line in file(rc_path):
        if line.startswith("nameserver "):
            defs.append(line.split(" ", 1)[1].rstrip("\n"))
    return defs

def getNameServers():
    return getDefs()

def setNameServers(nameservers=None, searchdomain=None):
    f = file(rc_path)
    # keep rest of the resolv.conf
    restof = filter(lambda x: not x.strip().startswith("nameserver"), f.readlines())
    if searchdomain and not searchdomain == "None":
        restof = filter(lambda x: not x.strip().startswith("search") and \
                                  not x.strip().startswith("domain"), restof)
    f.close()

    servers = map(lambda x: "nameserver %s\n" % x, nameservers)
    f = file(rc_path, "w")
    if searchdomain and not searchdomain == "None":
        f.write("search %s\n" % searchdomain)
    f.write("".join(restof) + "".join(servers))
    f.close()

def useNameServers(nameservers=None, searchdomain=None):
    defs = getDefs()
    if nameservers and nameservers != []:
        temp = nameservers
        temp.extend(defs)
        defs = temp
    setNameServers(defs, searchdomain)

def getHostName():
    cmd = subprocess.Popen(["/usr/bin/hostname"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    a = cmd.communicate()
    if a[1] == "":
        return a[0].rstrip("\n")
    return ""

def setHostName(hostname=None):
    if not hostname:
        return
    invalid = filter(lambda x: not x in valid_name_chars, hostname)
    if len(invalid) > 0:
        fail("Invalid characters '%s' in hostname" % ("".join(invalid)))
    
    # hostname
    if os.path.exists(name_path):
        f = file(name_path)
        data = f.read()
        f.close()
        data = re.sub('HOSTNAME="(.*)"', 'HOSTNAME="%s"' % hostname, data)
    else:
        data = 'HOSTNAME="%s"\n' % hostname
    f = file(name_path, "w")
    f.write(data)
    f.close()
    
    # hosts
    f = file(hosts_path)
    data = f.readlines()
    f.close()
    f = file(hosts_path, "w")
    flag = 1
    for line in data:
        if line.startswith("127.0.0.1"):
            line = "127.0.0.1 localhost %s\n" % hostname
            flag = 0
        f.write(line)
    if flag:
        f.write("127.0.0.1 localhost %s\n" % hostname)
    f.close()
    
    # update environment
    os.system(env_cmd)
    
    # we dont call the following command, it mess up system
    # hostname changes take effect after restart
    #os.system(host_cmd % hostname)

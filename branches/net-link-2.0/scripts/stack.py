#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

HEADER_DEFAULT = """
"""

HEADER_DYNAMIC = """
"""

MAX_SERVERS = 3

def getSearchDomain():
    for line in file("/etc/resolv.default.conf"):
        line = line.strip()
        if line.startswith("searchdomain"):
            return line.split()[1]
    return None

# Network.Stack methods

def getNameServers():
    servers = []
    if not os.access("/etc/resolv.default.conf", os.R_OK):
        return servers
    for line in file("/etc/resolv.default.conf"):
        line = line.strip()
        if line.startswith("nameserver"):
            servers.append(line.split()[1])
    return servers

def setNameServers(nameservers, searchdomain):
    f = file("/etc/resolv.default.conf")
    f.write(HEADER_DEFAULT)

    for server in nameservers:
        f.write("nameserver %s\n" % server)

    if searchdomain:
        f.write("searchdomain %s\n" % searchdomain)

    f.close()

def useNameServers(nameservers, searchdomain):
    # Append default name servers
    nameservers.extend(getNameServers())

    f = file("/etc/resolv.conf")
    f.write(HEADER_DYNAMIC)

    for server in nameservers[:MAX_SERVERS]:
        f.write("nameserver %s\n" % server)

    if searchdomain:
        f.write("searchdomain %s\n" % searchdomain)
    elif getSearchDomain():
        f.write("searchdomain %s\n" % getSearchDomain())

    f.close()

def getHostName():
    # TODO: Return hostname (from config)
    return ""

def setHostName(hostname):
    # TODO: Save hostname (to config)
    pass

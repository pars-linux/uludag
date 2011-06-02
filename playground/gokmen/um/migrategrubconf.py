#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
from pardus.diskutils import getRoot

grubconf = "/boot/grub/grub.conf"
#grubconf = "/tmp/sil/grub.conf"
debug = False
#debug = True
rootDevice = ""

def loadFile(_file):
    try:
        f = open(_file)
        d = f.read().split("\n")
        f.close()
        return d
    except IOError:
        return []

def writeFile(_file, data):
    try:
        if debug:
            f = open("%s.new" % _file, "w")
        else:
            f = open(_file, "w")
        f.write(data)
        f.close()

    except IOError:
        print "Could not write to %s" % _file

def printd(mystr):
    if debug:
        print mystr

def capture(*cmd):
    a = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return a.communicate()

def isRealRoot(realroot, tocheck):
    if tocheck.startswith("/dev"):
        foundDevice = tocheck
    else:
        foundDevice = capture("findfs %s" % tocheck)[0]
        foundDevice = foundDevice.strip(" \n")

    printd("DEVNAME: %s" % foundDevice)

    return (foundDevice == realroot)

def migrateGrubconf(cfg=grubconf):
    rootDevice = getRoot()
    oldConfig = loadFile(cfg)
    newConfig = []

    printd("REALROOT: %s" % rootDevice)

    for line in oldConfig:
        if line.startswith("kernel") and "root=" in line:
            printd("\nLINEMATCH: %s" % line)

            grubroot = re.sub("(.*root=)([^ ]*)( .*)", r"\2", line)
            printd("GRUBROOT: %s" % grubroot)

            if isRealRoot(rootDevice, grubroot):
                printd("FOUNDROOT: %s  =  %s" % (rootDevice, grubroot))
                line = re.sub(" splash[^ ]*", " splash", line)
                line = re.sub(" vga[^ ]*", "", line)

        newConfig.append(line)

    writeFile(cfg, "\n".join(newConfig))

if __name__ == "__main__":
    migrateGrubconf(grubconf)


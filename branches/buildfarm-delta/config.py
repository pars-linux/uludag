#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2008 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
import os

#Some configuration info for other modules..
workDir          = "/var/pisi/"
outputDir        = "/var/cache/pisi/buildlogs/"
binaryPath       = "/var/cache/pisi/packages/"
testPath         = "/var/cache/pisi/packages-test/"
deltaPath        = "/var/cache/pisi/packages-delta/"
localPspecRepo   = "/root/2008"
logFile          = "/var/cache/pisi/buildfarm.log"

#information for mailer module.
mailFrom         = "buildfarm@pardus.org.tr"
announceAddr     = "gelistirici@pardus.org.tr"
ccList           = ["paketler-commits@pardus.org.tr"]
#ccList           = ["ekin@pardus.org.tr"]
smtpServer       = "mail.pardus.org.tr"
useSmtpAuth      = True
smtpUser         = ""
smtpPassword     = ""

# Blacklist for delta packages. Buildfarm will never build
# delta packages for them.

blacklist = ["skype",
             "kernel",
             "kernel-debug",
             "openarena-data",
             "vdrift-data-full",
             "eclipse-jdt-binary",
             "nvidia-drivers177",
             "nvidia-drivers180",
             "nvidia-drivers173",
             "nvidia-drivers-new",
             "nvidia-drivers-old"]

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
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
deltaPath        = binaryPath
pardus2007       = "/mnt/sda5/mudur/pardus-2007/"
localPspecRepo   = "%s/2007" % os.getcwd()
logFile          = "/var/cache/pisi/buildfarm.log"

#information for mailer module.
mailFrom         = "buildfarm@pardus.org.tr"
ccList           = []
smtpServer       = "mail.pardus.org.tr"
useSmtpAuth      = False
smtpUser         = ""
smtpPassword     = ""

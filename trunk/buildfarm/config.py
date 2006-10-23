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

class CfgError(Exception):
    pass

#Some configuration info for other modules..
workDir          = "/var/tmp/pisi/"
outputDir        = "/var/tmp/pisi/buildlogs/"
binaryPath       = "/var/cache/pisi/packages/"
localPspecRepo   = "%s/exampleRepo" % os.getcwd()
logFile          = "%s/buildfarm.log" % workDir

#information for mailer module.
mailFrom         = "buildfarm@pardus.org.tr"
ccList           = []
smtpServer       = "mail.uludag.org.tr"
smtpUser         = ""
smtpPassword     = ""

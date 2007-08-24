#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006,2007 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

# XMLRPC Connection parameters
HOST = "localhost"
PORT = 443

#Some configuration info for other modules..
workDir          = "/var/pisi/"
outputDir        = "/var/pisi/buildlogs/"
binaryPath       = "/var/cache/pisi/packages/"
localPspecRepo   = "./exampleRepo"      # must be an absolute path!
logFile          = "%s/buildfarm.log" % workDir
stateFile        = "%s/buildfarm.state" % workDir

#information for mailer module.
mailFrom         = "buildfarm@pardus.org.tr"
ccList           = []
smtpServer       = "mail.pardus.org.tr"
smtpUser         = ""
smtpPassword     = ""

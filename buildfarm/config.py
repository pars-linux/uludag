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
#

import os
from pisi.util import join_path

class CfgError(Exception):
    pass

#Some configuration info for other modules..

workDir          = "/var/tmp/pisi/"
outputDir        = "/var/tmp/pisi/buildlogs"
newBinaryPath   = "/var/cache/pisi/packages/newBinaries/"
localPspecRepo   = join_path(os.getcwd(), "/exampleRepo")
logFile          = join_path(workDir, "buildfarm.log")
smtpUserInfo     = './smtpUserInfo'

#information for mailer module.
mailFrom        = "buildfarm@pardus.org.tr"
ccList          = []
smtpServer      = 'mail.uludag.org.tr'
try:
    smtpUser, smtpPassword = open(smtpUserInfo).readline().strip().split(':')
except:
    smtpUser, smtpPassword = '', ''    


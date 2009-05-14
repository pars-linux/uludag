#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

# Basic buildfarm configuration.
#
# Workdir
workDir          = "/var/pisi/"

# Local source repo
localPspecRepo   = "/root/2009"

# Main buildfarm log
logFile          = "/var/cache/pisi/buildfarm.log"

# All package logs are kept in this directory as
# package_name-log.
outputDir        = "/var/cache/pisi/buildlogs/"

# This repo contains all binaries and deltas built
binaryPath       = "/var/cache/pisi/packages/"

# This repo contains latest binaries and 3 deltas -
# one delta from iso release to latest binary, two deltas
# from previus releases.
testPath         = "/var/cache/pisi/packages-test/"

# This repo contains only the latest binaries and deltas.
# It seems that it's not used anymore
deltaPath        = "/var/cache/pisi/packages-delta/"

# This repo contains only the dbginfo packages
# Set debugSupport to 'True' for managing a separate
# debug repository in debugPath.
debugSupport     = False
debugPath        = "/var/cache/pisi/packages-debug/"

# Information for mailer module.
# Edit templates.py for the structure of mails.

# Set this to 'False' for turning off notification e-mails
sendEmail        = True

# Default from address
mailFrom         = "buildfarm@pardus.org.tr"

# This address is used for automated reports
announceAddr     = "buildfarm@pardus.org.tr"

# This is the default CC address for all info and error mails
# Error mails are sent to package maintainer and CC'ed to this address,
# info mails have no 'TO' address, only this one as a 'CC'.
ccList           = ["buildfarm@pardus.org.tr"]

# Server for sending mail.
smtpServer       = "mail.pardus.org.tr"

# Create and edit mailauth.py for authentication if needed
# Set this to 'False' for not authenticating on the SMTP server
useSmtpAuth      = True

# Set this to 'False' if you don't want to generate delta packages
generateDelta    = True

# Blacklist for delta packages. Buildfarm will never build
# delta packages for them.

deltaBlacklist   = ["skype",
                    "kernel",
                    "flashplugin",
                    "kernel-debug",
                    "openarena-data",
                    "vdrift-data-full",
                    "eclipse-jdt-binary",
                    "nvidia-drivers177",
                    "nvidia-drivers180",
                    "nvidia-drivers173",
                    "nvidia-drivers-new",
                    "nvidia-drivers-old"]

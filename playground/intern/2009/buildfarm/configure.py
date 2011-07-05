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

import sys

# i18n
import gettext
__trans = gettext.translation('buildfarm', fallback=True)
_ = __trans.ugettext

# Configuration text
confText = """\
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

# Configuration info for buildfarm directories
workDir          = "%(workdir)s"
outputDir        = "%(outputdir)s"
binaryPath       = "%(binarypath)s"
localPspecRepo   = "%(localpspecrepo)s"
logFile          = "%(workdir)s%(logfile)s"

# Informations for mailer module.
mailFrom         = "%(mailfrom)s"
ccList           = []
smtpServer       = "%(smtpserver)s"
smtpUser         = "%(smtpuser)s"
smtpPassword     = "%(smtppassword)s"

#daemon related configuration strings.
daemonLog        = "%(daemonlog)s"

"""

# Dictionary which holds the configuration informations
answers = {'workdir'            :'/var/pisi/',
           'outputdir'          :'/var/pisi/buildlogs',
           'binarypath'         :'/var/cache/pisi/packages',
           'localpspecrepo'     :'',
           'logfile'            :'buildfarm.log',
           'mailfrom'           :'buildfarm@pardus.org.tr',
           'smtpserver'         :'mail.pardus.org.tr',
           'smtpuser'           :'',
           'smtppassword'       :'',
           'daemonlog'          :'/var/log/buildfarmd.log'}
    
def processAnswer(str, conf):
    if str:
        answers[conf] = str

if __name__ == "__main__":
    
    # Start configuration
    print _("Welcome to pardus buildfarm daemon configuration.\n")
    
    processAnswer(raw_input(_("Working directory of buildfarm[%s] : " % answers['workdir'])), "workdir")
    processAnswer(raw_input(_("Per-package logs directory[%s] : " % answers['outputdir'])), "outputdir")
    processAnswer(raw_input(_("Directory in which the PiSi packages will be placed[%s] : " % answers['binarypath'])), "binarypath")
    processAnswer(raw_input(_("Local pspec repository[%s] : " % answers['localpspecrepo'])), "localpspecrepo")
    processAnswer(raw_input(_("General buildfarm log[%s] : " % answers['logfile'])), "logfile")
    processAnswer(raw_input(_("'From:' string for information e-mails[%s] : " % answers['mailfrom'])), "mailfrom")
    processAnswer(raw_input(_("SMTP Server[%s] : " % answers['smtpserver'])), "smtpserver")
    processAnswer(raw_input(_("SMTP Server username[%s] : " % answers['smtpuser'])), "smtpuser")
    processAnswer(raw_input(_("SMTP Server password[%s] : " % answers['smtppassword'])), "smtppassword")
    processAnswer(raw_input(_("Log file of buildfarm daemon[%s] : " % answers['daemonlog'])), "daemonlog")
    
    # Write configuration file
    print _("Writing configuration file...")
    try:
        f = open("config1.py","w")
        f.write(confText % answers)
        f.close()
    except:
        print _("File I/O Error!")
        sys.exit(1)
        
    print _("Configuration is completed!")
    sys.exit(0)
    
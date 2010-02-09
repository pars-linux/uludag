#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

import os
import socket
import smtplib

import pisi.specfile
import pisi.config

from buildfarm import logger, templates
from buildfarm.auth import Auth
from buildfarm.config import configuration as conf

# Authentication stuff
(username, password) = Auth().get_credentials("Mailer")

# Parse pisi.conf for distribution informations
pconfig = pisi.config.Config()


class MailerError(Exception):
    pass

def send(message, pspec = "", _type = ""):

    def wrap(message, length=72):
        return reduce(lambda line, word: "%s%s%s" %
                      (line,
                       [" ", "\n"][(len(line)-line.rfind("\n")-1 + len(word.split("\n",1)[0]) >= length)],
                       word),
                      message.split(" "))

    if not conf.sendemail:
        logger.info("*** Sending of notification e-mails is turned off.")
        return

    recipientsName, recipientsEmail = [], []
    if pspec:
        specFile = pisi.specfile.SpecFile()
        specFile.read(os.path.join(conf.localpspecrepo, pspec))
        recipientsName.append(specFile.source.packager.name)
        recipientsEmail.append(specFile.source.packager.email)

    packagename = os.path.basename(os.path.dirname(pspec))
    last_log = "".join(open(conf.logfile).readlines()[-20:])
    message = templates._all[_type] % {
                                        'log'          : wrap(last_log),
                                        'recipientName': " ".join(recipientsName),
                                        'mailTo'       : ", ".join(recipientsEmail),
                                        'ccList'       : ', '.join(conf.cclist),
                                        'mailFrom'     : conf.mailfrom,
                                        'announceAddr' : conf.announceaddr,
                                        'subject'      : pspec or _type,
                                        'message'      : wrap(message),
                                        'pspec'        : pspec,
                                        'type'         : _type,
                                        'packagename'  : packagename,
                                        'distribution' : pconfig.values.general.distribution,
                                        'release'      : pconfig.values.general.distribution_release,
                                     }

    # timeout value in seconds
    socket.setdefaulttimeout(10)

    try:
        session = smtplib.SMTP(conf.smtpserver)
    except:
        logger.error("*** Failed sending e-mail: Couldn't open session on %s." % conf.smtpserver)
        return

    if conf.usesmtpauth:
        try:
            session.login(username, password)
        except smtplib.SMTPAuthenticationError:
            logger.error("*** Failed sending e-mail: Authentication failed.")
            return

    try:
        if _type == "announce":
            session.sendmail(conf.mailfrom, conf.announceaddr, message)
        else:
            session.sendmail(conf.mailfrom, recipientsEmail + conf.cclist, message)
    except smtplib.SMTPRecipientsRefused:
        logger.error("*** Failed sending e-mail: Recipient refused probably because of a non-authenticated session.")

def error(message, pspec):
    send(message, pspec, _type="error")

def info(message):
    send(message, _type="info")

def announce(message):
    send(message, _type="announce")

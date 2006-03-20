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

""" Standart Python Modules """
import os
import sys
import smtplib
import xml.dom.minidom as mdom

sys.path.append(".")
sys.path.append("..")

""" BuildFarm Modules """
import buildfarm.config as config
import buildfarm.logger as logger
import buildfarm.templates as tmpl
from buildfarm import Get

class MailerError(Exception):
    pass


RecInfo = lambda x, y: [i.firstChild.wholeText for i in \
             Get(Get(Get(y, "Source")[0], "Packager")[0], x)]

def send(message, pspec = '', type = ''):
    recipientsName, recipientsEmail = [], []
    if pspec:
        dom = mdom.parse(os.path.join(config.localPspecRepo, pspec))
        recipientsName = RecInfo('Name', dom.documentElement)
        recipientsEmail = RecInfo('Email', dom.documentElement)

    templates = {'error': tmpl.error_message,
                 'info' : tmpl.info_message}

    msg = templates.get(type) % {'log'          : ''.join(open(config.logFile).readlines()[-20:]),
                                 'recipientName': ' ve '.join(recipientsName),
                                 'mailTo'       : ', '.join(recipientsEmail),
                                 'ccList'       : ', '.join(config.ccList),
                                 'mailFrom'     : config.mailFrom,
                                 'subject'      : pspec or type,
                                 'message'      : message,
                                 'pspec'        : pspec,
                                 'type'         : type}

    session = smtplib.SMTP(config.smtpServer)

    if config.smtpPassword:
        session.login(config.smtpUser, config.smtpPassword)

    smtpresult = session.sendmail(config.mailFrom, recipientsEmail + config.ccList, msg)

def error(message, pspec):
    send(message, pspec, type = 'error')

def info(message):
    send(message, type = 'info')

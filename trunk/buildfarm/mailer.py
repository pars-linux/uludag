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
from buildfarm import Get

class MailerError(Exception):
    pass


RecInfo = lambda x, y: [i.firstChild.wholeText for i in \
             Get(Get(Get(y, "Source")[0], "Packager")[0], x)]

messagetmpl = """\
From: Derleme =?utf-8?q?=C3=87iftli=C4=9Fi?= <%s>
To: %s
Cc: %s
Subject: %s
Content-Type: text/plain;
            utf-8

 Merhaba,

 Bu ileti derleme çiftliği tarafından otomatik olarak gönderilmektedir.

 Sorumlusu '%s' olan '%s' dosyası işlenirken olmaması gereken bir şeyler oldu. Hata mesajı şöyle:


-- <Hata Mesajı> -------------------------------------------------------

%s

-- </Hata Mesajı> ------------------------------------------------------


 Olaydan önce tutlan kayıtların son 20 satırı ise şöyle idi:


-- <Kayıt Dosyası> -----------------------------------------------------

%s

-- </Kayıt Dosyası> ----------------------------------------------------


 Kolay gelsin.
 (Vallahi ben bir şey yapmadım..)
"""

def send(pspec, message):
    dom = mdom.parse(os.path.join(config.localPspecRepo, pspec))
    recipientsName, recipientsEmail = RecInfo('Name', dom.documentElement), RecInfo('Email', dom.documentElement)


    message = messagetmpl % (config.mailFrom, \
                             ', '.join(recipientsEmail),\
                             ', '.join(config.ccList),\
                             pspec,\
                             ' ve '.join(recipientsName),\
                             pspec,\
                             message,\
                             ''.join(open(config.logFile).readlines()[-20:]))


    session = smtplib.SMTP(config.smtpServer)

    if config.smtpPassword:
        session.login(config.smtpUser, config.smtpPassword)

    smtpresult = session.sendmail(config.mailFrom, recipientsEmail + config.ccList, message)


#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import logging
import simplejson
import socket

# PiSi
import pisi

# COMAR
import comar


def process(message, dryrun=False):
    if message.type == "command":
        if message.command == "apache info":
            if "apache" in pisi.api.list_installed():
                link = comar.Link()
                if str(link.System.Service["apache"].info()[2]) in ("started", "on"):
                    args = "http://%s/" % socket.gethostname()
                else:
                    args = True
            else:
                args = False
            message.reply("apache info:%s" % simplejson.dumps(args))

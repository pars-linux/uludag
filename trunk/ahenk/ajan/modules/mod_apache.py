#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import logging
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
                    message.reply("apache info:http://%s/" % socket.gethostname())
                else:
                    message.reply("apache info:yes")
            else:
                message.reply("apache info:no")

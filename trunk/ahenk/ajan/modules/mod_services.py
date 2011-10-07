#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import logging
from dbus import DBusException

# COMAR
import comar


def process(message, options):
    """
        Policy/command processor.

        Arguments:
            message: Message object
            options: Options
    """

    dryrun = options.dryrun

    if message.type == "command":
        if message.command == "service.info":
            link = comar.Link()
            args = []
            for package in link.System.Service:
                type_, desc_, status_ = link.System.Service[package].info()
                args.append((package, desc_, status_))
            message.reply("service.info", args)
        elif message.command == "service.start":
            package = message.arguments[0]
            link = comar.Link()
            try:
                link.System.Service[package].start()
                message.reply("service.start.status", "Successful")
            except DBusException, e:
                message.reply("service.start.status", str(e))
        elif message.command == "service.stop":
            package = message.arguments[0]
            link = comar.Link()
            try:
                link.System.Service[package].stop()
                message.reply("service.stop.status", "Successful")
            except DBusException, e:
                message.reply("service.stop.status", str(e))

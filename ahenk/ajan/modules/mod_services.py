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
            logging.info("---- replied ----")

    elif message.type == "policy":

        if "serviceStart" in message.policy:
            start_set = []
            for packages in message.policy["serviceStart"]:

                try:
                    for package in packages.split(","):
                        start_set.append(package)
                except ValueError:
                    start_set = []
                    break

                logging.info("\n~~~~ start set ~~~~")
                logging.info(start_set)

                for package in start_set:
                    #try:
                    link = comar.Link()
                    link.System.Service[package].start()
                    #message.reply("service.start.status", "Successful")
                    #except DBusException, e:
                    #message.reply("service.start.status", str(e))

        if "serviceStop" in message.policy:
            stop_set = []
            for packages in message.policy["serviceStop"]:

                try:
                    for package in packages.split(","):
                        stop_set.append(package)
                except ValueError:
                    stop_set = []
                    break

                logging.info("\n~~~~ stop set ~~~~")
                logging.info(stop_set)

                for package in stop_set:
                    #try:
                    link = comar.Link()
                    link.System.Service[package].stop()
                    #message.reply("service.stop.status", "Successful")
                    #except DBusException, e:
                    #message.reply("service.stop.status", str(e))


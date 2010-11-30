#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import logging
import os

SERVICE_DIR = "/etc/ahenk/webservices/"

def get_services():
    if not os.path.exists(SERVICE_DIR):
        return {}
    services = {}
    for filename in os.listdir(SERVICE_DIR):
        if filename.startswith("."):
            continue
        try:
            data = file(os.path.join(SERVICE_DIR, filename)).read()
        except:
            continue
        services[filename] = data.strip()
    return services

def process(message, options):
    """
        Policy/command processor.

        Arguments:
            message: Message object
            options: Options
    """

    dryrun = options.dryrun

    if message.type == "command":
        if message.command == "apache.info":
            args = get_services()
            message.reply("apache.info", args)

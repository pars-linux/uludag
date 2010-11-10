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
        data = file(os.path.join(SERVICE_DIR, filename)).read()
        services[filename] = data.strip()
    return services

def process(message, dryrun=False):
    if message.type == "command":
        if message.command == "apache.info":
            args = get_services()
            message.reply("apache.info", args)

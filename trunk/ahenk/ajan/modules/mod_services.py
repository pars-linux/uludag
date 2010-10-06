#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import logging

# COMAR
import comar


def process(message, dryrun=False):
    if message.type == "command":
        if message.command == "service.info":
            link = comar.Link()
            args = []
            for package in link.System.Service:
                type_, desc_, status_ = link.System.Service[package].info()
                args.append((package, desc_, status_))
            message.reply("service.info", args)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

def process(message, dryrun=False):
    if message.type == "command":
        message.reply("You said: %s" % message.command)

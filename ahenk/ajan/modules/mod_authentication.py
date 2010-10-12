#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import logging

# Ahenk
from ahenk.agent import utils


def process(message, dryrun=False):
    """
        Policy/command processor.

        Arguments:
            message: Message object
            dryrun: True, if "do nothing, just say" mode is on
    """
    if message.type == "policy":
        if "authenticationType" in message.policy:
            authenticationType = message.policy.get("authenticationType", "unix")[0]
            logging.info("Authentication: Source is %s" % authenticationType)

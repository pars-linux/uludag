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
        if "firewallState" in message.policy:
            firewallState = message.policy.get("firewallState", ["off"])[0]
            firewallRules = message.policy.get("firewallRules", [""])[0]
            if firewallState == "on":
                logging.info("Firewall: IPTables service is running.")
            elif firewallState == "off":
                logging.info("Firewall: IPTables service is not running.")

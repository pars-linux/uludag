#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import base64
import bz2
import logging
import os
import tempfile

# COMAR
import comar

# Ahenk
from ahenk.agent import utils


def enable_firewall(rules, options, first=False):
    dryrun = options.dryrun

    script_path = os.path.join(options.policydir, "firewall.sh")

    if rules:
        rules = rules.split(":")[1]
        rules = base64.decodestring(rules)
        rules = bz2.decompress(rules)

        fp = file(script_path, 'w')
        fp.write(rules)
        fp.close()

        if not dryrun:
            if first:
                os.system("/bin/bash %s stop" % script_path)
            os.system("/bin/bash %s start" % script_path)

        logging.info("Firewall: IPTables service is running.")

def disable_firewall(options):
    dryrun = options.dryrun

    script_path = os.path.join(options.policydir, "firewall.sh")

    if not dryrun:
        if os.path.exists(script_path):
            os.system("/bin/bash %s stop" % script_path)

    logging.info("Firewall: IPTables service is not running.")

def process(message, options):
    """
        Policy/command processor.

        Arguments:
            message: Message object
            options: Options
    """

    dryrun = options.dryrun

    if message.type == "policy":
        stack = message.policy_stack
        stack.reverse()
        first = True
        for policy in stack:
            firewallState = policy.get("firewallState", [""])[0]
            firewallRules = policy.get("firewallRules", [""])[0]
            if firewallState == "on":
                enable_firewall(firewallRules, options, first)
            elif firewallState == "off" and first:
                disable_firewall(options)
            first = False

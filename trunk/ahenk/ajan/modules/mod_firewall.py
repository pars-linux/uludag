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


def enable_firewall(rules, options):
    dryrun = options.dryrun

    script_path = os.path.join(options.policydir, "firewall.sh")

    if not dryrun:
        link = comar.Link()
        link.System.Service['iptables'].start()
        link.System.Service['iptables'].setState('on')

    if rules:
        rules = rules.split(":")[1]
        rules = base64.decodestring(rules)
        rules = bz2.decompress(rules)

        fp = file(script_path, 'w')
        fp.write(rules)
        fp.close()

        if not dryrun:
            os.system("/bin/bash %s start" % script_path)

        logging.info("Firewall: IPTables service is running.")

def disable_firewall(options):
    dryrun = options.dryrun

    script_path = os.path.join(options.policydir, "firewall.sh")

    if not dryrun:
        if os.path.exists(script_path):
            os.system("/bin/bash %s stop" % script_path)

        link = comar.Link()
        link.System.Service['iptables'].stop()
        link.System.Service['iptables'].setState('off')

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
        if "firewallState" in message.policy:
            firewallState = message.policy.get("firewallState", ["off"])[0]
            firewallRules = message.policy.get("firewallRules", [""])[0]
            if firewallState == "on":
                enable_firewall(firewallRules, options)
            elif firewallState == "off":
                disable_firewall(options)

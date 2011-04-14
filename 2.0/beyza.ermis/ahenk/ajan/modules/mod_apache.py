#!/usr/bin/python
# -*- coding: utf-8 -*-

def process(message, options):
    """
        Policy/command processor.

        Arguments:
            message: Message object
            options: Options
    """

    dryrun = options.dryrun

    if message.type == "policy":
        apacheDomains = message.policy.get("apacheDomains", [])
        print "Domainler:", apacheDomains

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import logging

# Ahenk
from ahenk.agent import utils


def process(message, options):
    """
        Policy/command processor.

        Arguments:
            message: Message object
            options: Options
    """

    dryrun = options.dryrun

    if message.type == "policy":
        if "authenticationType" in message.policy:
            authenticationType = message.policy.get("authenticationType", ["unix"])[0]
            # UNIX database
            if authenticationType == "unix":
                logging.info("Authentication: Using UNIX password database.")
                if not dryrun:
                    os.system("ahenk_authentication --type unix")
            # LDAP database
            elif authenticationType == "ldap":
                authenticationDomainLDAP = message.policy.get("authenticationDomainLDAP", [""])[0]
                authenticationHostLDAP = message.policy.get("authenticationHostLDAP", [""])[0]
                if authenticationHostLDAP and authenticationDomainLDAP:
                    logging.info("Authentication: Using LDAP domain %s on %s" % (authenticationDomainLDAP, authenticationHostLDAP))
                    if not dryrun:
                        os.system("ahenk_authentication --type=ldap --host=%s --domain=%s" % (authenticationHostLDAP, authenticationDomainLDAP))
            # Active Directory database
            elif authenticationType == "ad":
                authenticationDomainAD = message.policy.get("authenticationDomainAD", [""])[0]
                authenticationHostAD = message.policy.get("authenticationHostAD", [""])[0]
                if authenticationHostAD and authenticationDomainAD:
                    logging.info("Authentication: Using Active Directory domain %s on %s" % (authenticationDomainAD, authenticationHostAD))
                    if not dryrun:
                        pass

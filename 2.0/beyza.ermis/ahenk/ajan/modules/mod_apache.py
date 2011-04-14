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

        documentRoot = message.policy.get("documentRoot", [])
        print "Root:", documentRoot

        ip = message.policy.get("ip", [])
        print "IP:", ip

        port = message.policy.get("port", [])
        print "Port:", port

        serverAdmin = message.policy.get("serverAdmin", [])
        print "Server Admin:", serverAdmin

        serverName = message.policy.get("serverName", [])
        print "Server Name:", serverName

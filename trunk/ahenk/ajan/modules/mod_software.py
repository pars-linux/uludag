#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time

def process(message, dryrun=False):
    if message.type == "policy":
        if message.first_run:
            init(message)
        else:
            logging.debug("New policy: %s" % message.policy)
        repositories = []
        if "softwareRepositories" in message.policy:
            for i in message.policy["softwareRepositories"][0].split(","):
                logging.debug("Repository: %s" % i)

def init(message):
    logging.debug("Initializing PiSi: %s" % message.policy)

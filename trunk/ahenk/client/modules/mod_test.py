#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

def updatePackages():
    logging.debug("Updating!")

def timers():
    return {
        "updatePackages": (updatePackages, 30),
    }

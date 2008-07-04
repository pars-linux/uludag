#!/usr/bin/python
# -*- coding: utf-8 -*-
"""COMAR stuff for finger-manager"""
from os import path

datadir = "/var/lib/pyfinger/" #data directory, with trailing slash

#FIXME: what are we supposed to return?

def getPrintStatus(uid):
    """Check if user has a fignerprint or not."""
    if (type(uid) != int):
        return "uid must be an int"
    return (path.exists(datadir + str))

def saveFprint(fprintdata, uid):
    """Save fingerprint data for given uid.
    Data is saved under datadir/uid/fpdata.
    Make sure data dir is not readable by common users."""
    if (type(uid) != int):
        return "uid must be an int."
    if (type(fprintdata) != str):
        return "fprintdata must be in serialized string format."
    try:
        datafile = open(datadir + str(uid), "w")
        datafile.write(fprintdata)
    except:
        return "Write failed."
    datafile.close()

def loadFprint(uid):
    """Load fingerprint data for given uid.
    See saveFprint() for more details."""
    if (type(uid) != int):
        return "uid must be an int."
    try:
        datafile = open(datadir+str(uid), "r")
        fprintdata = datafile.read()
    except:
        return "Read failed."
    datafile.close()
    return fprintdata


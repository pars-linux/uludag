#!/usr/bin/python
# -*- coding: utf-8 -*-
"""COMAR stuff for finger-manager"""

datadir = "/var/lib/pyfinger/"

#FIXME: what are we supposed to return?

def saveFprint(fprintdata, uid):
    """Save fingerprint data for given uid.
    Data is saved under datadir/uid/fpdata.
    Make sure data dir is not readable by common users."""
    if (type(uid) != int):
        return "uid must be an int."
    if (type(fprintdata) != str):
        return "fprintdata must be in serialized string format."
    datafile = open(datadir + str(uid), "w")
    datafile.write(fprintdata)
    datafile.close()

def loadFprint(uid):
    """Load fingerprint data for given uid.
    See saveFprint() for more details."""
    if (type(uid) != int):
        return "uid must be an int."
    datafile = open(datadir+str(uid), "r")
    fprintdata = datafile.read()
    datafile.close()
    return fprintdata


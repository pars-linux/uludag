#!/usr/bin/python
# -*- coding: utf-8 -*-
"""COMAR stuff for finger-manager"""
import os, os.path as path

datadir = "/var/lib/pyfinger/" #data directory, w/ trailing slash
fpname = "fpdata" #name for fingerprint data files
imgname = "img" #name for image files

def getPrintStatus(uid):
    """Check if user has a fingerprint or not."""
    return (path.exists(path.join(datadir, str(uid))))

def saveFprint(fprintdata, uid):
    """Save fingerprint data for given uid.
    Data is saved under datadir/uid/fpdata.
    Make sure data dir is not readable by common users."""
    if (type(fprintdata) != str):
        return False #data must be string
    filename = path.join(datadir, str(uid))
    if not path.exists(filename):
        os.makedirs(filename)
    try:
        datafile = open(path.join(filename, fpname) , "w")
        datafile.write(fprintdata)
    except:
        return False #Write failed.
    datafile.close()

def loadFprint(uid):
    """Load fingerprint data for given uid.
    See saveFprint() for more details."""
    if (type(uid) != int):
        return False #uid must be an int.
    filename = path.join(datadir, str(uid))
    try:
        datafile = open(path.join(filename + fpname), "r")
        fprintdata = datafile.read()
    except:
        return False #Read failed.
    datafile.close()
    return fprintdata


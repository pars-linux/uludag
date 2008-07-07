#!/usr/bin/python
# -*- coding: utf-8 -*-
"""COMAR stuff for finger-manager"""
import os, os.path as path

datadir = "/var/lib/pyfinger/" #data directory, w/ trailing slash
fpname = "fpdata" #name for fingerprint data files
imgname = "img" #name for image files

#FIXME: Catch more specific exceptions?
#TODO: should printstatus() check for image too? maybe separate function?

def printstatus(uid):
    """Check if user has a fingerprint or not.
    Does not check for image, as it is not always needed."""
    return (path.exists(path.join(datadir, str(uid), fpname)))

def savedata(fprintdata, imgdata, uid):
    """Save fingerprint data for given uid.
    Data is saved under datadir/uid/fpdata.
    Make sure data dir is not readable by common users."""
    if (type(uid) != int):
        return False #uid must be an int.
    if (type(fprintdata) != str):
        return False #data must be string
    writepath = path.join(datadir, str(uid))
    try:
        if not path.exists(writepath):
            os.makedirs(writepath)
        #Write our stuff
        fpdatafile = open(path.join(writepath, fpname), "w")
        fpdatafile.write(fprintdata)
        imgdatafile = open(path.join(writepath, imgname), "w")
        imgdatafile.write(imgdata)
    except:
        return False #Write failed.
    fpdatafile.close()
    imgdatafile.close()

def loaddata(uid):
    """Load fingerprint data for given uid.
    See savedata() for more details."""
    if (type(uid) != int):
        return False #uid must be an int.
    writepath = path.join(datadir, str(uid))
    try:
        fpdatafile = open(path.join(writepath, fpname), "r")
        fprintdata = fpdatafile.read()
        imgdatafile = open(path.join(writepath, imgname), "r")
        imgdata = fpdatafile.read()
    except:
        return False #Read failed.
    fpdatafile.close()
    imgdatafile.close()
    return (fprintdata, imgdata)

def eraseFprint(uid):
    """Erase fingerprint data for given uid.
    See savedata() for more details."""
    if (type(uid) != int):
        return False #uid must be an int.
    fppath = path.join(datadir, str(uid), fpname)
    imgpath = path.join(datadir, str(uid), imgname)
    if path.exists(fppath):
        os.remove(fppath)
    if path.exists(imgpath):
        os.remove(imgpath)


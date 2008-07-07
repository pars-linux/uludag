#!/usr/bin/python
# -*- coding: utf-8 -*-
"""COMAR stuff for finger-manager"""
import os, os.path as path

datadir = "/var/lib/finger-manager/" #data directory, w/ trailing slash
fpname = "fpdata" #name for fingerprint data files
imgname = "fpimg" #name for image files

#FIXME: Catch more specific exceptions?
#TODO: should printstatus() check for image too? maybe separate function?

def getStatus(uid):
    """Check if user has a fingerprint or not.
    Does not check for image, as it is not always needed."""
    return (path.exists(path.join(datadir, str(uid), fpname)))

def saveData(uid, fprintdata, imgdata):
    """Save fingerprint data for given uid.
    Data is saved under datadir/uid/fpdata.
    If no image is available, a blank string must be supplied.
    Make sure data dir is not readable by common users."""
    if (not uid) or (not fprintdata) or (not imgdata):
        return False
    writepath = path.join(datadir, uid)
    print writepath
    try:
        if not path.exists(writepath):
            os.makedirs(writepath)
        #Write our stuff
        fpdatafile = open(path.join(writepath, fpname), "w")
        fpdatafile.write(fprintdata)
        imgdatafile = open(path.join(writepath, imgname), "w")
        imgdatafile.write(imgdata)
    except IOError, (errno, strerror):
        print "I/O error(%s): %s" % (errno, strerror)
    except:
        return False #Write failed.
    fpdatafile.close()
    imgdatafile.close()
    return True

def loadData(uid):
    """Load fingerprint data for given uid.
    See savedata() for more details."""
    writepath = path.join(datadir, str(uid))
    if not uid:
        return False
    try:
        fpdatafile = open(path.join(writepath, fpname), "r")
        fprintdata = fpdatafile.read()
        imgdatafile = open(path.join(writepath, imgname), "r")
        imgdata = imgdatafile.read()
    except:
        return False #Read failed.
    fpdatafile.close()
    imgdatafile.close()
    return (fprintdata, imgdata)

def eraseData(uid):
    """Erase fingerprint data for given uid.
    See savedata() for more details."""
    if not uid:
        return False
    fppath = path.join(datadir, str(uid), fpname)
    imgpath = path.join(datadir, str(uid), imgname)
    try:
        if path.exists(fppath):
            os.remove(fppath)
        if path.exists(imgpath):
            os.remove(imgpath)
    except:
        return False

    return True

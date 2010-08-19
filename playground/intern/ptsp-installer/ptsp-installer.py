#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api

PackageList=["dhcp", \
             "tftp", \
             "ltspfs", \
             "perl-X11-Protocol", \
             "ptsp-server"]

def CheckPackages():

    print "-"*30
    print "Checking for required packages.\n"
    PackageNotFound = False
    for package in PackageList:
        try:
            api.list_installed().index(package)
        except:
            print "Missing package: %s" % package
            PackageNotFound = True

    if PackageNotFound:
        print "\nInstall missing packages and try again."
        print "-"*30 + "\n"
        #TODO: Terminate Script
    else:
        print "Check Successful."
        print "-"*30 + "\n"

if __name__ == "__main__":
    CheckPackages()

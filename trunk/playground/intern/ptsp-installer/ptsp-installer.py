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
    print "Checking for required Packages.\n"
    PackageNotFound = False
    for package in PackageList:
        print "Checking for Package: %s --> " % package,
        try:
            api.list_installed().index(package)
            print "OK"
        except:
            print "Not Found"
            PackageNotFound = True

    if PackageNotFound:
        print "\nInstall missing packages and try again."
        print "-"*30 + "\n"
        raise SystemExit

    else:
        print "Check Successful."
        print "-"*30 + "\n"

if __name__ == "__main__":
    CheckPackages()

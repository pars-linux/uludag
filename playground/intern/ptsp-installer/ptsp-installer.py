#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api
from comar import service

PackageList = ["dhcp", \
               "tftp", \
               "ltspfs", \
               "perl-X11-Protocol", \
               "ptsp-server"]

ServicesList = ["dhcpd", \
                "tftpd", \
                "nfs-utils", \
                "portmap"]

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
        print "\nCheck Successful."
        print "-"*30 + "\n"

def StartServices():

    #FIXME: Failed to start services.
    try:
        for curservice in ServicesList:
            if not service.isServiceRunning('%s' % curservice):
                service.startService('%s' % curservice)
    except:
        print "Failed to start %s service" % curservice
        raise SystemExit

def CreateNetworkProfile(ip, netmask, gateway):
    #FIXME: Unable to import comar.network
    pass

if __name__ == "__main__":

    CheckPackages()

#    if raw_input("Do you want to create new network profile \
#or use an existing one[Y/N]: ") == 'Y':
#        ip = raw_input("Enter Ip Address: ")
#        netmask = raw_input("Enter Netmask Address: ")
#        gateway = raw_input("Enter Gateway Address: ")
#        CreateNetworkProfile(ip, netmask, gateway)

#    StartServices()

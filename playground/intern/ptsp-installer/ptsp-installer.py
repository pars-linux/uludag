#!/usr/bin/python
# -*- coding: utf-8 -*-

from pisi import api
import comar
import shutil

PackageList = ["dhcp", \
               "tftp", \
               "ltspfs", \
               "perl-X11-Protocol", \
               "ptsp-server"]

ServicesList = ["dhcpd", \
                "tftpd", \
                "nfs-utils", \
                "portmap"]


import re

def setKey(section, key, value, rc):
    sectionEscaped = re.escape(section)

    if not re.compile('^%s$' % sectionEscaped, re.MULTILINE).search(rc):
        print "setKey failed, '%s' section not found in kdmrc." % section
        return False

    result = re.compile('^%s=(.*)$' % key, re.MULTILINE)
    if result.search(rc):
        return result.sub('%s=%s' % (key, value), rc)

    result = re.compile('^#%s=(.*)$' % key, re.MULTILINE)
    if result.search(rc):
        return result.sub('%s=%s' % (key, value), rc)

    # If key can not be found, insert key=value right below the section
    return re.compile('^%s$' % sectionEscaped, re.MULTILINE).sub("%s\n%s=%s" % \
                                                            (section, key, value), rc)

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

def KdmrcUpdate():

    KdmrcPath = "/etc/X11/kdm/kdmrc"
    fp = open(KdmrcPath, "r")
    import ConfigParser
    KdmrcConfig = ConfigParser.ConfigParser()
    KdmrcConfig.readfp(fp)
    if KdmrcConfig.get("Xdmcp", "Enable") == "true":
        print "Kdmrc is OK, no need for update this file."
        return

    shutil.copyfile(KdmrcPath, "%s.orig" % KdmrcPath)
    KdmrcFile = fp.read()
    NewKdmrcFile = setKey("[Xdmcp]", "Enable", "true", KdmrcFile)
    fp.close()
    if not NewKdmrcFile:
        print "Error while updating kdmrc file"
        shutil.copyfile("%s.orig" % KdmrcPath, KdmrcPath)
        raise SystemExit

    fp = open("/etc/X11/kdm/kdmrc", "w")
    fp.writelines(NewKdmrcFile)
    fp.close()

    print "Kdmrc has successfully updated. Please restart X server \
to apply changes.\n"

def StartServices():

    try:
        for curservice in ServicesList:
            pass
            #TODO: Start services, stop it if service is running

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
    KdmrcUpdate()

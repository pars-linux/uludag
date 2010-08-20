#!/usr/bin/python
# -*- coding: utf-8 -*-
""" PTSP installer script """


from pisi import api
import comar
import shutil

PACKAGE_LIST = ["dhcp", \
               "tftp", \
               "ltspfs", \
               "perl-X11-Protocol", \
               "ptsp-server"]

SERVICE_LIST = ["dhcp", \
                "tftp", \
                "nfs-utils", \
                "portmap"]


import re

def set_key(section, key, value, file_content):
    """ Function to set key in configuration files. """
    section_escaped = re.escape(section)

    if not re.compile('^%s$' % section_escaped, re.MULTILINE).\
            search(file_content):
        print "setKey failed, '%s' section not found in kdmrc." % section
        return False

    result = re.compile('^%s=(.*)$' % key, re.MULTILINE)
    if result.search(file_content):
        return result.sub('%s=%s' % (key, value), file_content)

    result = re.compile('^#%s=(.*)$' % key, re.MULTILINE)
    if result.search(file_content):
        return result.sub('%s=%s' % (key, value), file_content)

    # If key can not be found, insert key=value right below the section
    return re.compile('^%s$' % section_escaped, re.MULTILINE)\
            .sub("%s\n%s=%s" % (section, key, value), file_content)

def check_packages():
    """ Function to check packages, if they aren't installed, \
terminate script. """

    print "-"*30
    print "Checking for required Packages.\n"
    package_not_found = False
    for package in PACKAGE_LIST:
        print "Checking for Package: %s --> " % package,
        try:
            api.list_installed().index(package)
            print "OK"
        except:
            print "Not Found"
            package_not_found = True

    if package_not_found:
        print "\nInstall missing packages and try again."
        print "-"*30 + "\n"
        raise SystemExit

    else:
        print "\nCheck Successful."
        print "-"*30 + "\n"

def kdmrc_update():
    """ Updates kdmrc file. """

    kdmrc_path = "/etc/X11/kdm/kdmrc"
    file_pointer = open(kdmrc_path, "r")
    import ConfigParser
    kdmrc_config = ConfigParser.ConfigParser()
    kdmrc_config.readfp(file_pointer)
    if kdmrc_config.get("Xdmcp", "Enable") == "true":
        print "Kdmrc is OK, no need for update this file.\n"
        return

    shutil.copyfile(kdmrc_path, "%s.orig" % kdmrc_path)
    kdmrc_file = file_pointer.read()
    new_kdmrc_file = set_key("[Xdmcp]", "Enable", "true", kdmrc_file)
    file_pointer.close()
    if not new_kdmrc_file:
        print "Error while updating kdmrc file"
        shutil.copyfile("%s.orig" % kdmrc_path, kdmrc_path)
        raise SystemExit

    file_pointer = open("/etc/X11/kdm/kdmrc", "w")
    file_pointer.writelines(new_kdmrc_file)
    file_pointer.close()

    print "Kdmrc has successfully updated. Please restart X server \
to apply changes.\n"

def start_services():
    """ Start necessary services. """

    link = comar.Link()
    try:
        for service in SERVICE_LIST:
            if link.System.Service[service].info()[2].find("on") != -1 or \
                link.System.Service[service].info()[2].find("started") != -1:
                link.System.Service[service].stop()
            link.System.Service[service].start()

            print "Service: %s has successfully started.\n" % service

    except:
        print "Failed to start %s service" % service
        raise SystemExit

def create_network_profile(ip, netmask, gateway):
    """ Create a network profile to use. """
    #FIXME: Unable to import comar.network
    pass

if __name__ == "__main__":

    check_packages()

#    if raw_input("Do you want to create new network profile \
#or use an existing one[Y/N]: ") == 'Y':
#        ipaddr = raw_input("Enter Ip Address: ")
#        netmask = raw_input("Enter Netmask Address: ")
#        gateway = raw_input("Enter Gateway Address: ")
#        create_network_profile(ipaddr, netmask, gateway)

    kdmrc_update()
    start_services()

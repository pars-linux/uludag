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



def set_key(section, key, value, file_content):
    """ Function to set key in configuration files. """

    import re

    section_escaped = re.escape(section)

    if not re.compile('^%s$' % section_escaped, re.MULTILINE).\
            search(file_content):
        print "set_key failed, '%s' section not found in kdmrc." % section
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

def update_kdmrc():
    """ Updates kdmrc file. """

    kdmrc_path = "/etc/X11/kdm/kdmrc"
    shutil.copyfile(kdmrc_path, "%s.orig" % kdmrc_path)
    file_pointer = open(kdmrc_path, "r")
    import ConfigParser
    kdmrc_config = ConfigParser.ConfigParser()
    kdmrc_config.readfp(file_pointer)
    if kdmrc_config.get("Xdmcp", "Enable") == "true":
        print "Kdmrc is OK, no need for update this file.\n"
        return

    file_pointer.seek(0)
    kdmrc_file = file_pointer.read()
    new_kdmrc_file = set_key("[Xdmcp]", "Enable", "true", kdmrc_file)
    file_pointer.close()
    if not new_kdmrc_file:
        print "Error while updating kdmrc file"
        shutil.copyfile("%s.orig" % kdmrc_path, kdmrc_path)
        raise SystemExit

    file_pointer = open(kdmrc_path, "w")
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

def select_network_device():
    i = 1
    print "Select a Network Device to use"
    link = comar.Link()
    info = link.Network.Link["net_tools"].linkInfo()
    devices = link.Network.Link["net_tools"].deviceList().values()
    if len(devices) > 0:
        print "%s devices" % info["name"]
        for d in devices:
            print "[%s]  %s" % (i, d)
            i=i+1
    selected_device = input("Device: ")
    return devices[selected_device-1]

def select_network_profile():
    """ Show network profile to use. """

    link = comar.Link()
    device = select_network_device()
    if device in link.Network.Link["net_tools"].deviceList():
        for connection in link.Network.Link["net_tools"].connections():
            info = link.Network.Link["net_tools"].connectionInfo(connection)
            #TODO: List Network Profiles and Select one of them.

def firefox_pixmap():
    """ This function disables firefox's image optimization. """

    try:
        file_pointer = open("/etc/env.d/11MozillaFirefoxPixmap", "w")
        file_pointer.write("MOZ_DISABLE_IMAGE_OPTIMIZE=1")
        file_pointer.close()
        print "Disabled Firefox's Image Optimization.\n"

    except:
        print "Failed to write Firefox Pixmap file.\n"
        raise SystemExit

def update_exports(server_gateway, server_netmask):
    """ Updates /etc/exports file. """

    try:
        shutil.copyfile("/etc/exports", "/etc/exports.orig")
        file_pointer = open("/etc/exports", "a")
        file_pointer.write("\n#This line is for PTSP server.\n\
/opt/ptsp \t\t%s/%s(ro,no_root_squash,sync)" % (server_gateway, server_netmask))
        file_pointer.close()
        print "Updated exports file.\n"

    except:
        print "Failed to update exports file.\n"
        raise SystemExit

def update_hosts(server_ip, client_name, number_of_clients):
    """ Updates /etc/hosts file. """

    try:
        shutil.copyfile("/etc/hosts", "/etc/hosts.orig")
        file_pointer = open("/etc/hosts", "a")
        file_pointer.write("\n#This lines are for PTSP server.\n")

        ip_mask = server_ip[0:server_ip.rfind(".")]
        add_last = int(server_ip[server_ip.rfind(".")+1:]) + 1

        for i in range(number_of_clients):
            file_pointer.write("%s.%s\t\t\t\t%s%s\n" % (ip_mask, add_last+i, \
                    client_name, i+1))

        file_pointer.close()
        print "Updated hosts file.\n"

    except:
        print "Failed to update hosts file.\n"
        raise SystemExit


if __name__ == "__main__":

    check_packages()

#    create_profile = raw_input("Do you want to create new network profile \
#or use an existing one[Y/N]: ")
#    if create_profile  == 'Y' or create_profile == 'y':
#        ipaddr = raw_input("Enter Ip Address: ")
#        netmask = raw_input("Enter Netmask Address: ")
#        gateway = raw_input("Enter Gateway Address: ")
#        nameserver = raw_input("Nameserver Address (write 'default' to use \
#default nameservers) : ")

#    elif create_profile == 'N' or create_profile == 'n':
#        select_network_profile()

    update_kdmrc()

    #TODO: Get server_ip, network_gateway and network_netmask
    #from COMAR after selecting network profie
    server_ip = "10.0.0.1"
    network_gateway = "10.0.0.0"
    network_netmask = "255.255.255.0"

    update_exports(network_gateway, network_netmask)

    client_name = raw_input("Please enter Client's name: ")
    number_of_clients = input("Please enter number of clients: ")

    update_hosts(server_ip, client_name, number_of_clients)

    firefox_pixmap()

    start_services()

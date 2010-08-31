#!/usr/bin/python
# -*- coding: utf-8 -*-
""" PTSP installer script """


from pisi import api
import comar
import shutil
import ConfigParser

PACKAGE_LIST = ["dhcp", \
               "tftp", \
               "ltspfs", \
               "perl-X11-Protocol", \
               "ptsp-server"]

SERVICE_LIST = ["dhcp", \
                "tftp", \
                "nfs-utils", \
                "portmap"]

def set_key(section, key, value, file_content, white_spaces="false"):
    """ Function to set key in configuration files. """

    import re

    section_escaped = re.escape(section)

    if white_spaces:
        if not re.compile('^%s$' % section_escaped, re.MULTILINE).\
                search(file_content):
            print "set_key failed, '%s' section not found in kdmrc." % section
            return False

        result = re.compile('^%s = (.*)$' % key, re.MULTILINE)
        if result.search(file_content):
            return result.sub('%s = %s' % (key, value), file_content)

        result = re.compile('^#%s = (.*)$' % key, re.MULTILINE)
        if result.search(file_content):
            return result.sub('%s = %s' % (key, value), file_content)

        # If key can not be found, insert key=value right below the section
        return re.compile('^%s$' % section_escaped, re.MULTILINE)\
                .sub("%s\n%s = %s" % (section, key, value), file_content)

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

    try:
        kdmrc_path = "/etc/X11/kdm/kdmrc"
        shutil.copyfile(kdmrc_path, "%s.orig" % kdmrc_path)
        file_pointer = open(kdmrc_path, "r")
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
            print "Error while updating kdmrc file.\n"
            shutil.copyfile("%s.orig" % kdmrc_path, kdmrc_path)
            raise SystemExit

        file_pointer = open(kdmrc_path, "w")
        file_pointer.writelines(new_kdmrc_file)
        file_pointer.close()

        print "Kdmrc has successfully updated. Please restart X server \
to apply changes.\n"

    except:

        print "Failed to update kdmrc file.\n"
        shutil.copyfile("%s.orig" % kdmrc_path, kdmrc_path)
        raise SystemExit

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
    """ Selects network device. """

    i = 1
    print "Select a Network Device to use"
    dev_list = []
    link = comar.Link()
    info = link.Network.Link["net_tools"].linkInfo()
    devices = link.Network.Link["net_tools"].deviceList()
    if len(devices) > 0:
        print "%s devices" % info["name"]
        for dev_id, dev_name in devices.iteritems():
            dev_list.append(dev_id)
            print "[%s]  %s" % (i, dev_name)
            i = i + 1
    selected_device = input("Device: ")
    return dev_list[selected_device-1]

def select_network_profile():
    """ Select network profile to use. """
    i = 1
    link = comar.Link()
    device = select_network_device()
    if device in link.Network.Link["net_tools"].deviceList():
        profile_list = link.Network.Link["net_tools"].connections()
        if len(profile_list) > 0:
            for profile in profile_list:
                profile_info = link.Network.Link["net_tools"].connectionInfo(profile)
                dev_name = profile_info["device_name"].split(" - ")[0]
                print "[%s] %s\t-\t%s" % (i, profile, dev_name)
                i = i + 1

        network_profile = input("Select a Profile: ")

    try:
        set_network_profile_state(network_profile-1, "up")
    except:
        print "Setting network profile to up failed.\n"

    return link.Network.Link["net_tools"].connectionInfo\
            (profile_list[network_profile-1])

def set_network_profile_state(profile_index, state):
    """ This function sets network profile state(up or down). """

    link = comar.Link()
    profile_list = link.Network.Link["net_tools"].connections()

    link.Network.Link["net_tools"].setState(profile_list[profile_index], state)

    if link.Network.Link["net_tools"].connectionInfo(profile_list[profile_index])\
            ["state"].find(state) != -1:
        print "Profile %s is %s!\n" % (profile_list[profile_index], state)

    else:
        print "Change state the Profile %s to %s is failed.\n" % \
                (profile_list[profile_index], state)

def create_network_profile():
    """ Function to create network profile. """

    try:
        link = comar.Link()
        profile = None
        profile_list = link.Network.Link["net_tools"].connections()

        device = select_network_device()

        while not profile:
            profile = raw_input("Network Profile Name: ")
            if profile in profile_list:
                print "There is already a profile named '%s'" % profile
                profile = None

        if profile == None:
            raise SystemExit

        print """\
Select IP Assignment Method:
[1] Enter an IP address manually
[2] Automatically obtain an IP Address
"""
        ip_selection = input("Method: ")
        if ip_selection == 1:
            ip_mode = "manual"
            server_address = raw_input("Ip Address: ")
            network_netmask = raw_input("Netmask Address: ")
            network_gateway = raw_input("Gateway Address: ")

        elif ip_selection == 2:
            ip_mode = "auto"
            server_address = ""
            network_netmask = ""
            network_gateway = ""

        else:
            print "Selection Error.\n"
            raise SystemExit

        print """\
Select Name server (DNS) assignment method:
[1] Use default name servers
[2] Enter an name server address manually
[3] Automatically obtain from DHCP
"""
        dns_selection = input("Method: ")

        if dns_selection == 1:
            dns_mode = "default"
            network_dns = ""

        elif dns_selection == 2:
            dns_mode = "manual"
            network_dns = raw_input("Enter Dns Address: ")

        elif dns_selection == 3:
            dns_mode = "auto"
            network_dns = ""

        else:
            print "Selection Error.\n"
            raise SystemExit

        link.Network.Link["net_tools"].setDevice(profile, device)

        link.Network.Link["net_tools"].setAddress(profile, ip_mode, server_address, \
                network_netmask, network_gateway)

        link.Network.Link["net_tools"].setNameService(profile, dns_mode, network_dns)

        network_profile = 0

        for _profile in profile_list:
            if link.Network.Link["net_tools"].connectionInfo(_profile) == profile:
                break
            network_profile = network_profile + 1

        try:
            set_network_profile_state((network_profile-1), "up")
        except:
            print "Activating the new network profile failed.\n"

        print "New network profile added successfully.\n"

        return link.Network.Link["net_tools"].connectionInfo(profile_list\
                [network_profile-1])

    except:
        print "Creating new network profile failed!\n"
        raise SystemExit

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

    exports_path = "/etc/exports"

    try:
        shutil.copyfile(exports_path, "%s.orig" % exports_path)
        file_pointer = open(exports_path, "r")
        orig_exports = file_pointer.readlines()
        file_pointer.close()
        new_exports = ""
        for line in orig_exports:
            if line.find("%s" % server_gateway) == -1 and \
                line.find("%s" % server_netmask) == -1 and \
                line.find("/opt/ptsp") == -1 and \
                line != "\n" and \
                line.find("#This line is for PTSP Server.") == -1:
                        new_exports = new_exports + line
        new_exports = new_exports + ("\n#This line is for PTSP Server.\n\
/opt/ptsp \t\t%s/%s(ro,no_root_squash,sync)\n" % (server_gateway, server_netmask))

        file_pointer = open(exports_path, "w")
        file_pointer.writelines(new_exports)
        file_pointer.close()

        print "Updated exports file.\n"

    except:
        print "Failed to update exports file.\n"
        shutil.copyfile("%s.orig" % exports_path, exports_path)
        raise SystemExit

def update_hosts(server_ip, client_name, number_of_clients):
    """ Updates /etc/hosts file. """

    hosts_path = "/etc/hosts"

    try:

        shutil.copyfile(hosts_path, "%s.orig" % hosts_path)

        ip_mask = server_ip[0:server_ip.rfind(".")]
        add_last = int(server_ip[server_ip.rfind(".")+1:]) + 1

        file_pointer = open(hosts_path, "r")
        orig_hosts = file_pointer.readlines()
        file_pointer.close()
        new_hosts = ""
        for line in orig_hosts:
            if line.find("#This lines are for PTSP Server.") == -1:
                ignore_line = False
                for i in range(number_of_clients):
                    if line.find("%s.%s" % (ip_mask, add_last+i)) != -1 and \
                            line.find("%s%s" % (client_name, i+1)) != -1:
                                ignore_line = True
                if not ignore_line:
                    new_hosts = new_hosts + line

        new_hosts = new_hosts +"\n#This lines are for PTSP Server.\n"
        for i in range(number_of_clients):
            #FIXME: Alignment problem
            new_hosts = new_hosts + "%s.%s\t\t\t\t%s%s\n" % \
                    (ip_mask, add_last+i, client_name, i+1)

        file_pointer = open(hosts_path, "w")
        file_pointer.writelines(new_hosts)
        file_pointer.close()

        print "Updated hosts file.\n"

    except:
        print "Failed to update hosts file.\n"
        shutil.copyfile("%s.orig" % hosts_path, hosts_path)
        raise SystemExit

def update_pts_client_conf(server_ip):
    """ Updates /opt/ptsp/etc/pts-client.conf file. """

    pts_client_conf_path = "/opt/ptsp/etc/pts-client.conf"

    try:

        shutil.copyfile(pts_client_conf_path, "%s.orig" % pts_client_conf_path)
        file_pointer = open(pts_client_conf_path, "r")
        pts_client_conf = ConfigParser.ConfigParser()
        pts_client_conf.readfp(file_pointer)
        if pts_client_conf.get("Server", "XSERVER") == server_ip:
            print "pts-client.conf is OK, no need for update this file.\n"
            file_pointer.close()
            return

        file_pointer.seek(0)
        pts_client_conf_file = file_pointer.read()
        new_pts_client_conf_file = set_key("[Server]", "XSERVER", \
                server_ip, pts_client_conf_file, white_spaces="true")
        file_pointer.close()

        if not new_pts_client_conf_file:
            print "Error while updating pts-client.conf file.\n"
            shutil.copyfile("%s.orig" % pts_client_conf_path, \
                    pts_client_conf_path)

        file_pointer = open(pts_client_conf_path, "w")
        file_pointer.writelines(new_pts_client_conf_file)
        file_pointer.close()

        print "Updated pts-client.conf file.\n"

    except:
        print "Failed to update pts-client.conf file.\n"
        shutil.copyfile("%s.orig" % pts_client_conf_path, \
                pts_client_conf_path)
        raise SystemExit

def update_dhcpd_conf(server_ip, network_gateway, network_netmask, \
                      number_of_clients):
    """ Updates /etc/dhcp/dhcpd.conf file. """

    dhcpd_conf_path = "/etc/dhcp/dhcpd.conf"

    try:

        shutil.copyfile(dhcpd_conf_path, "%s.orig" % dhcpd_conf_path)
        ip_mask = server_ip[0:server_ip.rfind(".")]
        add_last = int(server_ip[server_ip.rfind(".")+1:]) + 1

        file_pointer = open(dhcpd_conf_path, "r")
        orig_dhcpd_conf = file_pointer.readlines()
        file_pointer.close()
        new_dhcpd_conf = ""
        paranthesis = False
        for line in orig_dhcpd_conf:
            if line.find("#This lines are for PTSP Server.") == -1 and \
                line.find("%s:/opt/ptsp" % server_ip) == -1:
                    if line.find("subnet %s netmask %s {" % \
                        (network_gateway, network_netmask)) == -1:
                        paranthesis = True
                        if line.find("%s" % network_netmask) == -1 and \
                            line.find("%s.%s" % (ip_mask, add_last+\
                            number_of_clients)) == -1 and \
                            line.find("#send this file for pxe") == -1 and \
                            line.find("filename \"/pts/latest-ptsp") == -1:
                                if line.find("}") == -1 and not paranthesis:
                                    paranthesis = False
                                    new_dhcpd_conf = new_dhcpd_conf + line
        new_dhcpd_conf = new_dhcpd_conf + """
#This lines are for PTSP Server.
 option root-path      "%s:/opt/ptsp";
 subnet %s netmask %s {
     range %s  %s.%s;

     #send this file for pxe file requests
     filename "/pts/latest-ptsp/pxelinux.0";
 }
""" % (server_ip, network_gateway, network_netmask, server_ip, ip_mask, \
        add_last+number_of_clients)

        file_pointer = open(dhcpd_conf_path, "w")
        file_pointer.writelines(new_dhcpd_conf)
        file_pointer.close()

        print "Updated dhcpd.conf file.\n"

    except:

        print "Failed to update dhcpd.conf file.\n"
        shutil.copyfile("%s.orig" % dhcpd_conf_path, dhcpd_conf_path)
        raise SystemExit

if __name__ == "__main__":

    select = raw_input("Do you want to Check Packages?[Y/N]")
    if select == 'Y' or select == 'y':
        check_packages()

    select = raw_input("Do you want to make change with your network settings?[Y/N]")
    if select == 'Y' or select == 'y':

        create_profile = raw_input("Do you want to create new network profile \
or use existing one[Y/N]: ")

        if create_profile  == 'Y' or create_profile == 'y':
            profile_settings = create_network_profile()

        elif create_profile == 'N' or create_profile == 'n':
            profile_settings = select_network_profile()

        server_ip = profile_settings["net_address"]
        network_gateway = profile_settings["net_gateway"]
        network_netmask = profile_settings["net_mask"]

    client_name = raw_input("Please enter Client's name: ")
    number_of_clients = input("Please enter number of Clients: ")

    select = raw_input("Do you want to Update dhcpd.conf?[Y/N]")

    if select == 'Y' or select == 'y':
        update_dhcpd_conf(server_ip, network_gateway, network_netmask, \
            number_of_clients)

    select = raw_input("Do you want to Update kdmrc?[Y/N]")

    if select == 'Y' or select == 'y':
        update_kdmrc()

    select = raw_input("Do you want to Update exports?[Y/N]")

    if select == 'Y' or select == 'y':
        update_exports(network_gateway, network_netmask)


    select = raw_input("Do you want to Update hosts?[Y/N]")

    if select == 'Y' or select == 'y':
        update_hosts(server_ip, client_name, number_of_clients)

    select = raw_input("Do you want to Update pts-client.conf?[Y/N]")

    if select == 'Y' or select == 'y':
        update_pts_client_conf(server_ip)

    select = raw_input("Do you want to Disable Firefox Image Caching?[Y/N]")

    if select == 'Y' or select == 'y':
        firefox_pixmap()

    select = raw_input("Do you want to start Services?[Y/N]")

    if select == 'Y' or select == 'y':
        start_services()

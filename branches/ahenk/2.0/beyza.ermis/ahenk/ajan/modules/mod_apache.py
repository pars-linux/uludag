#!/usr/bin/python
# -*- coding: utf-8 -*-

import augeas
import os

MYROOT="/"

def find_next_file_prefix(path):
    max = 0

    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            try:
                current = int((filename.split("_"))[0])
                if current > max:
                    max = current
            except:
                pass

    if max < 10:
        return "0%s" % str(max + 1)
    else:
        return str(max + 1)


def add_virtual_host(vhost_config):
    """ Add new virtual host to apache config, vhosts.d directory """

    vhosts_config_path = "/etc/apache2/vhosts.d/"

    port = vhost_config["port"]
    ip = vhost_config["ip"]

    server_admin = vhost_config["serverAdmin"]
    document_root = vhost_config["documentRoot"]
    server_name = vhost_config["serverName"]

    # === FUTURE ===
    # Directory specific settings
    # Every directory must be held in a dictionary with the following properties
    #   path = directory["path"]
    #   allow_override = directory["allowOverride"]
    #   is_default_host = directory["isDefaultHost"]
    #   indexes = directory["indexes"]

    # Generate file name from server name
    prefix = find_next_file_prefix(vhosts_config_path)
    vhost_file_name = "%s_%s_vhosts.conf" % (prefix, server_name.replace(".", "_"))

    # Create configuration file if not exists
    vhost_path = "%s%s" % (vhosts_config_path, vhost_file_name)
    if not os.path.exists(vhost_path):
        vhost_file = open(vhost_path, "w").close()

    # Add vhosts.d to /usr/share/augeas/lenses/dist/httpd.aug

    config = augeas.Augeas(root=MYROOT)

    # Define vhost variable
    config.defvar("vhost", "/files%s" % vhost_path)

    # Add <VirtualHost></VirtualHost> if doesn't exists
    config.insert("$vhost", "VirtualHost")

    vhost_ip_port = "%s:%s" % (ip, port)
    config.set("$vhost/VirtualHost/arg", vhost_ip_port)

    # Add ServerAdmin
    config.set("$vhost/VirtualHost/directive[1]", "ServerAdmin")
    config.set("$vhost/VirtualHost/*[self::directive='ServerAdmin']/arg", server_admin)

    # Add DocumentRoot
    config.set("$vhost/VirtualHost/directive[2]", "DocumentRoot")
    config.set("$vhost/VirtualHost/*[self::directive='DocumentRoot']/arg", document_root)

    # Add ServerName
    config.set("$vhost/VirtualHost/directive[3]", "ServerName")
    config.set("$vhost/VirtualHost/*[self::directive='ServerName']/arg", server_name)

    config.save()


def process(message, options):
    """
        Policy/command processor.

        Arguments:
            message: Message object
            options: Options
    """

    dryrun = options.dryrun

    if message.type == "policy":
        apacheDomains = message.policy.get("apacheDomains", [])
        documentRoot = message.policy.get("documentRoot", [])
        ip = message.policy.get("ip", [])
        port = message.policy.get("port", [])
        serverAdmin = message.policy.get("serverAdmin", [])
        serverName = message.policy.get("serverName", [])

    vhost = { "port":port,
              "ip":ip,
              "serverAdmin":serverAdmin,
              "documentRoot":documentRoot,
              "serverName":serverName
            }


    add_virtual_host(vhost)

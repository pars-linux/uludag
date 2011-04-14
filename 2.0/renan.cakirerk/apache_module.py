#!/usr/bin/python
# -*- coding: utf-8 -*-

# Ahenk Apache Virtual Host Configuration
# Renan Cakirerk <renan at pardus.org.tr>

import augeas
import os

MYROOT="/"

def addVirtualHost(vhost_config):
    """ Add new virtual host to apache config, vhosts.d directory """

    vhosts_path = "/etc/apache2/vhosts.d/"

    config = augeas.Augeas(root=MYROOT)

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
    vhost_file_name = "01_%s_vhosts.conf" % server_name.replace(".", "_")

    # Create configuration file if not exists
    vhost_path = "%s%s" % (vhosts_path, vhost_file_name)
    if not os.path.exists(vhost_path):
        vhost_file = open(vhost_path, "w").close()

    # Add vhosts.d to /usr/share/augeas/lenses/dist/httpd.aug

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


if __name__ == "__main__":

    # Example vhost configuration
    vhost = { "port":"81",
              "ip":"192.168.1.1",
              "serverAdmin":"admin@bar.com",
              "documentRoot":"/var/www/localhost/htdocs/bar",
              "serverName":"foo.bar.com"
            }

    addVirtualHost(vhost)

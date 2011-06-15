# -*- coding: utf-8 -*-

"""
    ldap.conf parser. Example files use that module to read
    LDAP configuration.
"""

# Standard modules
import ConfigParser
import os

def parse():
    """
        Parses ldap.conf and returns connection settings.

        Returns:
            host: Server address
            domain: Domain name
            username: Account name
            password: Account password
    """

    filepath = os.path.dirname(__file__) + '/ldap.conf'

    cp = ConfigParser.ConfigParser()
    cp.read(filepath)

    host = cp.get('directory', 'host')
    domain = cp.get('directory', 'domain')
    username = cp.get('directory', 'username')
    password = cp.get('directory', 'password')

    return host, domain, username, password

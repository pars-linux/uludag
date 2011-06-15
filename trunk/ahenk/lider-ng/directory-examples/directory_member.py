#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Example application for editing LDAP access control lists.
"""

# Standard modules
import sys

# LDAP configuration
import ldap_conf

# Directory module
from directory import Connection


def main():
    """
        Example that lists current policies, and adds a dummy policy.
    """

    host, domain, username, password = ldap_conf.parse()

    domain = "dc=%s" % domain.replace(".", ",dc=")

    api = Connection()
    if not api.connect(host, domain):
        print 'Unable to connect to server'
        return -1

    if not api.login_simple(username, password):
        print 'Unable to login to server'
        return -1

    group = api.find_node_by_address('cn=group1,dc=example,dc=org')
    node = api.find_node_by_address('cn=user1,dc=example,dc=org')
    api.set_members(group, [node])

    return 0

if __name__ == '__main__':
    sys.exit(main())

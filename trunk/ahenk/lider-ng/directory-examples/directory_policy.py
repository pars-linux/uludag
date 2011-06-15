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
from directory import Connection, Policy


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

    if not api.enable_config(username, password):
        print "Server doesn't support dynamic configuration or access denied."
        return -1

    for policy in api.get_policies():
        if isinstance(policy, Policy):
            print 'Parsed policy: %s' % policy.to_pretty()
        else:
            # Complicated policies are kept as strings
            print 'Complex policy: %s' % policy
        print '-' * 20

    return 0

if __name__ == '__main__':
    sys.exit(main())

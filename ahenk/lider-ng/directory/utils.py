#!/usr/bin/python
# -*- coding: utf-8 -*-

def sanitize_ldap_address(address):
    """
        Sanitizes LDAP address.

        Arguments:
            address: LDAP address (dc = example,dc=org)
        Returns:
            Sanitized LDAP address (dc=example, dc=org)
    """
    parts = []
    for part in address.split(','):
        key, value = part.split('=')
        key = key.strip()
        value = value.strip()
        parts.append('%s=%s' % (key, value))
    return ', '.join(parts)

def get_ldap_domain(domain):
    """
        Converts a domain name to LDAP format.

        Arguments:
            domain: Domain name (test.example.org)
        Returns:
            LDAP domain name (dc=test, dc=example, dc=org)
    """
    parts = []
    for part in domain.split('.'):
        parts.append('dc=%s' % part)
    return ', '.join(parts)

def get_inet_domain(domain):
    """
        Converts a LDAP domain name to Internet domain format.

        Arguments:
            domain: LDAP Domain name (dc=test, dc=example, dc=org)
        Returns:
            LDAP domain name (test.example.org)
    """
    parts = []
    for part in domain.split(','):
        part = part.split('=')[1]
        part = part.strip()
        parts.append(part)
    return '.'.join(parts)

def get_ldap_name(user):
    """
        Picks username from LDAP node address.

        Arguments:
            user: LDAP user address (cn=admin, dc=example, dc=org)
        Returns:
            User name (admin)
    """
    return user.split(',')[0].split('=')[1]

def get_pattern(attributes):
    """
        Converts pattern dictionary to LDAP search pattern.

        Arguments:
            attributes: Dictionary for filtering like: {'cn': 'x', ...}
        Returns:
            Search pattern like: (&(cn=x)(...))
    """
    patterns = []
    for key in attributes:
        pattern = '(%s=%s)' % (key, attributes[key])
        patterns.append(pattern)
    return '(&%s)' % ''.join(patterns)

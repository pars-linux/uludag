#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Directory service helper utilities
"""

# LDAP modules
import ldap
import ldap.modlist


class DirectoryError(Exception):
    """
        Base exception class for directory server errors
    """
    pass

class Directory:
    """
        Directory service manager.

        Usage:
            dir = Directory()
            dir.connect("127.0.0.1", "directory.example.net", "admin", "password):
            print dir.get_name()
    """

    def __init__(self):
        """
            Constructor for directory service manager.
        """
        self.host = None
        self.domain = None
        self.user = None
        self.password = None
        self.directory_domain = None
        self.directory_user = None
        self.conn = None
        self.is_connected = False

    def connect(self, host, domain, user, password):
        """
            Connects to directory server.

            Arguments:
                host: Directory address
                domain: Directory root domain
                user: User name
                password: User password
        """
        self.host = host
        self.domain = domain
        self.user = user
        self.password = password

        self.directory_domain = "dc=" + domain.replace(".", ",dc=")
        self.directory_user = "cn=%s,%s" % (self.user, self.directory_domain)

        try:
            self.conn = ldap.open(self.host)
            self.conn.simple_bind_s(self.directory_user, self.password)
            self.is_connected = True
        except ldap.LDAPError:
            self.is_connected = False
            raise DirectoryError

    def get_name(self):
        """
            Gives directory name.

            Returns: Directory name.
        """
        pattern = "(objectClass=dcObject)"

        try:
            search = self.conn.search_s(self.directory_domain, ldap.SCOPE_BASE, pattern)
        except ldap.LDAPError:
            raise DirectoryError

        dn, attributes = search[0]

        if "o" in attributes:
            return attributes["o"][0]
        else:
            return ""

    def add_new(self, dn, attributes):
        """
            Adds new item

            Arguments:
                dn: Distinguished name
                attributes: Properties
        """
        ldif = ldap.modlist.addModlist(attributes)
        self.conn.add_s(dn, ldif)

    def search(self, directory=None, fields=None, scope="one"):
        """
            Searches for all Folder and Computer objects in given directory.

            Arguments:
                directory: Directory name
                fields: List of required fields
                scope: Search scope (base, one, sub)
            Returns: List of DN's
        """
        if not directory:
            directory = self.directory_domain

        results = []

        if scope == "base":
            scope = ldap.SCOPE_BASE
        elif scope == "one":
            scope = ldap.SCOPE_ONELEVEL
        elif scope == "sub":
            scope = ldap.SCOPE_SUBTREE

        print "Search:", directory
        pattern = "(|(objectClass=dcObject)(objectClass=pardusComputer))"
        for dn, attributes in self.conn.search_s(directory, scope, pattern, fields):
            results.append((dn, attributes,))

        return results

    def get_label(self, dn):
        """
            Returns label of a directory object.

            Arguments:
                dn: Distinguished name
            Returns:
                Object label, or common name.
        """
        if dn.startswith("dc="):
            dn, attrs = directory.search(directory.directory_domain, ["o"], "base")
            if "o" in attrs:
                label = attrs["o"][0]
            else:
                label = dn.split(",")[0].split("=")[1]
        else:
            label = dn.split(",")[0].split("=")[1]
        return label

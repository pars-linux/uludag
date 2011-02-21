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

class DirectoryConnectionError(DirectoryError):
    """
        Connection error class
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
            raise DirectoryConnectionError

    def disconnect(self):
        """
            Disconnects from server.
        """
        self.is_connected = False
        try:
            if self.conn:
                self.conn.unbind_s()
        except ldap.LDAPError:
            pass

    def get_name(self):
        """
            Gives directory name.

            Returns: Directory name.
        """
        pattern = "(objectClass=dcObject)"

        try:
            search = self.conn.search_s(self.directory_domain, ldap.SCOPE_BASE, pattern)
        except ldap.LDAPError:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError:
                raise DirectoryConnectionError
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

        items = []

        if scope == "base":
            scope = ldap.SCOPE_BASE
        elif scope == "one":
            scope = ldap.SCOPE_ONELEVEL
        elif scope == "sub":
            scope = ldap.SCOPE_SUBTREE

        pattern = "(|(objectClass=dcObject)(objectClass=pardusComputer)(objectClass=posixAccount))"
        try:
            results = self.conn.search_s(directory, scope, pattern, fields)
        except ldap.LDAPError:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError:
                raise DirectoryConnectionError
            raise DirectoryError
        for dn, attributes in results:
            items.append((dn, attributes,))

        return items

    def get_parent_paths(self, dn):
        """
            Returns a list of parent paths of the DN.

            Args:
                dn: Distinguished name
            Returns:
                List of parents, and self.
        """
        paths = []

        dn_parts = dn.split(",")
        for index in range(len(dn_parts)):
            part = ",".join(dn_parts[index:])
            if len(dn_parts) - index == self.directory_domain.count(","):
                break
            paths.append(part)
        paths.reverse()

        return paths

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

    def add_folder(self, parent_dn, name, label):
        """
            Adds a new folder under specified DN.

            Arguments:
                parent_dn: Distinguished name of parent
                name: Node name
                label: Node label
        """
        dn = "dc=%s,%s" % (name, parent_dn)
        properties = {
            "dc": [name],
            "objectClass": ["top", "dcObject", "organization"],
            "o": [label]
        }
        try:
            self.add_new(dn, properties)
        except ldap.LDAPError:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError:
                raise DirectoryConnectionError
            raise DirectoryError

    def add_computer(self, parent_dn, name, password):
        """
            Adds a new computer under specified DN.

            Arguments:
                parent_dn: Distinguished name of parent
                name: Node name
                password: Node password
        """
        dn = "cn=%s,%s" % (name, parent_dn)
        properties = {
            "cn": [name],
            "objectClass": ["top", "device", "pardusComputer"],
            "userPassword": [password]
        }
        try:
            self.add_new(dn, properties)
        except ldap.LDAPError:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError:
                raise DirectoryConnectionError
            raise DirectoryError

    def add_user(self, parent_dn, name, password, uid, gid, home=None):
        """
            Adds a new user under specified DN.

            Arguments:
                parent_dn: Distinguished name of parent
                name: Node name
                password: Node password
        """
        dn = "uid=%s,%s" % (name, parent_dn)
        if not home:
            home = "/home/%s" % name
        properties = {
            "uid": [name],
            "objectClass": ["top", "account", "posixAccount", "shadowAccount"],
            "cn": [name],
            "homeDirectory": [home],
            "uidNumber": [uid],
            "gidNumber": [gid],
            "userPassword": [password]
        }
        try:
            self.add_new(dn, properties)
            return dn
        except ldap.LDAPError:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError:
                raise DirectoryConnectionError
            raise DirectoryError

    def modify(self, dn, old, new):
        """
            Modifies attributes of a node.

            Arguments:
                dn: Distinguished name
                old: Old attributes
                new: New attributes
        """
        try:
            ldif = ldap.modlist.modifyModlist(old, new)
            self.conn.modify_s(dn, ldif)
        except ldap.LDAPError, e:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError, e:
                raise DirectoryConnectionError, e
            raise DirectoryError, e

    @staticmethod
    def make_password(password):
        import os
        salt = os.urandom(4)
        import hashlib
        sha = hashlib.sha1(password)
        sha.update(salt)
        import base64
        return '{SSHA}' + base64.encodestring(sha.digest() + salt)

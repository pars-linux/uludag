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

class DirectoryAccessError(DirectoryError):
    """
        Access error class
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

        try:
            self.conn = ldap.open(self.host)
        except ldap.LDAPError:
            self.is_connected = False
            raise DirectoryConnectionError

        try:
            pattern = "(cn=%s)" % self.user
            search = self.conn.search_s(self.directory_domain, ldap.SCOPE_SUBTREE, pattern, ['cn'])
            if len(search):
                self.directory_user = search[0][0]
            else:
                self.is_connected = False
                raise DirectoryConnectionError

        except ldap.LDAPError:
            self.is_connected = False
            raise DirectoryConnectionError


        try:
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

    def delete_item(self, dn):
        """
            Deletes selected item

            Arguments:
                dn: Distinguished name
        """
        self.conn.delete_s(dn)

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

        #pattern = "(|(objectClass=dcObject)(objectClass=pardusComputer)(objectClass=posixAccount)(objectClass=groupOfNames))"
        pattern = "(|(objectClass=dcObject)(objectClass=pardusComputer)(objectClass=posixAccount)(objectClass=simpleSecurityObject)(objectClass=groupOfNames))"
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

    def add_folder(self, parent_dn, name, label, description=""):
        """
            Adds a new folder under specified DN.

            Arguments:
                parent_dn: Distinguished name of parent
                name: Node name
                label: Node label
                description: LDAP attribute name
        """
        dn = "dc=%s,%s" % (name, parent_dn)
        properties = {
            "dc": [name],
            "objectClass": ["top", "dcObject", "organization"],
            "o": [label],
        }
        if len(description):
            properties["description"] = [description]
        try:
            self.add_new(dn, properties)
        except ldap.LDAPError, e:
            if "access" in e[0]["desc"]:
                raise DirectoryAccessError
            try:
                self.conn.whoami_s()
            except ldap.LDAPError, e:
                raise DirectoryConnectionError
            raise DirectoryError

    def add_computer(self, parent_dn, name, password, description=""):
        """
            Adds a new computer under specified DN.

            Arguments:
                parent_dn: Distinguished name of parent
                name: Node name
                password: Node password
                description: description
        """
        dn = "cn=%s,%s" % (name, parent_dn)
        properties = {
            "cn": [name],
            "objectClass": ["top", "device", "pardusComputer"],
            "userPassword": [password],
        }
        if len(description):
            properties["description"] = [description]
        try:
            self.add_new(dn, properties)
        except ldap.LDAPError, e:
            if "access" in e[0]["desc"]:
                raise DirectoryAccessError
            try:
                self.conn.whoami_s()
            except ldap.LDAPError:
                raise DirectoryConnectionError
            raise DirectoryError

    def add_user(self, parent_dn, name, password, description=""):
        """
            Adds a new user under specified DN.

            Arguments:
                parent_dn: Distinguished name of parent
                name: Node name
                password: Node password
        """
        dn = "cn=%s,%s" % (name, parent_dn)
        properties = {
            "cn": [name],
            "objectClass": ["organizationalRole", "simpleSecurityObject"],
            "userPassword": [password]
        }
        if len(description):
            properties["description"] = [description]
        try:
            self.add_new(dn, properties)
            return dn
        except ldap.LDAPError, e:
            if "access" in e[0]["desc"]:
                raise DirectoryAccessError
            try:
                self.conn.whoami_s()
            except ldap.LDAPError:
                raise DirectoryConnectionError
            raise DirectoryError

    def add_group(self, parent_dn, name, members, description=""):
        """
            Adds a new group under specified DN.

            Arguments:
                parent_dn: Distinguished name of parent
                name: Node name
                members: List of member DNs
        """
        dn = "cn=%s,%s" % (name, parent_dn)
        properties = {
            "cn": [name],
            "objectClass": ["top", "groupOfNames"],
            "member": members
        }
        if len(description):
            properties["description"] = [description]
        try:
            self.add_new(dn, properties)
            return dn
        except ldap.LDAPError, e:
            if "access" in e[0]["desc"]:
                raise DirectoryAccessError
            try:
                self.conn.whoami_s()
            except ldap.LDAPError:
                raise DirectoryConnectionError
            raise DirectoryError

    def modify_folder(self, dn, label, description=""):
        """
            Modified folder information.

            Arguments:
                dn: Distinguished name
                label: Node label
                description: description
        """
        dn, old_properties = self.search(dn, scope="base", fields=["o", "description"])[0]

        properties = {
            "o": [label],
        }

        if description:
            properties['description'] = [description]
        else:
            properties['description'] = []

        try:
            self.modify(dn, old_properties, properties)
        except ldap.LDAPError, e:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError, e:
                raise DirectoryConnectionError
            raise DirectoryError

    def modify_user(self, dn, password="", description=""):
        """
            Modifies user information.

            Arguments:
                dn: Distinguished name
                password: User password
                description: description
        """
        dn, old_properties = self.search(dn, scope="base", fields=["userPassword", "description"])[0]

        properties = {}

        if description:
            properties['description'] = [description]
        else:
            properties['description'] = []

        if len(password):
            properties["userPassword"] = [password]
        elif 'userPassword' in old_properties:
            del old_properties["userPassword"]

        try:
            self.modify(dn, old_properties, properties)
        except ldap.LDAPError, e:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError, e:
                raise DirectoryConnectionError
            raise DirectoryError

    def modify_computer(self, dn, password="", description=""):
        """
            Modifies computer information.

            Arguments:
                dn: Distinguished name
                password: Computer password
                description: description
        """
        dn, old_properties = self.search(dn, scope="base", fields=["userPassword", "description"])[0]

        properties = {}

        if description:
            properties['description'] = [description]
        else:
            properties['description'] = []

        if len(password):
            properties["userPassword"] = [password]
        elif 'userPassword' in old_properties:
            del old_properties["userPassword"]

        try:
            self.modify(dn, old_properties, properties)
        except ldap.LDAPError, e:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError, e:
                raise DirectoryConnectionError
            raise DirectoryError

    def modify_group(self, dn, members=[], description=""):
        """
            Modifies group information.

            Arguments:
                dn: Distinguished name
                members: List of members
                description: description
        """
        dn, old_properties = self.search(dn, scope="base", fields=["member", "description"])[0]

        properties = {
            "member": members
        }

        if description:
            properties['description'] = [description]
        else:
            properties['description'] = []

        try:
            self.modify(dn, old_properties, properties)
        except ldap.LDAPError, e:
            try:
                self.conn.whoami_s()
            except ldap.LDAPError, e:
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
            if "access" in e[0]["desc"]:
                raise DirectoryAccessError
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

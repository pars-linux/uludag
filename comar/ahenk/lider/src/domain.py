#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sha

import piksemel
import ldap
import ldap.modlist

import ldapmodel
import ldapview


LDAPCritical = (
    ldap.ADMINLIMIT_EXCEEDED,
    ldap.CONNECT_ERROR,
    ldap.SERVER_DOWN,
)

i18n = lambda x: x

class Connection:
    """LDAP connection"""
    
    def __init__(self, label, host, base_dn, bind_dn="", bind_password=""):
        self.label = label
        self.host = host
        self.base_dn = base_dn
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.ldap = None
        self.updateSum()
    
    def bind(self):
        """Open connection."""
        if self.whoami():
            return
        self.ldap = ldap.open(self.host)
        self.ldap.simple_bind_s(self.bind_dn, self.bind_password)
    
    def unbind(self):
        """Close connection."""
        if self.ldap:
            self.ldap.unbind_s()
            self.ldap = None
    
    def whoami(self):
        """Who am i?"""
        if self.ldap:
            try:
                return self.ldap.whoami_s()
            except ldap.LDAPError, e:
                return ""
        return ""
    
    def getSum(self, text):
        """Give sha1 sum of given text."""
        return sha.new(text).hexdigest()
    
    def updateSum(self):
        """Re-calculate sha1 sum of connection information."""
        fields = [
            self.label,
            self.host,
            self.base_dn,
            self.bind_dn,
            self.bind_password,
        ]
        self.sum = self.getSum(repr(fields))
    
    def isModified(self):
        """Connection info modified?"""
        fields = [
            self.label,
            self.host,
            self.base_dn,
            self.bind_dn,
            self.bind_password,
        ]
        sum = self.getSum(repr(fields))
        return sum != self.sum
    
    def search(self, dn, scope, filters="", fields=None):
        return self.ldap.search_s(dn, scope, filters, fields)
    
    def add(self, dn, attrs):
        self.ldap.add_s(dn, ldap.modlist.addModlist(attrs))
    
    def delete(self, dn):
        self.ldap.delete_s(dn)
    
    def modify(self, dn, old, new):
        self.ldap.modify_s(dn, ldap.modlist.modifyModlist(old, new))
    
    def rename(self, old, new):
        self.ldap.modrdn_s(old, new)


class DomainXMLParseError(Exception):
    pass


class DomainConfigMissing(Exception):
    pass


class DomainConnectionError(Exception):
    pass


class DomainConfig:
    """Lider domain configuration file parser."""
    
    def __init__(self):
        self.connections = []
    
    def addConnection(self, conn):
        """Add connection"""
        if not isinstance(conn, Connection):
            raise DomainConnectionError, i18n("Not a valid Connection instance.")
        self.connections.append(conn)
    
    def removeConnection(self, conn):
        self.connections.remove(conn)
    
    def clear(self):
        """Unbind all connections and clear connection list."""
        for connection in self.connections:
            connection.unbind()
        self.connections = []
    
    def toXML(self, filename=None):
        """Save current configuration to specified filename. (default: ~/.lider.xml)"""
        if not filename:
            filename = os.path.join(os.environ["HOME"], ".lider.xml")
        doc = piksemel.newDocument("Lider")
        for connection in self.connections:
            dom = doc.insertTag("Domain")
            dom.setAttribute("label", connection.label)
            dom.insertTag("Host").insertData(connection.host)
            dom.insertTag("BaseDN").insertData(connection.base_dn)
            if connection.bind_dn and connection.bind_password:
                bind = dom.insertTag("Bind")
                bind.insertTag("DN").insertData(connection.bind_dn)
                bind.insertTag("Password").insertData(connection.bind_password)
        file(filename, "w").write(doc.toPrettyString())
    
    def fromXML(self, filename=None, clear=False):
        """Load configuration from specified filename. (default: ~/.lider.xml)"""
        ignore_errors = False
        if not filename:
            filename = os.path.join(os.environ["HOME"], ".lider.xml")
            ignore_errors = True
        if not os.path.exists(filename):
            if not ignore_errors:
                raise DomainConfigMissing, i18n("Domain configuration file is missing.")
        try:
            doc = piksemel.parse(filename)
        except piksemel.ParseError:
            raise DomainXMLParseError, i18n("Domain configuration file has syntax errors.")
        if clear:
            self.clear()
        for tag in doc.tags():
            if tag.name() == "Domain":
                label = unicode(tag.getAttribute("label"))
                host = tag.getTagData("Host")
                base_dn = tag.getTagData("BaseDN")
                bind = tag.getTag("Bind")
                if bind:
                    bind_dn = bind.getTagData("DN")
                    bind_password = bind.getTagData("Password")
                else:
                    bind_dn = ""
                    bind_password = ""
                connection = Connection(label, host, base_dn, bind_dn, bind_password)
                self.connections.append(connection)


class DirectoryModel(ldapmodel.LdapClass):
    object_label = i18n("Directory")
    entries = (
        ("name", "dc", str, "", i18n("Name"), ldapview.nameWidget),
        ("label", "o", str, "", i18n("Label"), ldapview.labelWidget),
        ("type", "objectClass", list, ["dcObject", "organization"], None, None),
    )

class ComputerModel(ldapmodel.LdapClass):
    object_label = i18n("Computer")
    entries = (
        ("name", "cn", str, "", i18n("Name"), ldapview.labelWidget),
        ("type", "objectClass", list, ["top", "device", "pardusComputer"], None, None),
    )

class UnitModel(ldapmodel.LdapClass):
    object_label = i18n("Unit")
    entries = (
        ("name", "ou", str, "", i18n("Name"), ldapview.labelWidget),
        ("type", "objectClass", list, ["top", "organizationalUnit"], None, None),
    )

class UserModel(ldapmodel.LdapClass):
    object_label = i18n("User")
    entries = (
        ("name", "uid", str, "", i18n("Username"), ldapview.labelWidget),
        ("label", "cn", str, "", i18n("Real Name"), ldapview.labelWidget),
        ("password", "userPassword", str, "", i18n("Password"), ldapview.passwordWidget),
        ("shell", "loginShell", str, "", i18n("Shell"), ldapview.labelWidget),
        ("home", "homeDirectory", str, "", i18n("Home"), ldapview.labelWidget),
        ("uid", "uidNumber", int, "", i18n("User ID"), ldapview.numberWidget),
        ("gid", "gidNumber", int, "", i18n("Group ID"), ldapview.numberWidget),
        ("type", "objectClass", list, ["top", "account", "posixAccount"], None, None),
    )

class GroupModel(ldapmodel.LdapClass):
    object_label = i18n("Group")
    entries = (
        ("name", "cn", str, "", i18n("Group Name"), ldapview.labelWidget),
        ("gid", "gidNumber", int, "", i18n("Group ID"), ldapview.numberWidget),
        ("members", "memberUid", list, [], i18n("Members"), ldapview.listWidget),
        ("type", "objectClass", list, ["top", "posixGroup"], None, None),
    )

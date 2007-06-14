#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import ajan.ldaputil

header = """#
# Auto generated by Ahenk
#

"""


class UserPolicy(ajan.ldaputil.LdapClass):
    entries = (
        ("mode", "comarUserSourceMode", str, None),
        ("ldap_scope", "comarUserLdapSearchScope", str, None),
        ("ldap_base", "comarUserLdapBase", str, None),
        ("ldap_filter", "comarUserLdapFilter", str, None),
        ("ldap_uri", "comarUserLdapURI", str, None),
    )


class Policy:
    def __init__(self):
        self.policy = UserPolicy()
    
    def update(self, computer, units):
        print "updating user policy"
        self.policy.fromEntry(computer)
    
    def set_pam_ldap(self):
        conf = header
        conf += "uri %s\n" % self.policy.ldap_uri
        conf += "base %s\n" % self.policy.ldap_base
        scope = {
            "base": "base",
            "onelevel": "one",
            "subtree": "sub",
        }.get(self.policy.ldap_scope, "sub")
        conf += "scope %s\n" % scope
        if self.policy.ldap_filter:
            conf += "pam_filter %s\n" % self.policy.ldap_filter
        
        f = file("/etc/security/pam_ldap.conf", "w")
        f.write(conf)
        f.close()
    
    def apply(self):
        print "applying user policy", self.policy.mode
        if self.policy.mode == "ldap":
            print "pam"
            self.set_pam_ldap()
    
    def timers(self):
        return {}

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
import ajan.pam
import ajan.nsswitch

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
    
    def set_padl_config(self, filename):
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
        
        f = file(filename, "w")
        f.write(conf)
        f.close()
    
    def set_pam(self):
        p = ajan.pam.Pam()
        p.load()
        service = p.services["system-auth"]
        if self.policy.mode == "ldap":
            service.auth.set_module("pam_ldap.so", "sufficient", before="pam_unix.so")
            service.account.set_module("pam_ldap.so", "sufficient", before="pam_unix.so")
        else:
            service.remove_module("pam_ldap.so")
        service.save()
    
    def set_nss(self):
        nss = ajan.nsswitch.NameServiceSwitch()
        sources = ["files"]
        if self.policy.mode == "ldap":
            sources = ["ldap", "files"]
        nss["shadow"].sources = sources
        nss["passwd"].sources = sources
        nss["group"].sources = sources
        nss.save()
    
    def apply(self):
        print "applying user policy", self.policy.mode
        if self.policy.mode == "ldap":
            self.set_padl_config("/etc/security/pam_ldap.conf")
            self.set_padl_config("/etc/security/nss_ldap.conf")
        self.set_nss()
        self.set_pam()
    
    def timers(self):
        return {}

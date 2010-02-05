#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import os
import re
import sys

import ahenk.pam
import ahenk.nsswitch


# Configuration template for Samba
CONF_SAMBA = """[global]
   workgroup = %(workgroup)s
   realm = %(domain)s
   preferred master = no
   server string = %(domain)s
   security = ADS
   encrypt passwords = yes
   log level = 3
   log file = /var/log/samba/%%m
   max log size = 50
   printcap name = cups
   printing = cups
   winbind enum users = Yes
   winbind enum groups = Yes
   winbind use default domain = Yes
   winbind nested groups = Yes
   winbind separator = +
   idmap uid = 10000-20000
   idmap gid = 10000-20000
   ;template primary group = "Domain Users"
   template shell = /bin/bash

[homes]
   comment = Home Directories
   valid users = %%S
   read only = No
   browseable = No

[printers]
   comment = All Printers
   path = /var/spool/cups
   browseable = no
   printable = yes
   guest ok = yes
"""

# Configuration template for Kerberos
CONF_KRB = """[logging]
default = FILE:/var/log/krb5libs.log
kdc = FILE:/var/log/krb5kdc.log
admin_server = FILE:/var/log/kadmind.log

[libdefaults]
default_realm = %(domain)s
dns_lookup_realm = false
dns_lookup_kdc = false
ticket_lifetime = 24h
forwardable = yes

[realms]
%(domain)s = {
   kdc = %(host)s
   admin_server = %(host)s
   default_domain = %(domain)s
}

[domain_realm]
.%(domain)s = %(domain)s

[kdc]
profile = /var/kerberos/krb5kdc/kdc.conf

[appdefaults]
pam = {
   debug = false
   ticket_lifetime = 36000
   renew_lifetime = 36000
   forwardable = true
   krb4_convert = false
}
"""

# Configuration template for LDAP
CONF_LDAP = """uri ldap://%(ldap_host)s
suffix %(ldap_domain)s

pam_password exop
pam_filter objectclass=posixAccount
pam_login_attribute uid
"""


def pamSetSource(mode, dryrun=False):
    """
        Sets new authentication source for PAM

        Parameters:
            mode: unix, ldap or ad
            dryrun: Does nothing, just prints configuration if True
    """

    p = ahenk.pam.Pam()
    p.load()
    service = p.services["system-auth"]

    # Remove all extra modules
    service.remove_module("pam_winbind.so")
    service.remove_module("pam_ldap.so")
    service.remove_module("pam_mkhomedir.so")

    if mode in ["ad", "ldap"]:
        # LDAP or AD?
        if mode == "ad":
            module = "pam_winbind.so"
        else:
            module = "pam_ldap.so"
        # Authentication through LDAP/AD module is sufficient
        service.auth.set_module(module, "sufficient", before=["pam_unix.so"])
        # Account verification through LDAP/AD is sufficient
        service.account.set_module(module, "sufficient", before=["pam_unix.so"])
        # Update password through LDAP/AD module
        service.password.set_module(module, "sufficient", before=["pam_unix.so", "pam_cracklib.so"])
        # Session tasks
        if mode == "ad":
            # Always run AD session tasks
            service.session.set_module(module, "required", args="mkhomedir")
        else:
            # Make homedir
            service.session.set_module("pam_mkhomedir.so", "required", args="umask=0077")
        # Don't ask password twice, use first password for all modules
        for rule in service.auth:
            if rule.module == "pam_unix.so":
                if not "try_first_pass" in rule.args:
                    rule.args += " try_first_pass"
    elif mode == "unix":
        service.remove_module("pam_winbind.so")
        service.remove_module("pam_ldap.so")

    if dryrun:
        print "PAM Configuration:"
        print "    %s" % str(service).replace("\n", "\n    ")
    else:
        service.save()


def nsSwitchSetSource(mode, dryrun=False):
    """
        Sets new data source for NS Switch

        Parameters:
            mode: unix, ldap or ad
            dryrun: Does nothing, just prints configuration if True
    """

    nss = ahenk.nsswitch.NameServiceSwitch()

    if mode == "ldap":
        sources = ["files", "ldap"]
    elif mode == "ad":
        sources = ["files", "winbind"]
    else:
        sources = ["files"]

    nss["shadow"].sources = sources
    nss["passwd"].sources = sources
    nss["group"].sources = sources

    if dryrun:
        print "NS Switch Configuration:"
        print "    %s" % str(nss).replace("\n", "\n    ")
    else:
        nss.save()

def ldapConfig(host, domain, dryrun=False):
    """
        Makes LDAP configuration for NS and PAM modules.

        Parameters:
            host: LDAP Host
            domain: LDAP domain
            dryrun: Does nothing, just prints configuration if True
    """

    dc = "dc=" + domain.replace(".", ", dc=")
    conf_ldap = CONF_LDAP % {"ldap_domain": dc, "ldap_host": host}

    if dryrun:
        print "LDAP Configuration:"
        print "    %s" % str(conf_ldap).replace("\n", "\n    ")
    else:
        file("/etc/security/ldap.conf", "w").write(conf_ldap)

def domainConfig(host, domain, workgroup, dryrun=False):
    """
        Builds Samba and Kerberos configuration for AD authentication.

        Parameters:
            host: Hostname
            domain: Domain name
            workgroup: Workgroup
            dryrun: Does nothing, just prints configuration if True
    """

    conf_samba = CONF_SAMBA % {"domain": domain, "workgroup": workgroup}
    conf_krb = CONF_KRB % {"domain": domain, "host": host}

    if dryrun:
        print "Samba Configuration:"
        print "    %s" % str(conf_samba).replace("\n", "\n    ")
        print
        print "Kerberos Configuration:"
        print "    %s" % str(conf_krb).replace("\n", "\n    ")
    else:
        file("/etc/samba/smb.conf", "w").write(conf_samba)
        file("/etc/krb5.conf", "w").write(conf_krb)

def serviceConfig(name, key, value=None, dryrun=False):
    """
        Updates configuration of a system service.

        Parameters:
            name: Service name
            key: Setting
            value: Value
            dryrun: Does nothing, just prints configuration if True
    """

    fn = os.path.join("/etc/conf.d", name)

    if os.path.exists(fn):
        lines = []
        updated = False
        for line in file(fn):
            line = line.strip()
            if re.match("^%s\s*=.*" % key, line):
                lines.append("%s = %s" % (key, value))
                updated = True
            else:
                lines.append(line)
        if not updated:
            lines.append("%s = %s" % (key, value))
        conf_service = "\n".join(lines)
    else:
        conf_service = "%s = %s\n" % (key, value)

    if dryrun:
        print "Service Configuration (%s):" % name
        print "    %s" % str(conf_service).replace("\n", "\n    ")
    else:
        file(fn, "w").write(conf_service)


if __name__ == '__main__':
    # Command line options
    parser = optparse.OptionParser()

    parser.add_option("-t", "--type", dest="type",
                      help="Authentication source (unix, ldap, ad)", metavar="TYPE")
    parser.add_option("-H", "--host", dest="host",
                      help="Hostname for LDAP or Active Directory authentication.")
    parser.add_option("-d", "--domain", dest="domain",
                      help="Domain name for LDAP or Active Directory authentication.")
    parser.add_option("-w", "--workgroup", dest="workgroup",
                      help="Workgroup for Active Directory authentication.")
    parser.add_option("-n", "--dry-run", action="store_true", dest="dryrun",
                      help="Do nothing, just tell.")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="Verbose mode")

    (options, args) = parser.parse_args()

    # If type is missing, print help
    if not options.type:
        parser.print_help()
        sys.exit(0)

    # Only root can run that application
    if os.getuid() != 0:
        print "%s must be run as root." % sys.argv[0]
        sys.exit(1)

    # If type is unknown, print error message
    if options.type not in ["ad", "ldap", "unix"]:
        print "Authentication source can be 'unix', 'ldap' or 'ad' only."
        sys.exit(1)

    if options.type == "unix":
        pamSetSource("unix", options.dryrun)
        nsSwitchSetSource("unix", options.dryrun)
    elif options.type == "ldap":
        if not options.host or not options.domain:
            print "Host and domain name is required. See --help"
            sys.exit(1)
        # Use LDAP module as authentication source
        pamSetSource("ldap", options.dryrun)
        # Use LDAP as Name Service source
        nsSwitchSetSource("ldap", options.dryrun)
        # LDAP configuration for NS and PAM
        ldapConfig(options.host, options.domain, options.dryrun)
    elif options.type == "ad":
        if not options.host or not options.domain or not options.workgroup:
            print "Host, domain name and workgroup is required. See --help"
            sys.exit(1)
        # Use WinBind (AD) module as authentication source
        pamSetSource("ad", options.dryrun)
        # Use WinBind (AD) as Name Service source
        nsSwitchSetSource("ad", options.dryrun)
        # Kerberos and SAMBA configuration
        domainConfig(options.host, options.domain, options.workgroup, options.dryrun)
        serviceConfig("samba", "winbind", "yes", options.dryrun)
        # FIXME: Start Samba

    sys.exit(0)

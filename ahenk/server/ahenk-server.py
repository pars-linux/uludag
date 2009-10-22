#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import optparse
import os
import subprocess
import sys
import time


TEMP_LDAP = """include       /etc/openldap/schema/core.schema
include       /etc/openldap/schema/cosine.schema
include       /etc/openldap/schema/nis.schema
include       /etc/openldap/schema/ahenk.schema

pidfile       /var/run/openldap/slapd.pid
argsfile      /var/run/openldap/slapd.args

modulepath    /usr/libexec/openldap
moduleload    back_hdb.la

database      bdb
suffix        "%(domain)s"
rootdn        "cn=%(root_account)s, %(domain)s"
rootpw        %(password)s

directory     /var/lib/openldap-data
index         objectClass eq"""

TEMP_LDIF = """dn: %(domain)s
objectclass: dcObject
objectclass: organization
o: %(title)s
dc: %(dc)s

dn: cn=%(root_account)s, %(domain)s
objectclass: organizationalRole
cn: %(root_account)s"""


def getText(label, hidden=False):
    try:
        if hidden:
            return getpass.getpass("%s > " % label)
        else:
            return raw_input("%s > " % label)
    except KeyboardInterrupt:
        return None


def cryptPass(password):
    cmd = ["/usr/sbin/slappasswd", "-n", "-s", password]
    proc = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    return proc.stdout.read()


def makeLDAPConf(domain, root_account, root_password):
    if "dc=" not in domain:
        domain = "dc=" + domain.replace(".", ", dc=")

    root_password = cryptPass(root_password)

    return TEMP_LDAP % {"domain": domain, "root_account": root_account, "password": root_password}


def makeLDIF(domain, root_account):
    if "dc=" not in domain:
        domain = "dc=" + domain.replace(".", ", dc=")
    dc = domain.split(",")[0].split("dc=")[1]
    return TEMP_LDIF % {"domain": domain, "title": dc.capitalize(),  "dc": dc, "root_account": root_account}


def importLDIF(domain, root_account, root_password):
    if "dc=" not in domain:
        domain = "dc=" + domain.replace(".", ", dc=")

    cn = "cn=%s, %s" % (root_account, domain)

    ldif = makeLDIF(domain, root_account)

    cmd = ["/usr/bin/ldapadd", "-x", "-D", cn, "-w", root_password]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input=ldif)


if __name__ == "__main__":

    parser = optparse.OptionParser("usage: %prog [options] domain")

    parser.add_option("-N", "--dryrun", dest="dryrun", action="store_true",
                      help="Do nothing, just tell")
    parser.add_option("-u", "--username", dest="username",
                      help="Username for root account", metavar="NAME")
    parser.add_option("-p", "--password", dest="password",
                      help="Password for root account", metavar="PW")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="Verbose mode")

    (options, args) = parser.parse_args()

    if os.getuid() != 0 and not options.dryrun:
        print "%s must be run as root." % sys.argv[0]
        sys.exit(1)

    if not len(args):
        print "A domain name is required."
        sys.exit(1)

    domain = args[0]

    if not options.username:
        options.username = getText("Username for admin account")
        if not options.username:
            sys.exit(1)

    if not options.password:
        options.password = getText("Password for admin account", hidden=True)
        if not options.password:
            sys.exit(1)

    print "Stopping openldap-server"
    if not options.dryrun:
        os.system("service openldap_server stop")

    print "Writing new /etc/openldap/slapd.conf"
    conf = makeLDAPConf(domain, options.username, options.password)
    if not options.dryrun:
        file("/etc/openldap/slapd.conf", "w").write(conf)
    else:
        print
        print "    " + conf.replace("\n", "\n    ")
        print

    print "Starting openldap-server"
    if not options.dryrun:
        os.system("service openldap_server start")

    print "Loading inital database components"
    if not options.dryrun:
        time.sleep(3)
        importLDIF(domain, options.username, options.password)
    else:
        ldif = makeLDIF(domain, options.username)
        print
        print "    " + ldif.replace("\n", "\n    ")
        print

    print "Server is ready."

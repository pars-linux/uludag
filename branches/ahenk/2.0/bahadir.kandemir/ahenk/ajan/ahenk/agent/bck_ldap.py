# -*- coding: utf-8 -*-

"""
    Ajan utils.
"""

import hashlib
import ldap
import ldif
import logging
import os
import time
import StringIO
import Queue


TIMEOUT = 5


def get_ldif(value):
    """
        Converts a policy object to LDIF string.

        Args:
            value: Policy setting object
        Returns: LDIF string
    """
    output = StringIO.StringIO()
    writer = ldif.LDIFWriter(output)
    try:
        writer.unparse(value[0], value[1])
        text = output.getvalue()
    except (KeyError, TypeError):
        return ''
    output.close()
    return text

def load_ldif(filename):
    """
        Reads an LDIF file and returns as a policy object.

        Args:
            filename: File that contains LDIF
        Returns:
            Policy object
    """
    class MyLDIF(ldif.LDIFParser):
        """Custom LDIF Parser"""
        def handle(self, dn, entry):
            """LDIF Handler"""
            if self.comp:
                self.ou.append(entry)
            else:
                self.comp = entry

    try:
        parser = MyLDIF(file(filename))
    except (KeyError, TypeError):
        return None
    parser.comp = None
    parser.ou = []
    parser.parse()
    return parser.comp

def parent_paths(dn, domain):
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
        if len(dn_parts) - index == domain.count(","):
            break
        paths.append(part)
    paths.reverse()

    return paths

def fetch_policy(conn, options, domain, dn):
    """
        Fetches a policy if necessary.

        Args:
            conn: LDAP connection object
            options: Options
            domain: Domain name
            dn: Distinguished name
        Returns:
            True or False, and policy object
    """

    policy_file = os.path.join(options.policydir, "policy_" + options.username)
    timestamp_file = policy_file + '.ts'
    timestamp_old = ''
    timestamp_new = ''
    policy_new = {}
    update_required = False

    if os.path.exists(timestamp_file):
        timestamp_old = file(timestamp_file).read().strip()
        try:
            timestamp_old = int(timestamp_old)
        except ValueError:
            update_required = True

    paths = parent_paths(dn, domain)

    timestamps = []
    for path in paths:
        search = conn.search_s(path, ldap.SCOPE_BASE, attrlist=['modifyTimestamp'])
        if len(search):
            attrs = search[0][1]
            timestamp = int(attrs['modifyTimestamp'][0][:-1])
            timestamps.append(timestamp)

    timestamp_new = max(timestamps)
    if timestamp_new != timestamp_old:
        update_required = True

    if update_required:
        for path in paths:
            search = conn.search_s(path, ldap.SCOPE_BASE)
            if len(search):
                attrs = search[0][1]
                policy_new.update(attrs)

        file(timestamp_file, 'w').write(str(timestamp_new))
        file(policy_file, 'w').write(get_ldif(policy_new))
        return True, policy_new

    return False, {}

def ldap_go(options, q_in, q_out, q_ldap):
    """
        Main event loop for LDAP worker
    """
    # Load last fetched policy
    logging.info("Loading last fetched policy.")
    filename = os.path.join(options.policydir, "policy_", options.username)
    if os.path.exists(filename):
        policy = load_ldif(filename)
        if policy:
            q_in.put({"type": "policy init", "policy": policy})

    domain = "dc=" + options.domain.replace(".", ", dc=")
    while True:
        try:
            conn = ldap.open(options.hostname)

            pattern = "(cn=%s)" % options.username
            search = conn.search_s(domain, ldap.SCOPE_SUBTREE, pattern, ['cn'])
            if len(search):
                dn = search[0][0]
            else:
                raise ldap.NO_SUCH_OBJECT

            conn.simple_bind(dn, options.password)
            logging.debug("Logged in as %s" % dn)

            while True:
                updated, policy = fetch_policy(conn, options, domain, dn)
                if updated:
                    logging.info("LDAP policy was updated.")
                    policy_repr = dict(zip(policy.keys(), ['...' for x in range(len(policy))]))
                    #policy_repr = policy
                    logging.debug("New policy: %s" % policy_repr)
                    q_in.put({"type": "policy", "policy": policy})
                try:
                    logging.debug("Checking policy...")
                    q_ldap.get(timeout=options.interval)
                except (Queue.Empty, IOError):
                    continue
        except (ldap.SERVER_DOWN, ldap.NO_SUCH_OBJECT, IndexError):
            logging.warning("LDAP connection failed. Retrying in %d seconds." % TIMEOUT)
            time.sleep(TIMEOUT)

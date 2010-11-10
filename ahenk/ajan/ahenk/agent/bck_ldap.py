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

def fetch_policy(conn, options, domain, pattern):
    """
        Fetches a policy if necessary.

        Args:
            conn: LDAP connection object
            options: Options
            domain: Domain name
            pattern: Search pattern
        Returns:
            True or False
    """
    policy_file = os.path.join(options.policydir, "policy_" + options.username)
    timestamp_file = policy_file + '.ts'
    timestamp_old = ''
    update_required = False

    if os.path.exists(timestamp_file):
        timestamp_old = file(timestamp_file).read().strip()

    if not timestamp_old:
        update_required = True

    search = conn.search_s(domain, ldap.SCOPE_SUBTREE, pattern, ['modifyTimestamp'])
    if len(search):
        attrs = search[0][1]
        timestamp_new = attrs['modifyTimestamp'][0]
        if timestamp_new != timestamp_old:
            update_required = True

    if update_required:
        search = conn.search_s(domain, ldap.SCOPE_SUBTREE, pattern)
        if len(search):
            attrs = search[0][1]
            file(timestamp_file, 'w').write(timestamp_new)
            file(policy_file, 'w').write(get_ldif(attrs))
            return True, attrs

    return False, {}

def ldap_go(options, q_in, q_out):
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
    username = "cn=%s, %s" % (options.username, domain)
    while True:
        try:
            conn = ldap.open(options.hostname)
            conn.simple_bind(username, options.password)
            while True:
                pattern = "(cn=%s)" % options.username
                updated, policy = fetch_policy(conn, options, domain, pattern)
                if updated:
                    logging.info("LDAP policy was updated.")
                    policy_repr = dict(zip(policy.keys(), ['...' for x in range(len(policy))]))
                    logging.debug("New policy: %s" % policy_repr)
                    q_in.put({"type": "policy", "policy": policy})
                time.sleep(options.interval)
        except (ldap.SERVER_DOWN, ldap.NO_SUCH_OBJECT, IndexError):
            logging.warning("LDAP connection failed. Retrying in 3 seconds.")
            time.sleep(3)

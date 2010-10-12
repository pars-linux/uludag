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
    writer.unparse(value[0], value[1])
    text = output.getvalue()
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

    parser = MyLDIF(file(filename))
    parser.comp = None
    parser.ou = []
    parser.parse()
    return parser.comp

def update_ldif(filename, value):
    """
        Args:
            filename: File to store LDIF
            value: LDIF object
        Returns: True if content was updated
    """
    hash_old = ""
    if os.path.exists(filename):
        hash_old = hashlib.sha1(file(filename).read()).hexdigest()
    ldif_new = get_ldif(value)
    hash_new = hashlib.sha1(ldif_new).hexdigest()
    if hash_new != hash_old:
        file(filename, "w").write(ldif_new)
        return True
    return False

def ldap_go(options, q_in, q_out):
    """
        Main event loop for LDAP worker
    """
    # Load last fetched policy
    logging.info("Loading last fetched policy.")
    filename = os.path.join(options.policydir, options.username)
    if os.path.exists(filename):
        policy = load_ldif(filename)
        q_in.put({"type": "policy init", "policy": policy})

    domain = "dc=" + options.domain.replace(".", ", dc=")
    username = "cn=%s, %s" % (options.username, domain)
    while True:
        try:
            conn = ldap.open(options.hostname)
            conn.simple_bind(username, options.password)
            while True:
                pattern = "(cn=%s)" % options.username
                search = conn.search_s(domain, ldap.SCOPE_SUBTREE, pattern)[0]
                policy = search[1]
                if update_ldif(os.path.join(options.policydir, options.username), search):
                    logging.info("LDAP policy was updated.")
                    logging.debug("New policy: %s" % repr(policy))
                    q_in.put({"type": "policy", "policy": policy})
                time.sleep(3)
        except (ldap.SERVER_DOWN, ldap.NO_SUCH_OBJECT, IndexError):
            logging.warning("LDAP connection failed. Retrying in 3 seconds.")
            time.sleep(3)

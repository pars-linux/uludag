#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# A python script which matches available sessions with the
# available smart cards. It primarily targets AKIS smart cards but should
# work with all PKCS#11 modules.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#
# Copyright (C) 2011 TUBITAK/UEKAE
# Ozan Çağlayan <ozan_at_pardus.org.tr>

import os
import sys
import glob

from optparse import OptionParser

import PyKCS11

DEBUG = False
DEFAULT_PKCS11_MODULE = "/usr/lib/libakisp11.so"

def debug(msg):
    if DEBUG:
        print "DEBUG: %s" % msg

def error(msg):
    print >> sys.stderr, "ERROR: %s" % msg

def get_pkcs11_loggedin_users():
    """Returns a dict of users who seems to be logged with
    a PKCS#11 token."""
    d = {}
    for env in glob.glob("/proc/*/environ"):
        try:
            environ = open(env, "r").read().strip()
            if "DISPLAY=" in environ:
                env = dict([line.split("=", 1) for line in environ.split("\x00") if line])
                d[env["USER"]] = dict([(k, env[k]) for k in env.keys() if k.startswith("PKCS11_")])
        except IOError, e:
            pass

    return d

def get_pkcs11_env_vars(user=None):
    """Return a dict of PKCS#11 related session keys."""
    d = {}
    for key,value in os.environ.items():
        if key.startswith("PKCS11_"):
            d[key] = value

    return d

def main():
    # Command-line parsing
    parser = OptionParser()

    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="debug",
                      default=False,
                      help="Print additional debugging informations")

    parser.add_option("-m", "--pkcs11-module",
                      action="store",
                      dest="module",
                      default=DEFAULT_PKCS11_MODULE,
                      help="PKCS#11 module to use")

    (options, args) = parser.parse_args()

    global DEBUG
    DEBUG = options.debug

    if not os.path.exists(options.module):
        error("Can't find %s" % options.module)

    pkcs11 = PyKCS11.PyKCS11Lib()
    pkcs11.load(options.module)

    # Get available slots
    available_slots = pkcs11.getSlotList()

    all_attributes = [PyKCS11.CKA_CLASS,
                      PyKCS11.CKA_LABEL,
                      PyKCS11.CKA_SERIAL_NUMBER]

    certificates = {}

    user_dict = get_pkcs11_loggedin_users()

    for slot in available_slots:
        try:
            # Get token information
            token = pkcs11.getTokenInfo(slot)
        except PyKCS11.PyKCS11Error, e:
            if e.value == PyKCS11.CKR_TOKEN_NOT_PRESENT:
                debug("No token found in slot %d" % slot)
        else:
            # Open a PIN-less session and get objects
            session = pkcs11.openSession(slot)
            objects = session.findObjects()

            # Traverse objects for finding certificates
            for obj in objects:
                attributes = session.getAttributeValue(obj, all_attributes)
                attr_dict = dict(zip(all_attributes, attributes))

                if attr_dict[PyKCS11.CKA_CLASS] == PyKCS11.CKO_CERTIFICATE:
                    serial = attr_dict[PyKCS11.CKA_SERIAL_NUMBER]
                    label = attr_dict[PyKCS11.CKA_LABEL]
                    certificates[serial] = label

            print certificates.items()

if __name__ == "__main__":
    sys.exit(main())

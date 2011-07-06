#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from optparse import OptionParser

import PyKCS11

DEBUG = False
DEFAULT_PKCS11_MODULE = "/usr/lib/libakisp11.so"

def debug(msg):
    if DEBUG:
        print "DEBUG: %s" % msg

def error(msg):
    print >> sys.stderr, "ERROR: %s" % msg


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

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    LDAP schema generator
"""

# Standard Modules
import os
import sys

# LDAP object types
TYPES = {
    "str": "1.3.6.1.4.1.1466.115.121.1.40",
    "int": "1.3.6.1.4.1.1466.115.121.1.27",
}


def print_usage():
    print "Usage: %s ID Name schema.txt" % sys.argv[0]
    print
    print "  Schema file example:"
    print "    # name type description ..."
    print "    softwareRepositories str Comma seperated list of package repositories"
    print "    softwareUpdateSchedule str Auto update schedule in CRON format"
    print "    softwareUpdateMode str Auto update mode (off, security or full)"
    print
    print "  Valid types:"
    print "    str, int, [str], [int]"
    print

def main():
    try:
        oid = int(sys.argv[1])
        name = sys.argv[2]
        filename = sys.argv[3]
    except (IndexError, ValueError):
        print_usage()
        return 1

    if not os.path.exists(filename):
        print "Unable to find %s" % filename
        return 1

    text = ["objectIdentifier pardusBase 2.16.792.1.2.1.1.5.1"]

    fields = []
    index = 1
    for line in file(filename):
        if line.startswith("#") or not line.strip():
            continue
        a_name, a_type, a_desc = line.strip().split(" ", 2)
        fields.append(a_name)
        a_list = False
        if a_type.startswith("["):
            a_list = True
            a_type = a_type[1:-1]
        text.append("attributetype ( pardusBase:%d.%d" % (oid, index))
        text.append("    NAME '%s'" % a_name)
        text.append("    DESC '%s'" % a_desc)
        text.append("    SYNTAX %s" % TYPES[a_type])
        if not a_list:
            text.append("    SINGLE-VALUE")
        text.append(" )")
        text.append("")
        index += 1

    text.append("objectclass ( pardusBase:%d.0" % oid)
    text.append("    NAME '%s'" % name)
    text.append("    SUP top")
    text.append("    AUXILIARY")
    text.append("    MAY ( %s )" % " $ ".join(fields))
    text.append(" )")

    print "\n".join(text)

if __name__ == "__main__":
    sys.exit(main())

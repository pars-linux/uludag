#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import optparse
import xmlrpclib

BUILDSERVICE="http://localhost:8007/"

### Utility functions

def _print(msg, title=False, color=None):
    """Prints optionally colorized message. If title is True, draws a line under the title."""
    colors = {'green'   : '\x1b[32;01m%s\x1b[0m',
              'red'     : '\x1b[31;01m%s\x1b[0m',
              'yellow'  : '\x1b[33;01m%s\x1b[0m',
              'none'    : '\x1b[0m%s\x1b[0m',
             }
    result = msg
    if color:
        result = colors[color, "none"] % result
    if title:
        result += "\n%s" % ((len(msg)+1)*'-')
    print result


if __name__ == "__main__":

    parser = optparse.OptionParser()

    parser.add_option("-u", "--username", dest="username", help="Username to authenticate on the buildservice")
    parser.add_option("-p", "--password", dest="password", help="Password to authenticate on the buildservice")

    (options, parameters) = parser.parse_args()

    # Connect to the remote end
    handle = xmlrpclib.ServerProxy(BUILDSERVICE)
    available_methods = []

    try:
        available_methods = [m for m in handle.system.listMethods() if not m.startswith("system.")]
    except Exception, e:
        _print("Error: %s (%s)" % (e.strerror, BUILDSERVICE))
        sys.exit(1)

    if available_methods:
        # Succesfully connected
        _print("Pardus Build Service Client v1.0", True)
        print
        _print("Available Methods:", True)
        for method in available_methods:
            print handle.system.methodSignature(method)

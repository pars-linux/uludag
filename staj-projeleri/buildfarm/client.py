#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006,2007 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

import sys
import xmlrpclib

# i18n
import gettext
__trans = gettext.translation('buildfarm', fallback=True)
_ = __trans.ugettext

# connection parameters
REMOTE_HOST = "localhost"
REMOTE_PORT = 443

def usage():
    print _("""Usage: buildfarm <command> [<param> ...]
    
  where command is:

  help           Displays this help screen
  status         Displays the buildfarm's active job(s)
  sync           Synchronizes the binary repositories
  update         Updates the repository
  list
    work         Dumps the work queue
    wait         Dumps the wait queue
  build
    index        Builds PiSi index for the repository
    packages     Builds and installs all packages of the work queue
    
 """)

def client(op, cmd=None):
    
    funcString = None
    
    # Get a connection handle
    remoteURI = "https://" + REMOTE_HOST + ":" + str(REMOTE_PORT)
    server = xmlrpclib.ServerProxy(remoteURI)
    
    if op == "update":
        print op
    elif op == "sync":
        print op
    elif op == "status":
        print op
        
    elif op == "list":
        funcString = "get" + cmd.capitalize() + "Queue"
        print _("Current %s queue" % cmd)
        print "-" * 20
        print "\n".join(server.__getattr__(funcString)())
        
    elif op == "build":
        funcString = op + cmd.capitalize()
        print _("Calling %s()..." % funcString)
        retval = server.__getattr__(funcString)()
        if retval:
            print _("%s successfully returned." % funcString)
        else:
            print _("Errors during %s." % funcString)
    
    # Call the appropriate method
    

if __name__ == "__main__":

    args = sys.argv[1:]
    
    if args == []:
        usage()
        
    elif args[0] == "help":
        usage()
    
    elif len(args) == 1:
        if args[0] in ("update","sync","status"):
            client(args[0])
        else:
            usage()
    
    elif len(args) == 2:
        if args[0] == "list" and args[1] in ("work","wait") or \
            args[0] == "build" and args[1] in ("index","packages"):
            client(args[0],args[1])
        else:
            usage()
        
    else:
        usage()
        
    


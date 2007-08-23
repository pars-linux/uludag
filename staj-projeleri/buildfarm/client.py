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
    subst = {'program':sys.argv[0]}
    print _("""Usage: %(program)s <command> [<param> ...]
    
  where command is:

  help           Displays this help screen
  status         Displays the buildfarm's active job(s)
  sync           Synchronizes the binary repositories
  update         Updates local pspec repository
  add p          Adds the package 'p' to the work queue
  list
    wait         Dumps the wait queue
    work         Dumps the work queue
  build
    index        Builds PiSi index for the repository
    packages     Builds and installs all packages of the work queue
  transfer
    wait p       Transfers the package 'p' from the work queue to the wait queue
    work p       Transfers the package 'p' from the wait queue to the work queue
  remove
    wait p       Removes the package 'p' from the wait queue
    work p       Removes the package 'p' from the work queue
                 Note: p can be 'all' to remove all packages from a queue
    
  Examples:
    $ %(program)s list wait
    $ %(program)s build packages
    $ %(program)s append work xmoto/pspec.xml
    $ %(program)s remove work all
 """ % subst)

def client(op, cmd=None, pspec=None):
    
    funcString = None
    
    # Get a connection handle
    remoteURI = "https://" + REMOTE_HOST + ":" + str(REMOTE_PORT)
    server = xmlrpclib.ServerProxy(remoteURI)
    
    # 1 Parameter
    if op == "update":
        result = server.updateRepository()
        if result:
            print _("These packages are added to the work queue\n%s\n" % ('-'*42))
            print "\n".join(result)
        else:
            print _("Local pspec repository is up-to-date")
    elif op == "sync":
        result = server.sync()
        if result:
            print _("'%s' doesn't contain these packages:\n%s" % ("pardus-2007", ('-'*45)))
            print "\n".join(result)
        else:
            print_("The repositories are already synchronized.")
    elif op == "status":
        print op
    
    # 2 Parameters
    elif op == "add":
        retval = server.appendToWorkQueue(pspec)
        
        if retval:
            print _("%s successfully added to the work queue!" % pspec)
        else:
            print _("The package '%s' is already in the work queue!" % pspec)
        
    elif op == "list":
        funcString = "get" + cmd.capitalize() + "Queue"
        result = server.__getattr__(funcString)()
        if result:    
            print _("Current %s queue\n%s" % (cmd, ('-'*19)))
            print "\n".join(result)
        else:
            print _("%s queue is empty!" % cmd.capitalize())
        
    elif op == "build":
        funcString = "build" + cmd.capitalize()
        print _("Calling %s()..." % funcString)
        retval = server.__getattr__(funcString)()
        if retval:
            print _("%s successfully returned." % funcString)
        else:
            print _("Errors during %s." % funcString)
    
    # 3 Parameters
    elif op == "remove":
        funcString = "removeFrom" + cmd.capitalize() + "Queue"
        print _("Removing '%s' from %s queue.." % (pspec, cmd))
        retval = server.__getattr__(funcString)(pspec)
        if retval:
            print _("Removed!")
        else:
            print _("Make sure that the packages are already in the %s queue!" % cmd)
            
    elif op == "transfer":
        funcString = "transferTo" + cmd.capitalize() + "Queue"
        retval = server.__getattr__(funcString)(pspec)
        if retval:
            print _("%s transferred to %s queue!" % (pspec, cmd))
        else:
            print _("Can not transfer %s to %s queue!" % (pspec, cmd))
    
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
        if args[0] == "add":
            client(args[0],pspec=args[1])
        elif args[0] == "list" and args[1] in ("work","wait") or \
            args[0] == "build" and args[1] in ("index","packages"):
            client(args[0],args[1])
        else:
            usage()
            
    elif len(args) == 3:
        if args[0] in ("remove","transfer") and args[1] in ("work","wait"):
            client(args[0],args[1],args[2])
        else:
            usage()
        
    else:
        usage()
        
    


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

def sendDirectory(server, dirname, username=""):
    # Sends the directory hierarchy to the remote server.
    # The remote server builds the pisi package(s) and places them in a
    # meaningful remote directory (e.g. /var/www/maintainer/package)
    
    import os
    from subprocess import call
    
    # First of all check if it is a non-empty directory
    if os.path.isdir(dirname) and os.listdir(dirname):
        # dirname ex. = applications/editors/vim
        # filename ex. = vim.tar.bz2
        dirname = os.path.normpath(dirname)
        filename = os.path.basename(dirname) + ".tar.bz2"
        
        print dirname
        
        tarCmd = ["tar", "cjf", filename, dirname]
        
        # if you give a package directory, it will add the component.xml
        # of the upper directory
        if not os.path.isfile("%s/component.xml" % dirname):
            tarCmd.append("--add-file=%s/component.xml" % os.path.dirname(dirname))
        
        # ASK : Use tarfile module instead?
        call(tarCmd)
        
        # Serialize file data
        f = open(filename, "rb")
        d = xmlrpclib.Binary(f.read())
        f.close()
        
        # Delete the compressed archive
        os.unlink(filename)
        
        # Call the appropriate method with the username validated from LDAP. 
        return server.buildArchive(dirname, filename, d, username)
    
    else:
        return False

def usage():
    subst = {'program':sys.argv[0]}
    print _("""Usage: %(program)s <operation> <command> [<param> ...]
    
  where operation is:

  help              Displays this help screen
  sync              Synchronizes the binary repositories
  update            Updates local pspec repository
  add  p1,..,pn     Adds the package(s) p1,..,pn to work queue
  send dir          Sends the contents of 'dir' to the server for remote building
  list              Has 2 possible commands : wait, work
    wait            Dumps the wait queue
    work            Dumps the work queue
  build             Has 2 possible commands : index, packages
    index           Builds PiSi index for the repository
    packages        Builds and installs all packages of the work queue
  transfer          Has 2 possible commands : wait, work
    wait p1,..,pn   Transfers the package(s) p1,..,pn from work queue to wait queue
    work p1,..,pn   Transfers the package(s) p1,..,pn from wait queue to work queue
  remove            Has 2 possible commands : wait, work
    wait p1,..,pn   Removes the package(s) p1,..,pn from wait queue
    work p1,..,pn   Removes the package(s) p1,..,pn from work queue
    
  Examples:
    $ %(program)s list wait
    $ %(program)s build packages
    $ %(program)s add xmoto/pspec.xml
    $ %(program)s remove work xmoto/pspec.xml ppracer/pspec.xml
 """ % subst)

def client(op, **kwargs):
    
    # Used for identifying server return codes in a user friendly manner 
    returnStrings = {'build'    : [_("Build process is successfully finished!"),
                                   None,
                                   _("Work Queue is empty!"),
                                   _("Queue finished with problems!")],
                     'add'      : [_("'%s' successfully added to the work queue!"),
                                   None,
                                   _("The package '%s' doesn't exist!"),
                                   _("The package '%s' is already in the work queue!")],
                     'remove'   : [_("Removed '%s' from %s queue!"),
                                   None,
                                   _("'%s' doesn't exist in the %s queue!")],
                     'transfer' : [_("'%s' is successfully transferred!"),
                                   None,
                                   _("'%s' doesn't exist in the source queue!")]
                    }
    
    funcString = None
    cmd = kwargs.get('cmd', None)
    pspecList = kwargs.get('pspec', None)
    
    # Get a connection handle
    remoteURI = "https://" + REMOTE_HOST + ":" + str(REMOTE_PORT)
    server = xmlrpclib.ServerProxy(remoteURI)
    
    # 1 Parameter
    if op == "update":
        result = server.updateRepository()
        if result:
            print _("These packages are added to the work queue\n%s\n" % ('-'*42))
            print "\n".join(result)
            print _("\nTotal: %d packages" % len(result) )
        else:
            print _("Local pspec repository is up-to-date")
            
    elif op == "sync":
        result = server.sync()
        if result:
            print _("'%s' doesn't contain these packages:\n%s" % ("pardus-2007", ('-'*45)))
            print "\n".join(result)
            print _("\nTotal: %d packages" % len(result) )
        else:
            print_("The repositories are already synchronized.")
            
    # 2 Parameters
        
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
        print _("Building %s..." % cmd)
        retval = server.__getattr__(funcString)()
        if retval == 1:
            print _("Buildfarm is busy!")
        else:
            print returnStrings['build'][retval]
    
    # 3 or more Parameters
    elif op == "add":
        for pspec in pspecList:
            retval = server.appendToWorkQueue(pspec, True)
            if retval == 1:
               print _("Buildfarm is busy!")
            else:
                print (returnStrings['add'][retval] % pspec)
            
    elif op == "remove":
        funcString = "removeFrom" + cmd.capitalize() + "Queue"
        for pspec in pspecList:    
            retval = server.__getattr__(funcString)(pspec)
            if retval == 1:
               print _("Buildfarm is busy!")
            else:
                print returnStrings['remove'][retval] % (pspec, cmd)
            
    elif op == "transfer":
        funcString = "transferTo" + cmd.capitalize() + "Queue"
        for pspec in pspecList:
            retval = server.__getattr__(funcString)(pspec)
            if retval == 1:
               print _("Buildfarm is busy!")
            else:
                print returnStrings['transfer'][retval] % (pspec)
            
if __name__ == "__main__":

    args = sys.argv[1:]
    
    # dummy trick to facilitate parsing of 'add' in the next blocks..
    if args.__contains__("add"):
        args.insert(1, "work")
    
    if args == []:
        usage()
        
    elif args[0] == "help":
        usage()
    
    elif len(args) == 1:
        if args[0] in ("update","sync"):
            client(args[0])
        else:
            usage()
    
    elif len(args) == 2:
        # doesn't work.
        if args[0] in ("send"):
            client(args[0],pspec=args[1])
        elif args[0] == "list" and args[1] in ("work","wait") or \
             args[0] == "build" and args[1] in ("index","packages"):
            client(args[0],cmd=args[1])
        else:
            usage()
    
    elif len(args) >= 3:        
        if args[0] in ("add","remove","transfer") and args[1] in ("work","wait"):
            client(args[0],cmd=args[1],pspec=args[2:])
        else:
            usage()
        
    else:
        usage()
        
    


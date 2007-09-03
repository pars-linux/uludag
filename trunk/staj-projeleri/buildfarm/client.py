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
    print _("""Usage: %(program)s <command> [<param> ...]
    
  where command is:

  help           Displays this help screen
  status         Displays the buildfarm's active job(s)
  sync           Synchronizes the binary repositories
  update         Updates local pspec repository
  add p          Adds the package 'p' to the work queue
  send dir       Sends the contents of 'dir' to the server for remote building
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

def client(op, **kwargs):
    
    # Used for identifying server return codes in a user friendly manner
    returnStrings = {'build' : [_("Build process is successfully finished!"),
                                _("Buildfarm is busy!"),
                                _("Work Queue is empty!"),
                                _("Queue finished with problems :(")],
                     'add'   : [_("%s successfully added to the work queue!"),
                                _("The package '%s' doesn't exist!"),
                                _("The package '%s' is already in the work queue!")]
                    }
                                
                                
                                
    
    # TODO : I can build a list of all formatted strings and select them
    # with the return values provided by the server to minimize the code.
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
    
    elif op == "send":
        # pspec is a directory which can contain 1 or more packages
        retval = sendDirectory(server, kwargs[pspec], "ozan")
        if retval:
            print _("Everything's OK")
        else:
            print _("There were problems during the process")
        
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
        print returnStrings['build'][retval]
    
    # 3 or more Parameters
    elif op == "add":
        for pspec in pspecList:
            retval = server.appendToWorkQueue(pspec, True)
            print (returnStrings['add'][retval] % pspec)
            
    elif op == "remove":
        funcString = "removeFrom" + cmd.capitalize() + "Queue"
        for pspec in pspecList:    
            print _("Removing '%s' from %s queue.." % (pspec, cmd)),
            retval = server.__getattr__(funcString)(pspec)
            if retval:
                print _("[Removed]")
            else:
                print _("[Doesn't exist]")
            
    elif op == "transfer":
        funcString = "transferTo" + cmd.capitalize() + "Queue"
        for pspec in pspecList:
            print _("Transferring '%s' to %s queue.." % (pspec, cmd)),
            retval = server.__getattr__(funcString)(pspec)
            if retval:
                print _("[Transferred]")
            else:
                print _("[Doesn't exist]")
            
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
        
    


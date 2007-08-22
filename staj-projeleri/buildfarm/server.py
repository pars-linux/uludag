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
#
# XMLRPC over SSL Based on :
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496786

KEYFILE="certs/new.cert.key"
CERTFILE="certs/new.cert.cert"

import sys
import os

import socket
import SocketServer
import BaseHTTPServer
import SimpleXMLRPCServer

""" pyOpenSSL """
from OpenSSL import SSL

""" helpers """
from helpers import qmanager
from helpers import repomanager

import main
import config

# Inherits from ForkingMixIn for multi-process support

class SecureXMLRPCServer(SocketServer.ForkingMixIn,
                         BaseHTTPServer.HTTPServer,
                         SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    
    # "SocketServer.py" cleans the zombies just after a new connection request
    # This function overrides the SIGCHLD handler for immediate clean-up.
    def overrideHandler(self):
        def SIGCHLDHandler(signum,frame):
            # dummy wrapper for calling collect_children()
            self.collect_children()
        import signal
        signal.signal(signal.SIGCHLD, SIGCHLDHandler)
        
    def __init__(self, server_address, HandlerClass, logRequests=True):
        
        # Override SIGCHLD Handler
        self.overrideHandler()
        
        self.logRequests = logRequests

        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self)
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
        # ssl related stuff
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file (KEYFILE)
        ctx.use_certificate_file(CERTFILE)
        # opens the ssl socket
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))
        self.server_bind()
        self.server_activate()
        
    def __getattr__(self,obj):
        return getattr(self,obj)

class SecureXMLRpcRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def do_POST(self):
        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and dispatch
            # using that method if present.
            response = self.server._marshaled_dispatch(data, getattr(self, "_dispatch", None))
        except: 
            # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown()

class CombinedServerClass(qmanager.QueueManager, repomanager.RepositoryManager):
    pass

def runServer():
    
    # Initialize server instance
    server = SecureXMLRPCServer((config.HOST, config.PORT), SecureXMLRpcRequestHandler)
    
    # let server.system.listMethods
    server.register_introspection_functions()
    
    # export CombinedServerClass
    server.register_instance(CombinedServerClass())
    
    # export buildPackages, buildIndex
    # FIXME: run these on another thread and return to client ASAP
    server.register_function(main.buildPackages)
    server.register_function(main.buildIndex)
    
    # enter main loop
    server.serve_forever()

if __name__ == "__main__":
    
    ## Add stream redirections
    #try:
    #    pid = os.fork()
    #    if pid > 0:
    #        # Exit first parent
    #        sys.exit(0)
    #except OSError, e:
    #    print >> sys.stderr, "fork() failed: %d (%s)" % (e.errno, e.strerror)
    #    sys.exit(1)
    #    
    ## Decouple from parent environment
    ##os.chdir("/")
    #os.setsid()
    #os.umask(0)
    #
    ## Do second fork
    #try:
    #    pid = os.fork()
    #    if pid > 0:
    #        # Exit from second parent
    #        sys.exit(0)
    #except OSError, e:
    #    print >> sys.stderr, "fork() failed: %d (%s)" % (e.errno, e.strerror)
    #    sys.exit(1)
    #    
    ## Start the daemon main loop
    
    runServer()

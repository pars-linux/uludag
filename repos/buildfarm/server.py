#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.
#
# Based on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496786

LISTEN_HOST="localhost"
LISTEN_PORT=443
KEYFILE="certs/new.cert.key"
CERTFILE="certs/new.cert.cert"

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

class SecureXMLRPCServer(BaseHTTPServer.HTTPServer,SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    def __init__(self, server_address, HandlerClass, logRequests=True):
        self.logRequests = logRequests

        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self)
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file (KEYFILE)
        ctx.use_certificate_file(CERTFILE)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))
        self.server_bind()
        self.server_activate()

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
            response = self.server._marshaled_dispatch
                (
                    data, getattr(self, "_dispatch", None)
                )
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

server = SecureXMLRPCServer((LISTEN_HOST, LISTEN_PORT), SecureXMLRpcRequestHandler)

# let server.system.listMethods
server.register_introspection_functions()

# export CombinedServerClass
server.register_instance(CombinedServerClass())

# export buildPackages
server.register_function(main.buildPackages)

# enter main loop
server.serve_forever()

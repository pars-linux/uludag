# Client code

import xmlrpclib

server = xmlrpclib.Server('http://localhost:8000')

print server.system.listMethods()

print server.updateRepository()

print server.getWorkQueue()
print server.getWaitQueue()

#print server.removeFromWorkQueue("a/pspec.xml")
#
#print server.appendToWaitQueue("b/pspec.xml")
#
#print server.buildPackages()

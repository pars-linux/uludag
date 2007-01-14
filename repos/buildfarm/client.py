# Client code

import xmlrpclib

server = xmlrpclib.Server('http://localhost:8000')

print "Provided Methotds: %s" % server.system.listMethods()

print "Update repository: %s" % server.updateRepository()

print "WorkQueue: %s" % server.getWorkQueue()
print "WaitQueue: %s" % server.getWaitQueue()

print "Remove A from WorkQueue: %s" % server.removeFromWorkQueue("a/pspec.xml")
print "Append b to WaitQueue: %s" % server.appendToWaitQueue("b/pspec.xml")
print "Append A to WorkQueue: %s" % server.appendToWorkQueue("a/pspec.xml")

print "WorkQueue: %s" % server.getWorkQueue()
print "WaitQueue: %s" % server.getWaitQueue()

print server.buildPackages()

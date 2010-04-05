#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pisi
from twisted.web import xmlrpc, server

#from buildfarm import config
#PORT = 8007

class BuildService(xmlrpc.XMLRPC):

    def xmlrpc_start(self, release, distribution="Pardus"):
        """Starts the corresponding buildfarm service

        @type   distribution:  string
        @param  distribution:  The distribution name for which the corresponding
                                build service will be started.

        @type   release:    string
        @param  release:    The distribution release for which the corresponding
                            build service will be started.

        @rtype: bool
        @return: True if the build service is succesfully started
        """

        # FIXME: Implement
        return "Started buildfarm for %s %s" % (distribution, release)

    def xmlrpc_stop(self, release, distribution="Pardus"):
        """Stops the corresponding buildfarm service."""
        # FIXME: Implement
        return "Stopped buildfarm for %s %s" % (distribution, release)

    def xmlrpc_push(self, release, package, distribution="Pardus"):
        """Push a package to the corresponding buildfarm's queue."""
        # FIXME: Implement
        return "Pushed %s to %s %s buildfarm" % (package, distribution, release)

    def xmlrpc_pop(self, release, package, distribution="Pardus"):
        """Pop a package from the corresponding buildfarm's queue."""
        # FIXME: Implement
        return "Popped %s from %s %s buildfarm" % (package, distribution, release)

    def xmlrpc_list(self):
        """List currently online buildfarms."""
        # FIXME: Implement
        return "Listing online buildfarms"

    def xmlrpc_status(self, release, package, distribution="Pardus"):
        """Lists the current status of the corresponding buildfarm service."""
        # FIXME: Implement
        return "Stopped buildfarm for %s %s" % (distribution, release)

if __name__ == "__main__":
    from twisted.internet import reactor
    reactor.listenTCP(PORT, server.Site(BuildService()))
    reactor.run()

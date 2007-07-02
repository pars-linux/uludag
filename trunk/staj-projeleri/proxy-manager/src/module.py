# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

class Module:
    
    # Following variables determine if the a configuration file of
    # an application that supports more then one protocol is open.
    def __init__(self):
        pass
    
    def setGlobalProxy(self,ip, port=None):
##        for module in self.modules:
##            if(module.__class__.__dict__.get("setGlobalProxy")):
##                module.setGlobalProxy(ip)
##            else:
##                print "method is not defined"
        return
    
    def setHTTPProxy(ip, port=None):
        return
    
    def setFTPProxy(ip, port=None):
        return
    
    def setGopherProxy(ip, port=None):
        return
    
    def setSSLProxy(self, ip, port=None):
        return
    
    def setSOCKSProxy(self, ip, port=None):
        return

    def noProxy(self):
        return

    def close(self):
        return

# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

class App:
    
    # Following variables determine if the a configuration file of
    # an application that supports more then one protocol is open.
    def __init__(self):
        pass
    
    def setGlobalProxy(self, ip, port=None, user=None, pasw=None):
        return
    
    def setHTTPProxy(self, ip, port=None, user=None, pasw=None):
        return
    
    def setFTPProxy(self, ip, port=None, user=None, pasw=None):
        return
    
    def setGopherProxy(self, ip, port=None, user=None, pasw=None):
        return
    
    def setSSLProxy(self, ip, port=None, user=None, pasw=None):
        return
    
    def setSOCKSProxy(self, ip, port=None, user=None, pasw=None):
        return

    def setPAC_URL(self, url):
        return
    
    def noProxy(self):
        return

    def close(self):
        return

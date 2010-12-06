#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar

class Backend:

    def __init__(self, parent):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("System.Service", parent.handleSignals)


    def info(self, service, async = None):
        if async:
            self.link.System.Service[service].info(async=async)
        else:
            return self.link.System.Service[service].info()

    def services(self):
        return list(self.link.System.Service)

    def run(self, method, async = None):
        try:
            if async:
                method(async = async)
            else:
                method()
            return True

        except Exception, msg:
            print 'Error: ', msg
            return False

    def start(self, service, async = None):
        return self.run(self.link.System.Service[service].start, async)

    def stop(self, service, async = None):
        return self.run(self.link.System.Service[service].stop, async)

    def set_state(self, service, state):
        return self.run(lambda:self.link.System.Service[service].setState(state))


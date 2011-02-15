#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import comar

from kdecore import i18n
from kdeui import KMessageBox

class Backend:

    def __init__(self, parent):
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("System.Service", parent.handleSignals)
        self.parent = parent

    def show_error(self, msg):
        return KMessageBox.error(self.parent, msg, i18n('Error'))

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
            if 'PolicyKit' in unicode(msg):
                self.show_error(i18n('You are not authorized for this operation.'))
            else:
                self.show_error(i18n('An error occurred:\n%s' % unicode(msg)))
            return False

    def start(self, service, async = None):
        return self.run(self.link.System.Service[service].start, async)

    def stop(self, service, async = None):
        return self.run(self.link.System.Service[service].stop, async)

    def set_state(self, service, state):
        return self.run(lambda:self.link.System.Service[service].setState(state))


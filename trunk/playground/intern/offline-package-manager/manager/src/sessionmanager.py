#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file
 
import backend

class SessionManager:

    (NORMAL, OFFLINE) = range(2)

    def __init__(self):
	pass

    def setSession(self, session):
	if session == self.NORMAL:
	    backend.pm = backend.normal_pm
	else:
	    backend.pm = backend.offline_pm
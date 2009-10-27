#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

import sys
import pisi

def get_history_dir():
    return pisi.ctx.config.history_dir()

def get_config_files(op):
    pass

def getPlan(op):
    return pisi.api.get_takeback_plan(op)

def reloadPisi():
    for module in sys.modules.keys():
        if module.startswith("pisi."):
            """removal from sys.modules forces reload via import"""
            del sys.modules[module]

    reload(pisi)

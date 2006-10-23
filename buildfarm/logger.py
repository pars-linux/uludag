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

""" Standart Python Modules """
import os
import sys
import time
import string

""" BuildFarm Modules """
from config import logFile as logFile

def findCaller():
    if string.lower(__file__[-4:]) in [".pyc", ".pyo"]:
        srcFile = __file__[:-4] + ".py"
    else:
        srcFile = __file__
    srcFile = os.path.normcase(srcFile)

    f = sys._getframe().f_back
    while 1:
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == srcFile:
            f = f.f_back
            continue
        return ":".join([os.path.basename(filename), str(f.f_lineno)])


def __raw(msg):
    open(logFile, "a").write("\n\n%s\n\n" %(msg))

def __log(level, caller, msg):
    print msg
    open(logFile, "a").write("%s | %-6.6s | %-16.16s :: %s\n" %(time.asctime(), level, caller, msg))


def debug(msg): __log("DEBUG", findCaller(), msg)

def error(msg): __log("ERROR", findCaller(), msg)

def info(msg): __log("INFO", findCaller(), msg)

def raw(msg = "-- --"): __raw(msg)

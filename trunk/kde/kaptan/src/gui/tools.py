#!/usr/bin/python
# -*- coding: utf-8 -*-

def isLiveCD():
    try:
        liveCDcheck = open('/var/run/pardus/livemedia')
    except IOError:
        return False

    return True

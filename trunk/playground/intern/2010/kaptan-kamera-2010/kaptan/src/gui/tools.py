#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def isLiveCD():
    return os.path.exists('/var/run/pardus/livemedia')

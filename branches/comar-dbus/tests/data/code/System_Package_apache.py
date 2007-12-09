#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time

def postInstall(a):
    time.sleep(random.randint(1, 3))
    return "You said: '%s'" % a

#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time

def postInstall(a, b=2.0):
    time.sleep(random.randint(1, 3))
    return "a: %s\nb: %s" % (repr(a), repr(b))

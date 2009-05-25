#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, glob

for filename in glob.glob1("gui", "*.ui"):
    os.system("/usr/kde/4/bin/pykde4uic -o gui/%s.py gui/%s" % (filename.split(".")[0], filename))

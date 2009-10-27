#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, glob

for filename in glob.glob1("gui", "*.ui"):
    os.system("/usr/kde/4/bin/pykde4uic -o gui/%s.py gui/%s" % (filename.split(".")[0], filename))

for filename in glob.glob1("gui", "*.qrc"):
    os.system("/usr/bin/pyrcc4 gui/%s -o gui/%s_rc.py" % (filename, filename.split(".")[0]))

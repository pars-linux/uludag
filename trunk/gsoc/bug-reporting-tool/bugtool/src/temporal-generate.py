#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, glob

for filename in glob.glob1("gui/widgets", "*.ui"):
    os.system("pykdeuic4 -o gui/%s.py gui/widgets/%s" % (filename.split(".")[0], filename))

for filename in glob.glob1("gui", "*.qrc"):
    os.system("pyrcc4 gui/%s -o gui/%s_rc.py" % (filename, filename.split(".")[0]))

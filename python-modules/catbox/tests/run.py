#!/usr/bin/python

import os
import sys

tests = """
    basic-test.py
    operations-test.py
    follow-test.py
    fork-test.py
    class-test.py
    retcode-test.py
    maxpath-test.py
"""

base = os.path.dirname(sys.argv[0])
for name in tests.split():
    os.system(os.path.join(base, name))


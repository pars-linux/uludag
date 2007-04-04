#!/usr/bin/python

import sys
import os
import catbox

def testMaxPath():
    count = 1
    while True:
        name = "a" * count
        try:
            if os.path.exists(name):
                os.rmdir(name)
            os.mkdir(name)
        except OSError, e:
            if e.errno == 36:
                print "max name", count
                return count
            print e
            raise
        count += 1

testMaxPath()

ret = catbox.run(testMaxPath, [os.getcwd()])
assert(ret.code == 0)
assert(ret.violations == [])

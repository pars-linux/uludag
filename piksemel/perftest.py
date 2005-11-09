#!/usr/bin/python

import sys
import piksemel as iks
import xml.dom.minidom as mini
import timeit

def piksor(name):
    a = iks.parse(name)
    print "Processing %s" % a.name()
    total = 0
    for b in a.tags():
        size = b.getTagData("Size")
        if size:
            size = size.strip()
            total += int(size)
    print "Total size is %d" % total

def suxor(name):
    a = mini.parse(name)
    print a.documentElement.tagName

if __name__ == "__main__":
    name = sys.argv[1]
    a = timeit.Timer('piksor("%s")' % name, "from __main__ import piksor")
    b = timeit.Timer('suxor("%s")' % name, "from __main__ import suxor")
    print a.timeit(1)
    print b.timeit(1)



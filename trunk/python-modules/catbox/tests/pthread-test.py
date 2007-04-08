#!/usr/bin/python

import os
import sys
import catbox
import thread

def test():
    file("lala", "w").write("hello world\n")

def main():
    thread.start_new_thread(test, tuple())
    thread.start_new_thread(test, tuple())
    thread.start_new_thread(test, tuple())
    test()

ret = catbox.run(main)
print ret.code, ret.violations

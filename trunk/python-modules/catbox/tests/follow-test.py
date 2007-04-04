#!/usr/bin/python

import os
import sys
import catbox

def good_op():
    os.unlink("catboxtest.link")

def bad_op():
    file("catboxtest2.link", "w").write("hello world\n")

def mklink(dest, source):
    if os.path.exists(source):
        os.unlink(source)
    os.symlink(dest, source)

mklink("/var", "catboxtest.link")
mklink("/tmp/hede", "catboxtest2.link")

ret = catbox.run(good_op, writable_paths=[os.getcwd()])
assert(ret.code == 0)
assert(ret.violations == [])

ret = catbox.run(bad_op, writable_paths=[os.getcwd()])
assert(ret.code == 1)
assert(len(ret.violations) == 1)

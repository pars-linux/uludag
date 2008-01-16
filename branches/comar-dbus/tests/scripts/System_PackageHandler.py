# -*- coding: utf-8 -*-

import piksemel
import os
from subprocess import *

pythonPath="/usr/lib/python2.4"

def byteCompile(filepath):
    doc = piksemel.parse(filepath)
    for item in doc.tags("File"):
        path = item.getTagData("Path")
        if path.endswith(".py"):
            call(["/usr/bin/python", "%s/py_compile.py" % pythonPath, "/%s" % path], stderr=PIPE, stdout=PIPE)
            call(["/usr/bin/python","-O", "%s/py_compile.py" % pythonPath, "/%s" % path], stderr=PIPE, stdout=PIPE)

def removeByteCompiled(filepath):
    doc = piksemel.parse(filepath)
    for item in doc.tags("File"):
        path = item.getTagData("Path")
        if path.endswith(".py"):
            try:
                # Remove .pyc and .pyo
                os.unlink("/%sc" % path)
                os.unlink("/%so" % path)
            except OSError:
                pass

def setupPackage(metapath, filepath):
    byteCompile(filepath)

def cleanupPackage(metapath, filepath):
    removeByteCompiled(filepath)

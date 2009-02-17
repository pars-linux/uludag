#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import glob
import os

COMAR_DB = "/var/db/comar/code"

def main():
    if os.getuid() != 0:
        print "Must be run as root."
        return -1

    link = comar.Link()

    for filename in os.listdir(COMAR_DB):
        if filename.endswith(".py"):
            _group, _class, _app = filename.split("_", 2)
            _model = "%s.%s" % (_group, _class)
            _app = _app.rsplit(".py", 1)[0]
            link.register(_app, _model, os.path.join(COMAR_DB, filename))
            print filename

    return 0

if __name__ == "__main__":
    main()

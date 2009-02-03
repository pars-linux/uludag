#!/usr/bin/python
# -*- coding: utf-8 -*-

import comar
import dbus
import locale
import sys
import os

def printUsage():
    print "Usage: %s <command>" % sys.argv[0]
    print "Commands:"
    print "  call <app> <model> <method> <arguments>"
    print "  list-apps <model>"
    print "  register <app> <model> <script.py>"
    print "  remove <app>"
    sys.exit(1)

def main():
    if len(sys.argv) == 1:
        printUsage()

    link = comar.Link("3")
    link.setLocale()

    if sys.argv[1] == "list-apps":
        try:
            model = sys.argv[2]
        except IndexError:
            printUsage()
        try:
            _group, _class = model.split(".")
        except ValueError:
            print "Invalid model name"
            return -1
        apps = list(comar.Call(link, _group, _class))
        for app in apps:
            print app
    elif sys.argv[1] == "register":
        try:
            app = sys.argv[2]
            model = sys.argv[3]
            script = os.path.realpath(sys.argv[4])
        except IndexError:
            printUsage()
        link.register(app, model, script)
    elif sys.argv[1] == "remove":
        try:
            app = sys.argv[2]
        except IndexError:
            printUsage()
        link.remove(app)
    elif sys.argv[1] == "call":
        try:
            app = sys.argv[2]
            model = sys.argv[3]
            method = sys.argv[4]
        except IndexError:
            printUsage()
        try:
            _group, _class = model.split(".")
        except ValueError:
            print "Invalid model name"
            return -1
        met = comar.Call(link, _group, _class, app, method)
        if len(sys.argv) > 5:
            args = []
            for i in sys.argv[5:]:
                if i.startswith("[") or i.startswith("(") or i.startswith("{"):
                    args.append(eval(i))
                else:
                    args.append(i)
            print met.call(*args)
        else:
            print met.call()
    else:
        printUsage()

    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/python

import os
import sys

def register(app, model, script):
    script = os.path.realpath(script)
    print "Registering %s_%s.py..." % (model, app)
    os.system("dbus-send --system --dest=tr.org.pardus.comar --type=method_call --print-reply /system tr.org.pardus.comar.register string:'%s' string:'%s' string:'%s'" % (app, model, script))

def main():
    register("grub", "Boot.Loader", "scripts/Boot_Loader_grub.py")
    register("mysql", "System.Package", "scripts/System_Package_mysql.py")

    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import sys
import exceptions

import pisi

def handle_exception(exception, value, tb):
    if exception == exceptions.KeyboardInterrupt:
        pisi.api.finalize()
        print("\n")
        sys.exit()

def ask_action(msg, actions, default):
    while True:
        s = raw_input(msg)
        if len(s) == 0:
            return default
        else:
            if s not in actions:
                continue

        return s

def get_installed_packages():
    return pisi.context.installdb.list_installed()

def check_changed_config_files(package):
    all_files = pisi.context.installdb.files(package)
    config_files = filter(lambda x: x.type == 'config', all_files.list)
    config_paths = map(lambda x: "/" + str(x.path), config_files)

    newconfig = [] 
    for path in config_paths:
        if os.path.exists(path) and os.path.exists(path + ".newconfig"):
            newconfig.append(path)

    return newconfig

def show_changes(package, changed):
    prompt = "%s has new config files. Would you like to see them [Y/n] " % package
    if ask_action(prompt, ["y","n"], "y") == "n":
        return

    for file in changed:
        prompt = "    %s has changed. Would you like to overwrite new config file [N/y/?] " % file
        answer = ask_action(prompt, ["y", "n", "?"], "n")

        if answer == "y":
            os.rename(file+".newconfig", file)
        if answer == "n":
            continue

        while answer == "?":
            os.system("diff -u %s %s | less" % (file, file + ".newconfig"))
            answer = ask_action(prompt, ["y", "n", "?"], "n")

            if answer == "y":
                os.rename(file+".newconfig", file)
                break
            if answer == "n":
                break

def check_package(package):
    changed = check_changed_config_files(package)
    if changed:
        show_changes(package, changed)

def check_changes():
    packages = get_installed_packages()
    for pkg in packages:
        check_package(pkg)

if __name__ == "__main__":
     sys.excepthook = handle_exception
     pisi.api.init(write=False)

     if len(sys.argv) == 1:
         print "Checking all packages"
         check_changes()
     if len(sys.argv) == 2:
         check_package(sys.argv[1])
     if len(sys.argv) > 2:
         for pkg in sys.argv[1:]:
             check_package(pkg)

     pisi.api.finalize()

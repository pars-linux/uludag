#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys
import os
import locale
import time
import dbus

# i18n

import gettext
__trans = gettext.translation('mudur', fallback=True)
_ = __trans.ugettext

# Utilities

def loadConfig(path):
    dict = {}
    for line in file(path):
        if line != "" and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('"') or value.startswith("'"):
                value = value[1:-1]
            dict[key] = value
    return dict

# Operations

class Service:
    types = {
        "local": _("local"),
        "script": _("script"),
        "server": _("server"),
    }
    
    def __init__(self, name, info=None):
        self.name = name
        self.running = ""
        self.autostart = ""
        if info:
            type, self.description, state = info
            self.state = state
            self.type = self.types[type]
            if state in ("on", "started"):
                self.running = _("running")
            if state in ("on", "stopped"):
                self.autostart = _("yes")


def format_service_list(services, use_color=True):
    if os.environ.get("TERM", "") == "xterm":
        colors = {
            "on": '[0;32m',
            "started": '[1;32m',
            "stopped": '[0;31m',
            "off": '[0m'
        }
    else:
        colors = {
            "on": '[1;32m',
            "started": '[0;32m',
            "stopped": '[1;31m',
            "off": '[0m'
        }
    name_title = _("Service")
    run_title = _("Status")
    auto_title = _("Autostart")
    desc_title = _("Description")
    
    name_size = max(max(map(lambda x: len(x.name), services)), len(name_title))
    run_size = max(max(map(lambda x: len(x.running), services)), len(run_title))
    auto_size = max(max(map(lambda x: len(x.autostart), services)), len(auto_title))
    desc_size = len(desc_title)
    
    line = "%s | %s | %s | %s" % (
        name_title.center(name_size),
        run_title.center(run_size),
        auto_title.center(auto_size),
        desc_title.center(desc_size)
    )
    print line
    print "-" * (len(line))
    
    cstart = ""
    cend = ""
    if use_color:
        cend = "\x1b[0m"
    for service in services:
        if use_color:
            cstart = "\x1b%s" % colors[service.state]
        line = "%s%s%s | %s%s%s | %s%s%s | %s%s%s" % (
            cstart,
            service.name.ljust(name_size),
            cend, cstart,
            service.running.center(run_size),
            cend, cstart,
            service.autostart.center(auto_size),
            cend, cstart,
            service.description,
            cend
        )
        print line

def startService(service, bus):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    print _("Starting %s..." % service)
    obj.start(dbus_interface="tr.org.pardus.comar.System.Service")

def stopService(service, bus):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    print _("Stopping %s..." % service)
    obj.stop(dbus_interface="tr.org.pardus.comar.System.Service")

def setServiceState(service, state, bus):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    obj.setState(state, dbus_interface="tr.org.pardus.comar.System.Service")
    if state == "on":
        print _("Service '%s' will be auto started.") % service
    else:
        print _("Service '%s' won't be auto started.") % service

def reloadService(service, bus):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    print _("Reloading %s..." % service)
    obj.reload(dbus_interface="tr.org.pardus.comar.System.Service")

def getServiceInfo(service, bus):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    return obj.info(dbus_interface="tr.org.pardus.comar.System.Service")

def getServices(bus):
    obj = bus.get_object("tr.org.pardus.comar", "/", introspect=False)
    return obj.listModelApplications("System.Service", dbus_interface="tr.org.pardus.comar")

def list_services(use_color=True):
    bus = dbus.SystemBus()
    services = []
    for service in getServices(bus):
        services.append((service, getServiceInfo(service, bus), ))
    
    if len(services) > 0:
        services.sort(key=lambda x: x[0])
        lala = []
        for service, info in services:
            lala.append(Service(service, info))
        format_service_list(lala, use_color)

def manage_service(service, op, use_color=True):
    bus = dbus.SystemBus()
    
    if op == "start":
        startService(service, bus)
    elif op == "stop":
        stopService(service, bus)
    elif op == "reload":
        pass
        #reloadService(service)
        #print _("Service '%s' reloaded.") % service
    elif op == "on":
        setServiceState(service, "on", bus)
    elif op == "off":
        setServiceState(service, "off", bus)
    elif op in ["info", "status", "list"]:
        info = getServiceInfo(service, bus)
        s = Service(service, info)
        format_service_list([s], use_color)
    elif op == "restart":
        manage_service(service, "stop")
        manage_service(service, "start")
        return

# Usage

def usage():
    print _("""usage: service [<options>] [<service>] <command>
where command is:
 list     Display service list
 status   Display service status
 info     Display service status
 on       Auto start the service
 off      Don't auto start the service
 start    Start the service
 stop     Stop the service
 restart  Stop the service, then start again
 reload   Reload the configuration (if service supports this)
and option is:
 -N, --no-color  Don't use color in output""")

# Main

def main(args):
    operations = ("start", "stop", "info", "list", "restart", "reload", "status", "on", "off")
    use_color = True
    
    # Parameters
    if "--no-color" in args:
        args.remove("--no-color")
        use_color = False
    if "-N" in args:
        args.remove("-N")
        use_color = False
    
    # Operations
    if args == []:
        list_services(use_color)
    
    elif args[0] == "list" and len(args) == 1:
        list_services(use_color)
    
    elif args[0] == "help":
        usage()
    
    elif len(args) < 2:
        usage()
    
    elif args[1] in operations:
        manage_service(args[0], args[1], use_color)
    
    else:
        usage()

#

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    main(sys.argv[1:])

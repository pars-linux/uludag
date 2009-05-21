#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sys
import time
import dbus
import socket
import locale
import subprocess

# i18n

import gettext
__trans = gettext.translation('mudur', fallback=True)
_ = __trans.ugettext

# Utilities

def loadConfig(path):
    d = {}
    for line in file(path):
        if line != "" and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('"') or value.startswith("'"):
                value = value[1:-1]
            d[key] = value
    return d

def waitBus(unix_name, timeout=10, wait=0.1, stream=True):
    if stream:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    else:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    while timeout > 0:
        try:
            sock.connect(unix_name)
            return True
        except:
            timeout -= wait
        time.sleep(wait)
    return False

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
            servicetype, self.description, state = info
            self.state = state
            self.servicetype = self.types[servicetype]
            if state in ("on", "started", "conditional_started"):
                self.running = _("running")
            if state in ("on", "stopped"):
                self.autostart = _("yes")
            if state in ("conditional_started", "conditional_stopped"):
                self.autostart = _("conditional")


def format_service_list(services, use_color=True):
    if os.environ.get("TERM", "") == "xterm":
        colors = {
            "on": '[0;32m',
            "started": '[1;32m',
            "stopped": '[0;31m',
            "off": '[0m',
            "conditional_started": '[1;32m',
            "conditional_stopped": '[1;33m',
        }
    else:
        colors = {
            "on": '[1;32m',
            "started": '[0;32m',
            "stopped": '[1;31m',
            "off": '[0m',
            "conditional_started": '[0;32m',
            "conditional_stopped": '[0;33m',
        }

    run_title  = _("Status")
    name_title = _("Service")
    auto_title = _("Autostart")
    desc_title = _("Description")

    run_size  = max(max(map(lambda x: len(x.running), services)), len(run_title))
    name_size = max(max(map(lambda x: len(x.name), services)), len(name_title))
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

def readyService(service, bus):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    obj.ready(dbus_interface="tr.org.pardus.comar.System.Service")

def startService(service, bus, quiet=False):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    if not quiet:
        print _("Starting %s") % service
    obj.start(dbus_interface="tr.org.pardus.comar.System.Service")

def stopService(service, bus, quiet=False):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    if not quiet:
        print _("Stopping %s") % service
    obj.stop(dbus_interface="tr.org.pardus.comar.System.Service")

def setServiceState(service, state, bus, quiet=False):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    obj.setState(state, dbus_interface="tr.org.pardus.comar.System.Service")
    if not quiet:
        if state == "on":
            print _("Service '%s' will be auto started.") % service
        elif state == "off":
            print _("Service '%s' won't be auto started.") % service
        else:
            print _("Service '%s' will be started if required.") % service

def reloadService(service, bus, quiet=False):
    obj = bus.get_object("tr.org.pardus.comar", "/package/%s" % service, introspect=False)
    if not quiet:
        print _("Reloading %s") % service
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

def manage_service(service, op, use_color=True, quiet=False):
    if os.getuid() != 0 and op not in ["status", "info", "list"]:
        print _("You must be root to use that.")
        return -1

    bus = dbus.SystemBus()

    if op == "ready":
        readyService(service, bus)
    elif op == "start":
        startService(service, bus, quiet)
    elif op == "stop":
        stopService(service, bus, quiet)
    elif op == "reload":
        reloadService(service, bus, quiet)
    elif op == "on":
        setServiceState(service, "on", bus, quiet)
    elif op == "off":
        setServiceState(service, "off", bus, quiet)
    elif op == "conditional":
        setServiceState(service, "conditional", bus, quiet)
    elif op in ["info", "status", "list"]:
        info = getServiceInfo(service, bus)
        s = Service(service, info)
        format_service_list([s], use_color)
    elif op == "restart":
        manage_service(service, "stop", use_color, quiet)
        manage_service(service, "start", use_color, quiet)

def run(*cmd):
    subprocess.call(cmd)

def manage_dbus(op, use_color, quiet):
    if os.getuid() != 0 and op not in ["status", "info", "list"]:
        print _("You must be root to use that.")
        return -1

    def cleanup():
        try:
            os.unlink("/var/run/dbus/pid")
            os.unlink("/var/run/dbus/system_bus_socket")
        except OSError:
            pass
    if op == "start":
        if not quiet:
            print _("Starting %s") % "DBus"
        cleanup()
        if not os.path.exists("/var/lib/dbus/machine-id"):
            run("/usr/bin/dbus-uuidgen", "--ensure")
        run("/sbin/start-stop-daemon", "-b", "--start", "--quiet",
            "--pidfile", "/var/run/dbus/pid", "--exec", "/usr/bin/dbus-daemon",
            "--", "--system")
        if not waitBus("/var/run/dbus/system_bus_socket", timeout=20):
            print _("Unable to start D-Bus")
            return -1
    elif op == "stop":
        if not quiet:
            print _("Stopping %s") % "DBus"
        run("/sbin/start-stop-daemon", "--stop", "--quiet", "--pidfile", "/var/run/dbus/pid")
        cleanup()
    elif op == "restart":
        manage_dbus("stop", use_color, quiet)
        manage_dbus("start", use_color, quiet)
    elif op in ["info", "status", "list"]:
        try:
            dbus.SystemBus()
        except dbus.DBusException:
            print _("DBus is not running.")
            return
        print _("DBus is running.")

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
 -N, --no-color  Don't use color in output
 -q, --quiet     Don't print replies""")

# Main

def main(args):
    operations = ("start", "stop", "info", "list", "restart", "reload", "status", "on", "off", "ready", "conditional")
    use_color = True
    quiet = False

    # Parameters
    if "--no-color" in args:
        args.remove("--no-color")
        use_color = False
    if "-N" in args:
        args.remove("-N")
        use_color = False
    if "--quiet" in args:
        args.remove("--quiet")
        quiet = True
    if "-q" in args:
        args.remove("-q")
        quiet = True

    # Operations
    if args == []:
        list_services(use_color)

    elif args[0] == "list" and len(args) == 1:
        list_services(use_color)

    elif args[0] == "help":
        usage()

    elif len(args) < 2:
        usage()

    elif args[1] in operations and args[0] == "dbus":
        manage_dbus(args[1], use_color, quiet)
    elif args[1] in operations:
        try:
            manage_service(args[0].replace("-", "_"), args[1], use_color, quiet)
        except dbus.DBusException, e:
            print e.args[0]
            return -1
        except ValueError, e:
            print e
            return -1
    else:
        usage()

    return 0

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    main(sys.argv[1:])

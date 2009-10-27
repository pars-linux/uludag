#!/usr/bin/python
# -*- coding: utf-8 -*-

serviceType="server"
serviceDesc = _({"en": "Firebird Database Server",
                 "tr": "Firebird Veritabanı Sunucusu"})

from pardus.serviceutils import *

@synchronized
def start():
    startService(command="/opt/firebird/bin/fbmgr.bin",
                 args="-pidfile %s -start -forever" % pid_file,
                 chuid="firebird",
                 pidfile="/var/run/firebird/firebird.pid",
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/firebird/firebird.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/firebird/firebird.pid")
